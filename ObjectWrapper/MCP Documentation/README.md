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

The first documentation block becomes a summary in ``sphinx/index.rst``.
Each subsequent block is written to its own ``section_*.rst`` file and
referenced from a ``toctree`` in the index. Only the ``sphinx/`` folder is
needed for the MCP server. To build HTML from this source, run:

```bash
python -m sphinx -b html sphinx sphinx/_build/html
```

Only ``sphinx/_build`` is ignored by git so the source ``.rst`` files remain
available for documentation retrieval.
