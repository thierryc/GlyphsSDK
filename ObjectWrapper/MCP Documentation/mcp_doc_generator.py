#!/usr/bin/env python3
"""Generate Sphinx-ready reStructuredText for the MCP server.

The generator reads triple-quoted documentation blocks from
``GlyphsApp/__init__.py``. The first block becomes a summary in
``index.rst`` and subsequent blocks are written to individual
``section_*.rst`` files referenced from a ``toctree``.
"""

from __future__ import annotations

import re
from pathlib import Path


def extract_sections(init_path: Path) -> list[str]:
    """Return a list of documentation sections from ``init_path``."""
    content = init_path.read_text(encoding="utf-8")
    return [part.strip() for part in re.findall(r"'''(.*?)'''", content, re.DOTALL)]


def generate_rst() -> None:
    """Write ``index.rst`` and per-section files into ``sphinx/``."""
    root = Path(__file__).resolve().parent
    header = (root / "header.rst.txt").read_text(encoding="utf-8")
    init_file = root.parent / "GlyphsApp" / "__init__.py"
    sections = extract_sections(init_file)
    if not sections:
        raise SystemExit("No documentation blocks found")

    source_dir = root / "sphinx"
    source_dir.mkdir(parents=True, exist_ok=True)

    # first block is the summary
    summary = sections[0]
    toctree = [".. toctree::", "   :maxdepth: 1", ""]
    for i, section in enumerate(sections[1:], start=1):
        name = f"section_{i}"
        (source_dir / f"{name}.rst").write_text(section + "\n", encoding="utf-8")
        toctree.append(f"   {name}")

    index_content = f"{header}\n{summary}\n\n" + "\n".join(toctree) + "\n"
    (source_dir / "index.rst").write_text(index_content, encoding="utf-8")
    print(f"reStructuredText documentation written to {source_dir}")


if __name__ == "__main__":
    generate_rst()
