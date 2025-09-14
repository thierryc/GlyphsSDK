#!/usr/bin/env python3
"""Generate Sphinx-ready reStructuredText for the MCP server.

This script extracts triple-quoted documentation blocks from
``GlyphsApp/__init__.py`` and prepends a header template so the
resulting file can be built by Sphinx into HTML or other formats.
"""

from __future__ import annotations

import re
from pathlib import Path


def extract_sections(init_path: Path) -> str:
    """Return concatenated documentation sections from ``init_path``."""
    content = init_path.read_text(encoding="utf-8")
    parts = re.findall(r"'''(.*?)'''", content, re.DOTALL)
    return "\n".join(part.strip() for part in parts)


def generate_rst() -> None:
    """Write ``index.rst`` based on the header and extracted sections."""
    root = Path(__file__).resolve().parent
    header = (root / "header.rst.txt").read_text(encoding="utf-8")
    init_file = root.parent / "GlyphsApp" / "__init__.py"
    doc = extract_sections(init_file)

    source_dir = root / "sphinx"
    source_dir.mkdir(parents=True, exist_ok=True)
    index_path = source_dir / "index.rst"
    index_path.write_text(f"{header}\n{doc}\n", encoding="utf-8")
    print(f"reStructuredText documentation written to {index_path}")


if __name__ == "__main__":
    generate_rst()
