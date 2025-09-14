# MCP Documentation

This directory contains tools for building HTML documentation for the MCP server.

## Requirements

- [Sphinx](https://www.sphinx-doc.org/)
- Python 3.8+

## Usage

1. Place your Sphinx source files in the `sphinx` subdirectory.
2. Run the generator:

   ```bash
   python mcp_doc_generator.py
   ```

The generated HTML will be placed in `_build/html`.

The script uses the current Python interpreter and `subprocess.run` for a simple and portable build step.
