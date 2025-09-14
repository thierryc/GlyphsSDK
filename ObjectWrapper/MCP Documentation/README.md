# MCP Documentation

This directory contains tools for building reStructuredText documentation for the MCP server.
The generator reads documentation blocks from ``../GlyphsApp/__init__.py``
and writes a Sphinx source tree.

## Requirements

- Python 3.8+
- [Sphinx](https://www.sphinx-doc.org/) (see `requirements.txt`)

## Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Usage

Extract documentation and build the Sphinx source directory:

```bash
python mcp_doc_generator.py
```

The script creates a ``sphinx/`` directory containing ``index.rst``. To build
HTML from this source, run:

```bash
python -m sphinx -b html sphinx sphinx/_build/html
```

The generated files in ``sphinx/`` and ``sphinx/_build/html`` are ignored by
git.
