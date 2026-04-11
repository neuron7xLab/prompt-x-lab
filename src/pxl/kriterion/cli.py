"""``pxl-kriterion`` — command-line entry point."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import KRITERION_VERSION
from .benchmark import reproduce_benchmark
from .canonical import canonical_bytes, sha256_hex
from .protocols import list_protocols, load_protocol
from .schemas import list_schemas, validate_against


def _cmd_info() -> int:
    payload = {
        "kriterion_version": KRITERION_VERSION,
        "schemas": list_schemas(),
        "protocols": list_protocols(),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def _cmd_canonical(args: argparse.Namespace) -> int:
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    digest = sha256_hex(canonical_bytes(data))
    print(digest)
    if args.write_canonical:
        out = Path(args.input).with_suffix(Path(args.input).suffix + ".canonical.json")
        out.write_bytes(canonical_bytes(data))
        print(f"wrote {out}")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    data = json.loads(Path(args.instance).read_text(encoding="utf-8"))
    ok, reason = validate_against(args.schema, data)
    payload = {"schema": args.schema, "valid": ok, "reason": reason}
    print(json.dumps(payload, indent=2))
    return 0 if ok else 1


def _cmd_benchmark() -> int:
    report = reproduce_benchmark()
    payload = {
        "total": report.total,
        "matched": report.matched,
        "ok": report.ok,
        "published_metrics": report.published_metrics,
        "cases": [
            {
                "case_id": c.case_id,
                "matched": c.matched,
                "target_protocol": c.target_protocol,
                "adversarial_class": c.adversarial_class,
            }
            for c in report.cases
        ],
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if report.ok else 1


def _cmd_protocol(args: argparse.Namespace) -> int:
    print(load_protocol(args.id))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pxl-kriterion",
        description="Kriterion fail-closed evaluation primitives.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("info", help="Print version + bundled schemas + protocols.")
    sub.add_parser("benchmark", help="Reproduce the 10-case manifest-hash benchmark.")

    p_canonical = sub.add_parser(
        "canonical",
        help="Canonicalise a JSON file and print its SHA-256 fingerprint.",
    )
    p_canonical.add_argument("input")
    p_canonical.add_argument("--write-canonical", action="store_true")

    p_validate = sub.add_parser("validate", help="Validate a JSON instance against a bundled schema.")
    p_validate.add_argument("schema", help="Schema filename, e.g. evaluation-result.schema.json")
    p_validate.add_argument("instance", help="Path to JSON instance")

    p_protocol = sub.add_parser("protocol", help="Print a bundled protocol by ID.")
    p_protocol.add_argument("id", help="Protocol ID (with or without .txt)")

    args = parser.parse_args(argv)

    if args.cmd == "info":
        return _cmd_info()
    if args.cmd == "benchmark":
        return _cmd_benchmark()
    if args.cmd == "canonical":
        return _cmd_canonical(args)
    if args.cmd == "validate":
        return _cmd_validate(args)
    if args.cmd == "protocol":
        return _cmd_protocol(args)

    parser.print_help()
    return 2


def entrypoint() -> int:
    return main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(entrypoint())
