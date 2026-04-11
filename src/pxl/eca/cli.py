"""``pxl-eca`` command-line entry point."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import ECA_SELECTED_ITERATION, ECA_VERSION
from .config import load_best_config, load_metrics, load_router_spec
from .router import route_request
from .scorer import score_response
from .signer import sign_response
from .validate import validate_stack


def _cmd_info() -> int:
    spec = load_router_spec()
    best = load_best_config()
    metrics = load_metrics()
    print(
        json.dumps(
            {
                "eca_version": ECA_VERSION,
                "selected_iteration": ECA_SELECTED_ITERATION,
                "router_version": spec.version,
                "router_modes": sorted(spec.mode_lexicons.keys()),
                "shipping_thresholds": best.quality_thresholds.model_dump(),
                "metrics_version": metrics.version,
                "holdout_results": best.holdout_results.model_dump(),
            },
            indent=2,
        )
    )
    return 0


def _cmd_validate() -> int:
    from dataclasses import asdict

    report = validate_stack()
    payload = {
        "router_synthetic": asdict(report.router_synthetic),
        "router_adversarial": asdict(report.router_adversarial),
        "dual_output": asdict(report.dual_output),
        "quality_gate": asdict(report.quality_gate),
        "failures": report.failures,
        "ok": report.ok(),
    }
    print(json.dumps(payload, indent=2))
    return 0 if report.ok() else 1


def _cmd_route(args: argparse.Namespace) -> int:
    data = json.loads(Path(args.request).read_text(encoding="utf-8"))
    decision = route_request(data)
    print(json.dumps(decision.to_dict(), indent=2))
    return 0


def _cmd_score(args: argparse.Namespace) -> int:
    data = json.loads(Path(args.response).read_text(encoding="utf-8"))
    from .scorer import load_shipping_thresholds

    card = score_response(data, load_shipping_thresholds())
    print(json.dumps(card.to_dict(), indent=2))
    return 0 if card.ship else 1


def _cmd_sign(args: argparse.Namespace) -> int:
    data = json.loads(Path(args.response).read_text(encoding="utf-8"))
    sig = sign_response(data, secret=args.secret)
    print(sig)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pxl-eca", description="ECA Cognitive Engine CLI.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("info", help="Print bundled config + calibration summary.")
    sub.add_parser("validate", help="Reproduce calibration holdout metrics.")

    p_route = sub.add_parser("route", help="Route a request JSON to an ECA mode.")
    p_route.add_argument("request", help="Path to request JSON")

    p_score = sub.add_parser("score", help="Score a response JSON against shipping thresholds.")
    p_score.add_argument("response", help="Path to response JSON")

    p_sign = sub.add_parser("sign", help="HMAC-SHA256 sign a response JSON.")
    p_sign.add_argument("response", help="Path to response JSON")
    p_sign.add_argument("--secret", default=None, help="Signing secret (defaults to env)")

    args = parser.parse_args(argv)

    if args.cmd == "info":
        return _cmd_info()
    if args.cmd == "validate":
        return _cmd_validate()
    if args.cmd == "route":
        return _cmd_route(args)
    if args.cmd == "score":
        return _cmd_score(args)
    if args.cmd == "sign":
        return _cmd_sign(args)

    parser.print_help()
    return 2


def entrypoint() -> int:
    """Console-script entry point registered in pyproject.toml."""

    return main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(entrypoint())
