"""Kriterion schemas — loader + validator tests."""

from __future__ import annotations

from pxl.kriterion.schemas import SCHEMA_NAMES, list_schemas, load_schema, validate_against


def test_all_nine_schemas_load() -> None:
    assert len(SCHEMA_NAMES) == 9
    for name in SCHEMA_NAMES:
        schema = load_schema(name)
        assert "type" in schema or "$ref" in schema


def test_list_schemas_returns_full_set() -> None:
    assert set(list_schemas()) == set(SCHEMA_NAMES)


def test_load_schema_rejects_unknown() -> None:
    import pytest
    with pytest.raises(KeyError, match="unknown schema"):
        load_schema("not-a-real-schema.json")


def test_evaluation_result_schema_has_execution_chain_fields() -> None:
    schema = load_schema("evaluation-result.schema.json")
    required = schema.get("required", [])
    assert "execution_chain_format_version" in required
    assert "execution_state_chain" in required
    assert "execution_chain_terminal_hash" in required


def test_canonical_artifact_schema_enumerates_types() -> None:
    schema = load_schema("canonical-artifact.schema.json")
    artifact_type = schema["properties"]["artifact_type"]
    assert "enum" in artifact_type
    assert "RUNBOOK" in artifact_type["enum"]
    assert "THREAT_MODEL" in artifact_type["enum"]


def test_validate_against_rejects_empty_evaluation_result() -> None:
    ok, reason = validate_against("evaluation-result.schema.json", {})
    assert ok is False
    assert reason  # non-empty validator name


def test_validate_against_rejects_unknown_schema_name() -> None:
    import pytest
    with pytest.raises(KeyError):
        validate_against("nonsense.json", {})
