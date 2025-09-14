#!/usr/bin/env python3
"""Generate reStructuredText documentation for the MCP server.

This script draws inspiration from ``code2sphinx.py`` but focuses on
producing `.rst` files using ``sphinx.ext.apidoc`` so the output can be
consumed directly or further processed into other formats.
"""

from __future__ import annotations

from pathlib import Path

from sphinx.ext.apidoc import main as apidoc_main


def generate_rst() -> None:
    """Create ``.rst`` files for the MCP server API."""
    root = Path(__file__).resolve().parent
    output_dir = root / "rst"
    package_dir = root.parent / "GlyphsApp"
    output_dir.mkdir(parents=True, exist_ok=True)

    apidoc_main(["-o", str(output_dir), str(package_dir)])
    print(f"reStructuredText documentation written to {output_dir}")


if __name__ == "__main__":
    generate_rst()
