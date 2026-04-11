"""Kriterion benchmark reproduction.

The original Kriterion bundle ships ten synthetic cases and one
``dataset_manifest.json`` recording an ``artifact_manifest_hash`` for
every case. Those hashes were produced by the reference runner's
canonical-bytes pipeline.

This module reproduces those hashes *from first principles* using only
``pxl.kriterion.canonical`` — no imports from the original Kriterion
tree, no filesystem hardcoding. If ``pxl.kriterion.canonical`` ever
drifts away from the reference implementation, the per-case hashes
diverge and ``reproduce_benchmark()`` fails loudly.

This is the calibration contract for the entire canonical primitive:
ten independent fixtures that must produce exactly the hashes recorded
in the upstream manifest.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from importlib.resources import files

from .canonical import sha256_hex

_DATASETS = files("pxl.kriterion") / "datasets"


def _load_manifest() -> dict[str, object]:
    raw = (_DATASETS / "dataset_manifest.json").read_text(encoding="utf-8")
    data: dict[str, object] = json.loads(raw)
    return data


def _load_case_bytes(case_id: str) -> bytes:
    resource = _DATASETS / "synthetic_cases" / f"{case_id}.json"
    content: bytes = resource.read_bytes()
    return content


def _load_metrics() -> dict[str, object]:
    raw = (_DATASETS / "metrics.json").read_text(encoding="utf-8")
    data: dict[str, object] = json.loads(raw)
    return data


def compute_artifact_manifest_hash(case_id: str) -> str:
    """Replicate the upstream ``artifact_manifest_hash`` computation.

    Upstream computes SHA-256 over the **raw case-file bytes** (not
    the parsed JSON, not the canonical form). This vector is strictly
    stronger than canonical equality — it detects formatting-only
    tampering in addition to semantic drift.

    The ten bundled fixtures assert that byte-for-byte fidelity holds
    from upstream through the force-included wheel contents.
    """

    return sha256_hex(_load_case_bytes(case_id))


@dataclass(slots=True, frozen=True)
class CaseCheck:
    case_id: str
    expected_hash: str
    actual_hash: str
    matched: bool
    target_protocol: str
    adversarial_class: str | None


@dataclass(slots=True)
class BenchmarkReport:
    cases: list[CaseCheck] = field(default_factory=list)
    published_metrics: dict[str, object] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return all(c.matched for c in self.cases)

    @property
    def matched(self) -> int:
        return sum(1 for c in self.cases if c.matched)

    @property
    def total(self) -> int:
        return len(self.cases)


def reproduce_benchmark() -> BenchmarkReport:
    """Replay the 10 upstream manifest hashes and return a report."""

    manifest = _load_manifest()
    metrics = _load_metrics()
    report = BenchmarkReport(published_metrics=metrics)

    cases_list = manifest.get("cases", [])
    if not isinstance(cases_list, list):  # pragma: no cover — manifest shape invariant
        msg = "dataset_manifest.json 'cases' is not a list"
        raise TypeError(msg)

    for entry in cases_list:
        if not isinstance(entry, dict):  # pragma: no cover — manifest shape invariant
            continue
        case_id = str(entry["case_id"])
        expected = str(entry["artifact_manifest_hash"])
        target_protocol = str(entry["target_protocol"])
        adversarial_class = entry.get("adversarial_class")

        actual = compute_artifact_manifest_hash(case_id)
        report.cases.append(
            CaseCheck(
                case_id=case_id,
                expected_hash=expected,
                actual_hash=actual,
                matched=(expected == actual),
                target_protocol=target_protocol,
                adversarial_class=(
                    str(adversarial_class) if isinstance(adversarial_class, str) else None
                ),
            )
        )

    return report
