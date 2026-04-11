"""Audit tests — SHA256 body integrity for Layer 05."""

from __future__ import annotations

from pxl.audit import compute_manifest, extract_body, hash_body, iter_orchestration_files


def test_extract_body_pulls_first_fenced_block() -> None:
    text = "# h\n\n```\nAAA\nBBB\n```\n\nafter"
    assert extract_body(text) == "AAA\nBBB"


def test_extract_body_returns_empty_when_no_fence() -> None:
    assert extract_body("# just prose\n") == ""


def test_hash_body_is_deterministic() -> None:
    a = hash_body("abc")
    b = hash_body("abc")
    assert a == b
    assert len(a) == 64


def test_iter_orchestration_files_finds_26() -> None:
    files = iter_orchestration_files()
    assert len(files) == 26


def test_compute_manifest_matches_file_count() -> None:
    manifest = compute_manifest()
    files = iter_orchestration_files()
    assert len(manifest) == len(files)
    for _, digest in manifest:
        assert len(digest) == 64
