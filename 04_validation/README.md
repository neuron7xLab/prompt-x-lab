# 04 — Validation

Output-gate modules. These sit at the end of a pipeline and reject bad output rather than producing good output.

| Module | Purpose |
| --- | --- |
| [`hallucination-gate.md`](hallucination-gate.md) | Refuse any claim not backed by the provided context. |
| [`logical-fallacy-checker.md`](logical-fallacy-checker.md) | Audit an argument against a named taxonomy of fallacies. |

Validation modules are composed as wrappers: run the primary module, then pipe its output through one or more validation gates. If any gate rejects, the whole response is refused.
