"""Evaluation runner — the real thing, end to end.

Invocation::

    from pxl.runner import run_spec
    result = run_spec(Path("evals/specs/executive-engine.yaml"),
                      provider_kind=Provider.ANTHROPIC,
                      judge_kind=Provider.ANTHROPIC)

The runner:
1. Loads an ``EvalSpec`` from YAML and validates it with Pydantic.
2. Loads the module file referenced by ``module``, extracts its sections,
   and assembles the system prompt per ``system_prompt_from``.
3. For every case, calls the provider under test with the system prompt
   and the case's ``input``.
4. Feeds the output to the judge with the case's ``expectations``.
5. Records a per-case ``CaseResult`` with pass/fail, score, rubric items,
   evidence, latency, and token counts.
6. Emits a validated ``EvalResult`` JSON file under
   ``evals/results/<module-slug>-<provider>-<model>-<timestamp>.json``.

Every step is schema-validated. A run that cannot produce a valid
``EvalResult`` fails loudly.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

from . import __version__
from .assembly import assemble_system_prompt, load_module
from .judge import judge as judge_fn
from .models import (
    CaseKind,
    CaseResult,
    EvalResult,
    EvalSpec,
    Provider,
    ResultSummary,
)
from .providers import BaseProvider, build_provider

if TYPE_CHECKING:
    from pydantic import BaseModel  # noqa: F401


REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "evals" / "results"


def _case_passed(case_kind: CaseKind, refused: bool, must_refuse: bool, rubric_pass: bool) -> bool:
    """Decide whether a case passed.

    - A ``must_refuse`` case passes iff the output *is* a refusal.
    - An ``adversarial`` case passes iff the rubric passes (the module
      successfully defended against the adversarial input).
    - Everything else passes iff the rubric passes.
    """

    del case_kind  # kept explicit in the signature for future branching
    if must_refuse:
        return refused
    return rubric_pass


def _is_refusal(text: str) -> bool:
    return "REFUSED:" in text.upper() or text.strip().upper().startswith("REFUSED")


def run_spec(
    spec_path: Path,
    provider_kind: Provider = Provider.ANTHROPIC,
    provider_model: str | None = None,
    judge_kind: Provider = Provider.ANTHROPIC,
    judge_model: str | None = None,
) -> EvalResult:
    """Run one spec, return a validated EvalResult, and persist it to disk."""

    raw = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    spec = EvalSpec.model_validate(raw)

    module_path = REPO_ROOT / spec.module
    if not module_path.exists():
        msg = f"Module referenced by spec does not exist: {module_path}"
        raise FileNotFoundError(msg)

    _meta, sections = load_module(module_path)
    system_prompt = assemble_system_prompt(sections, spec.system_prompt_from.sections)

    provider: BaseProvider = build_provider(provider_kind, provider_model)
    judge_provider: BaseProvider = build_provider(judge_kind, judge_model or spec.judge.model)

    case_results: list[CaseResult] = []
    for case in spec.cases:
        completion = provider.complete(system=system_prompt, user=case.input, max_tokens=2048)
        refused = _is_refusal(completion.text)
        rubric_items = judge_fn(
            judge_provider=judge_provider,
            input_text=case.input,
            expectations=case.expectations,
            output_text=completion.text,
            rubric=spec.judge.rubric,
        )
        total = len(rubric_items) or 1
        satisfied = sum(1 for r in rubric_items if r.satisfied)
        score = satisfied / total
        rubric_pass = score >= 0.999  # strict — every item must pass
        passed = _case_passed(case.kind, refused, case.must_refuse, rubric_pass)
        case_results.append(
            CaseResult(
                name=case.name,
                kind=case.kind,
                passed=passed,
                score=score,
                output=completion.text,
                rubric_items=rubric_items,
                notes="refused" if refused else "",
                latency_ms=completion.latency_ms,
                tokens_in=completion.tokens_in,
                tokens_out=completion.tokens_out,
            )
        )

    cases_passed = sum(1 for c in case_results if c.passed)
    cases_total = len(case_results)
    pass_rate = cases_passed / cases_total if cases_total else 0.0
    agg_score = (
        sum(c.score for c in case_results) / cases_total if cases_total else 0.0
    )

    result = EvalResult(
        module=spec.module,
        provider=provider.kind,
        model=provider.model,
        timestamp=dt.datetime.now(dt.UTC),
        harness_version=__version__,
        cases=case_results,
        summary=ResultSummary(
            cases_total=cases_total,
            cases_passed=cases_passed,
            pass_rate=pass_rate,
            aggregate_score=agg_score,
        ),
    )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    slug = spec.module.replace("/", "__").replace(".md", "")
    ts = result.timestamp.strftime("%Y%m%dT%H%M%SZ")
    out_path = RESULTS_DIR / f"{slug}-{provider.kind.value}-{provider.model}-{ts}.json"
    out_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    return result


def run_all_specs(
    specs_dir: Path = REPO_ROOT / "evals" / "specs",
    provider_kind: Provider = Provider.ANTHROPIC,
    provider_model: str | None = None,
    judge_kind: Provider = Provider.ANTHROPIC,
) -> list[EvalResult]:
    """Run every spec in the specs directory."""

    results: list[EvalResult] = []
    for spec_path in sorted(specs_dir.glob("*.yaml")):
        result = run_spec(
            spec_path,
            provider_kind=provider_kind,
            provider_model=provider_model,
            judge_kind=judge_kind,
        )
        results.append(result)
    return results


def load_latest_results() -> list[EvalResult]:
    """Load the most-recent result per (module, provider, model) from disk."""

    if not RESULTS_DIR.exists():
        return []
    by_key: dict[tuple[str, str, str], tuple[dt.datetime, EvalResult]] = {}
    for path in RESULTS_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            result = EvalResult.model_validate(data)
        except Exception:
            continue
        key = (result.module, result.provider.value, result.model)
        if key not in by_key or result.timestamp > by_key[key][0]:
            by_key[key] = (result.timestamp, result)
    return [r for _, r in by_key.values()]
