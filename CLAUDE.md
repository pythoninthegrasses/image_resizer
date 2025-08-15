# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a self-contained PNG image resizer that uses Lanczos compression. It's implemented as a single Python script using `uv` for dependency management.

## Commands

### Running the Application

```bash
# Basic usage - resizes to all default sizes (16x16, 32x32, 64x64, 128x128, 512x512)
./image_resizer.py input.png

# Custom output directory
./image_resizer.py input.png -o resized/

# Custom sizes
./image_resizer.py input.png -s 48x48 96x96 256x256

# Show original dimensions
./image_resizer.py input.png --info
```

### Development

```bash
# Format code (using ruff as per global CLAUDE.md)
ruff format image_resizer.py

# Check formatting
ruff format --check --diff image_resizer.py
```

## Architecture

The application is structured as a single-file CLI tool with:

- **PNGLanczosResizer class**: Core resizing logic
  - Input validation and output directory management
  - Image resizing with transparency preservation (RGBA conversion)
  - PNG optimization with maximum compression (level 9)
  
- **CLI Interface**: argparse-based with support for:
  - Custom output directory (-o/--output)
  - Custom sizes (-s/--sizes in WIDTHxHEIGHT format)
  - Image info display (--info)

## Key Implementation Details

- Uses PEP 723 inline script metadata for dependencies
- Requires Python >=3.12 and Pillow >=11.3.0
- Default output sizes: 16x16, 32x32, 64x64, 128x128, 512x512
- Output filenames follow pattern: `{original_name}_{width}x{height}.png`
