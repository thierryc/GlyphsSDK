#!/usr/bin/env python3
"""
Generate documentation for the MCP server using Sphinx.

This script mirrors the functionality of the original
`code2sphinx.py` but uses modern Python features for clarity
and reliability.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def build_docs() -> None:
    """Build HTML documentation using Sphinx."""
    root = Path(__file__).resolve().parent
    source_dir = root / "sphinx"
    build_dir = root / "_build" / "html"
    build_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "html",
        str(source_dir),
        str(build_dir),
    ]
    subprocess.run(cmd, check=True)

    print(f"Documentation built at {build_dir}")


if __name__ == "__main__":
    build_docs()
