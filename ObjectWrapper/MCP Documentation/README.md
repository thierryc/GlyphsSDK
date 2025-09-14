# MCP Documentation

This directory contains tools for building reStructuredText documentation for the MCP server.

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

Generate `.rst` files from the `GlyphsApp` package:

```bash
python mcp_doc_generator.py
```

The resulting reStructuredText files are written to the `rst/` directory. These
files can be consumed directly by an MCP server or further processed by Sphinx
into other formats such as HTML or PDF.
