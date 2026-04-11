---
title: "ECA Packaging Notes"
category: "research"
vector: "engineering"
version: "1.1.0"
status: "stable"
origin: "ECA v1.1.0 production stack"
source_file: "docs/Packaging_Notes.md"
source_sha256: "3be5e6682dd23dc599066dd2a9dec70773c299c23655f00410867dc4d6d55f71"
---

# ECA Packaging Notes

> *Source: `docs/Packaging_Notes.md` — ECA Cognitive Engine v1.1.0 production stack. Content preserved byte-for-byte; this page is a prompt-x-lab native wrapper with frontmatter + audit metadata.*

````
# Packaging Notes

## Delivery options
1. Encrypted server-side deployment
2. Internal API container
3. Tenant-isolated enterprise deployment

## Do not ship publicly
- canonical prompt in plaintext
- internal policy bundle without access control
- signing secrets
- hidden eval sets

## Ship to clients
- operational manual
- input guide
- policy summary
- release notes
- agreed templates
````


---

*Integrated into prompt-x-lab as layer `06_eca_engine/` on 2026-04-11. See [`../README.md`](../README.md) for the full layer description and [`../../src/pxl/eca/`](../../src/pxl/eca/) for the typed Python subsystem (router · scorer · signer · validate).*
