# 03 — Personas

Specialized interactive agents for domain tasks. Personas are stateful over a conversation — they maintain a voice, a disposition, and a refusal policy.

| Module | Purpose |
| --- | --- |
| [`socratic-tutor.md`](socratic-tutor.md) | Teach by asking, not telling. |
| [`strategic-advisor.md`](strategic-advisor.md) | No-BS executive counsel for high-stakes decisions. |

Personas inherit from `00_foundation/identity-primitive.md` and typically wrap a validation gate from `04_validation/`.
