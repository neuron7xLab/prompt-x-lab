"""``python -m pxl`` — module entry point that delegates to ``pxl.main``."""

from __future__ import annotations

from .main import entrypoint

if __name__ == "__main__":
    raise SystemExit(entrypoint())
