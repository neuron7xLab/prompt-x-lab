# Contributing to prompt-x-lab

prompt-x-lab treats prompts as **engineering artifacts**: typed, versioned, tested, composable, falsifiable. Contributions that do not respect that discipline are rejected, regardless of how well-intentioned they are.

This document describes how to contribute well. If something here conflicts with [`CLAUDE.md`](CLAUDE.md) — which contains the non-negotiable development rules — **CLAUDE.md wins**.

---

## Non-negotiable rules

1. **Every seed module has valid frontmatter.** Pydantic schema. `pxl-validate` must pass.
2. **Every seed module has an eval spec.** No exceptions for layers 01–04.
3. **Every seed module cites its prior art.** Either `docs/references.bib` or a concrete prior incident. Unanchored claims are inadmissible.
4. **The `validated` frontmatter field is written only by the eval harness.** Never by hand.
5. **Layer-05, 06, 07 bodies are immutable.** Any change must be accompanied by a regenerated `AUDIT.sha256` and a rationale in the commit message.
6. **Every badge is computed from real data.** Aspirational claims are forbidden.
7. **The full quality gate (`make all`) must be green locally before pushing.**

---

## Full quality gate

```bash
make install-dev          # one-time
make all                  # run all checks
```

`make all` is:

| Step | Command | Proves |
|---|---|---|
| 1 | `pxl-validate` | All 91 module files conform to frontmatter schema. |
| 2 | `pytest -q` | All 117 tests pass (including hypothesis property tests). |
| 3 | `ruff check` | Style, imports, complexity. |
| 4 | `mypy --strict` | 27 source files type-check. |
| 5 | `python -m pxl.audit verify` | Layer 05/06/07 body hashes match. |
| 6 | `pxl-eca validate` | ECA full-corpus replay (router 99.44% · scorer 90.62% · FP=0). |
| 7 | `pxl-kriterion benchmark` | 10/10 canonical-hash fixtures match upstream. |

If any step fails, **do not push**. Fix the cause, not the symptom.

---

## How to add a new seed module (layers 00–04)

```bash
# 1. Copy the template
cp templates/base-module.md 02_engineering/my-module.md

# 2. Fill in frontmatter (title, category, vector, version 1.0.0, status draft)
$EDITOR 02_engineering/my-module.md

# 3. Validate
pxl-validate

# 4. Write the eval spec
$EDITOR evals/specs/my-module.yaml

# 5. Add a prior-art anchor to docs/references.bib

# 6. Test locally (mock mode is fine without API keys)
pxl-eval --spec evals/specs/my-module.yaml --provider mock --judge-provider mock

# 7. Full gate
make all

# 8. Commit
git add 02_engineering/my-module.md evals/specs/my-module.yaml docs/references.bib
git commit -m "feat(02_engineering): add my-module"
```

---

## How to add a new `pxl.*` Python module

1. Write the module under `src/pxl/`.
2. Add a docstring at the top explaining the module's single responsibility.
3. Full type annotations (`mypy --strict` clean).
4. Add unit tests in `tests/test_<module>.py` targeting **≥ 90% coverage**.
5. If the module accepts JSON-serialisable inputs, use `typing.Any` but add a `per-file-ignore` for `ANN401` in `pyproject.toml` — Any is the honest type for external data boundaries.
6. Run `make all`.
7. Update the public API in `src/pxl/__init__.py` if the module is user-facing.

---

## How to update a bundled asset (layer 05, 06, 07)

Layer-05, 06, and 07 content is **immutable** by default. If you *must* change a body:

1. Verify the change is authorised (upstream license allows it).
2. Edit the file.
3. Regenerate the audit: `python -m pxl.audit write`.
4. Commit both the content change and the updated `AUDIT.sha256` **in the same commit**.
5. In the commit message, state the rationale and cite the upstream source.

CI will fail on any content change that is not accompanied by a matching audit update. This is enforced by `make audit-verify`.

---

## Version bump rules

| Change | Bump | Example |
|---|---|---|
| Wording, typos, clarifications | **patch** | `1.0.0 → 1.0.1` |
| New test case, new constraint (additive) | **minor** | `1.0.0 → 1.1.0` |
| Output shape, refusal conditions, identity change | **major** | `1.0.0 → 2.0.0` |

Major bumps require a new filename: `my-module.md` → `my-module-v2.md`. The old file is marked `status: deprecated` and points to the replacement. Old dependents keep working.

---

## Style

- Declarative, slightly clinical tone. No emoji in source code or committed docs.
- Bullets ≤ 3 lines each.
- Module docstrings explain *why the module exists*, not just *what it does*.
- Prefer frozen dataclasses + pure functions over classes with mutable state.
- Public API in `__init__.py`. Everything else is underscore-prefixed.

When in doubt, read `02_engineering/senior-code-reviewer.md` and match its register.

---

## License of contributions

By submitting a contribution, you agree that your code is licensed under the MIT License (same as the prompt-x-lab packaging). Integrated upstream content retains its upstream license — do not submit derived works of layer-05/06/07 bodies without clearing them with the upstream author.

---

## Credits

Contributors are credited in `CHANGELOG.md` under the version in which their change landed. Security reporters are credited under the `### Security` subsection.

---

*This project is a discipline, not a catalog. Every contribution earns its place.*
