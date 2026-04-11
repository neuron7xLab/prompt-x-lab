"""Kriterion schemas — loaders and jsonschema validation.

Nine JSON Schemas ship as bundled assets under
``src/pxl/kriterion/assets/schemas/``. They are loaded via
``importlib.resources`` and validated with the ``jsonschema`` library
against instances produced by the evaluator or the benchmark runner.

A cross-reference resolver is configured so that inter-schema ``$ref``
pointers (e.g. ``canonical-artifact.schema.json`` from
``reference-input-bundle.schema.json``) resolve correctly.
"""

from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files
from typing import Any

import jsonschema
from jsonschema.validators import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

_SCHEMAS = files("pxl.kriterion") / "assets" / "schemas"

SCHEMA_NAMES = (
    "artifact-validation-result.schema.json",
    "canonical-artifact.schema.json",
    "domain-score.schema.json",
    "evaluation-result.schema.json",
    "gate-result.schema.json",
    "governance-invariant-registry.schema.json",
    "orchestration-handoff.schema.json",
    "reference-input-bundle.schema.json",
    "task-score.schema.json",
)


def list_schemas() -> list[str]:
    """Return the list of bundled schema names."""

    return list(SCHEMA_NAMES)


@lru_cache(maxsize=len(SCHEMA_NAMES))
def load_schema(name: str) -> dict[str, Any]:
    """Load a bundled schema by filename (e.g. ``'evaluation-result.schema.json'``)."""

    if name not in SCHEMA_NAMES:
        msg = f"unknown schema: {name}. Known: {SCHEMA_NAMES}"
        raise KeyError(msg)
    resource = _SCHEMAS / name
    raw: str = resource.read_text(encoding="utf-8")
    data: dict[str, Any] = json.loads(raw)
    return data


@lru_cache(maxsize=1)
def _registry() -> Registry[Any]:
    """Shared registry for inter-schema $ref resolution.

    Uses the modern ``referencing`` library instead of the deprecated
    ``jsonschema.RefResolver``. Every bundled schema is registered under
    both its filename and its ``$id`` (when present) so cross-schema
    references by either key resolve cleanly.
    """

    registry: Registry[Any] = Registry()
    for name in SCHEMA_NAMES:
        schema = load_schema(name)
        resource: Resource[Any] = DRAFT202012.create_resource(schema)
        registry = registry.with_resource(uri=name, resource=resource)
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            registry = registry.with_resource(uri=schema_id, resource=resource)
    return registry


def validate_against(schema_name: str, instance: Any) -> tuple[bool, str]:
    """Validate ``instance`` against the named schema.

    Returns ``(True, "VALID")`` on success, ``(False, <validator>)`` on
    failure. Inter-schema ``$ref`` pointers resolve via a shared
    ``referencing.Registry`` so the nine schemas can reference each
    other without filesystem dependencies.
    """

    schema = load_schema(schema_name)
    validator = Draft202012Validator(schema=schema, registry=_registry())
    try:
        validator.validate(instance)
        return True, "VALID"
    except jsonschema.ValidationError as e:
        return False, str(e.validator or "INVALID_SCHEMA")
