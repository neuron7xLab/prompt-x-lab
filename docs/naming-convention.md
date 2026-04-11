# Naming Convention

## Filename format

```
[category]-[vector]-[version].md
```

- **`category`** — the layer directory, without the numeric prefix: `foundation`, `cognition`, `engineering`, `personas`, `validation`.
- **`vector`** — one of: `cognitive`, `engineering`, `strategic`, `creative`, `validation`.
- **`version`** — SemVer. Bump major on breaking changes; minor on additive extensions; patch on wording fixes.

However, **short, descriptive filenames are preferred** when they are already unambiguous. `executive-engine.md` is clearer than `cognition-cognitive-v1.md`. The fully-qualified form is used only when needed to disambiguate.

## Module titles

- Title case.
- Noun or noun-phrase. Never a verb phrase.
- No emoji, no punctuation beyond dashes.

**Good:** `Senior Code Reviewer`, `Hallucination Gate`, `Executive Engine`
**Bad:** `Reviews your code like a senior!`, `🔍 Code Reviewer`, `Reviewing Code (v1)`

## Version bumping rules

- **Major bump** (`1.0.0 → 2.0.0`): the module's output shape changes, or its refusal conditions change, or its identity block changes. Users of the old version cannot drop-in swap.
- **Minor bump** (`1.0.0 → 1.1.0`): a new test prompt, a new edge case handled, a new constraint added that does not break existing usage.
- **Patch bump** (`1.0.0 → 1.0.1`): wording clarifications, typo fixes, example improvements.

## Deprecation

When a module is superseded:

1. Add `status: deprecated` to the frontmatter.
2. Add a `Deprecated:` line at the top of the body pointing to the replacement.
3. Do not delete the file — it may still be referenced by older composites.
4. Update `.metadata/manifest.yaml` to reflect the new status.

## Directory depth

Two levels max: `{layer}/{module}.md`. If a layer starts needing subdirectories, it's a signal that the layer is doing two jobs and should be split at the top level.
