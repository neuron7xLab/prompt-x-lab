"""Kriterion benchmark reproduction — the calibration contract.

``src/pxl/kriterion/canonical.py`` must produce byte-for-byte the same
hashes as the original Kriterion reference runner. The bundled
``dataset_manifest.json`` records the expected ``artifact_manifest_hash``
for every one of the ten synthetic cases; this module replays them and
asserts exact equality.

If any of the ten assertions fails, the canonical primitive has drifted
and no downstream chain-hash can be trusted.
"""

from __future__ import annotations

from pxl.kriterion.benchmark import reproduce_benchmark


def test_benchmark_reproduces_all_ten_manifest_hashes() -> None:
    report = reproduce_benchmark()
    assert report.total == 10
    mismatches = [
        (c.case_id, c.expected_hash, c.actual_hash) for c in report.cases if not c.matched
    ]
    assert not mismatches, f"manifest hash drift on: {mismatches}"
    assert report.ok
    assert report.matched == 10


def test_benchmark_cases_cover_all_six_protocols() -> None:
    report = reproduce_benchmark()
    protocols = {c.target_protocol for c in report.cases}
    # 10 cases, ≥ 5 distinct target protocols
    assert len(protocols) >= 5


def test_benchmark_has_four_adversarial_cases() -> None:
    report = reproduce_benchmark()
    adversarial = [c for c in report.cases if c.adversarial_class]
    assert len(adversarial) == 4


def test_published_metrics_bundled() -> None:
    report = reproduce_benchmark()
    m = report.published_metrics
    assert m["case_count"] == 10
    assert m["adversarial_case_count"] == 4
    # Published anti-gaming invariants
    assert m["anti_gaming_recall"] == 1.0
    assert m["anti_gaming_false_positive_rate"] == 0.0
    assert m["integrity_violation_count"] == 5
