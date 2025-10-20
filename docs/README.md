# Puhu Documentation

This directory contains the Sphinx documentation for the Puhu package.

## Building the Documentation Locally

### Prerequisites

Install the documentation dependencies:

```bash
pip install -r requirements.txt
```

### Build HTML Documentation

```bash
cd docs
make html
```

The built documentation will be in `build/html/`. Open `build/html/index.html` in your browser to view it.

### Other Build Formats

```bash
# PDF (requires LaTeX)
make latexpdf

# Clean build directory
make clean

# View all available formats
make help
```

## Documentation Structure

- `source/` - ReStructuredText source files
  - `conf.py` - Sphinx configuration
  - `index.rst` - Main documentation page
  - `installation.rst` - Installation guide
  - `quickstart.rst` - Quick start guide
  - `api.rst` - API reference
  - `pillow_compatibility.rst` - Pillow compatibility info
  - `contributing.rst` - Contributing guide
  - `changelog.rst` - Version history
  - `_static/` - Static files (images, CSS, etc.)
  - `_templates/` - Custom Sphinx templates

## ReadTheDocs

The documentation is automatically built and hosted on ReadTheDocs at:
https://puhu.readthedocs.io

## Contributing to Documentation

When contributing to the documentation:

1. Use ReStructuredText (.rst) format
2. Follow the existing structure and style
3. Test your changes locally before committing
4. Update the changelog when appropriate

See `source/contributing.rst` for more details.
