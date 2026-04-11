# prompt-x-lab — engineering targets
#
# All targets are idempotent and safe to run in CI. Nothing here reaches
# outside the repository except `make eval` (optional, needs API keys).

PY       ?= python3
VENV     ?= .venv
VENV_PY  := $(VENV)/bin/python
VENV_PIP := $(VENV)/bin/pip

.PHONY: help venv install install-dev validate test lint format \
        eval eval-mock audit audit-write audit-verify badges \
        eca-info eca-validate \
        kriterion-info kriterion-benchmark \
        all clean distclean ci

help: ## Show this help
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

venv: $(VENV_PY) ## Create .venv if missing

$(VENV_PY):
	$(PY) -m venv $(VENV)
	$(VENV_PIP) install --upgrade pip

install: venv ## Install runtime deps (pydantic, pyyaml, jsonschema, frontmatter)
	$(VENV_PIP) install -e '.'

install-dev: venv ## Install runtime + dev + eval extras
	$(VENV_PIP) install -e '.[dev,eval]'

validate: venv ## Validate every module's frontmatter against schema
	$(VENV_PY) -m pxl.cli_validate 2>/dev/null || $(VENV)/bin/pxl-validate

test: venv ## Run pytest
	$(VENV_PY) -m pytest -q

lint: venv ## Ruff check
	$(VENV_PY) -m ruff check src scripts evals tests

format: venv ## Ruff format
	$(VENV_PY) -m ruff format src scripts evals tests

typecheck: venv ## mypy --strict on src/
	$(VENV_PY) -m mypy src

eval: venv ## Run every eval spec against Claude Opus (requires ANTHROPIC_API_KEY)
	$(VENV)/bin/pxl-eval --provider anthropic --judge-provider anthropic

eval-mock: venv ## Run every eval spec in mock mode (no API keys needed)
	$(VENV)/bin/pxl-eval --provider mock --judge-provider mock

audit-write: venv ## Recompute Layer 05 SHA256 audit manifest
	$(VENV_PY) -m pxl.audit write

audit-verify: venv ## Verify Layer 05 has not drifted
	$(VENV_PY) -m pxl.audit verify

audit: audit-verify ## Default audit target = verify

badges: venv ## Compute real badge values from evaluation results
	$(VENV)/bin/pxl-badges

eca-info: venv ## Print ECA bundled config + calibration summary
	$(VENV)/bin/pxl-eca info

eca-validate: venv ## Replay ECA calibration holdouts (reproduces published metrics)
	$(VENV)/bin/pxl-eca validate

kriterion-info: venv ## Print Kriterion version + bundled schemas + protocols
	$(VENV)/bin/pxl-kriterion info

kriterion-benchmark: venv ## Reproduce Kriterion 10-case manifest-hash benchmark
	$(VENV)/bin/pxl-kriterion benchmark

all: validate test lint typecheck audit-verify eca-validate kriterion-benchmark ## Full local check

ci: all ## Exactly what CI runs

clean: ## Remove caches
	rm -rf .mypy_cache .ruff_cache .pytest_cache evals/results/.tmp-*
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

distclean: clean ## Also drop the venv
	rm -rf $(VENV)
