# image_resizer

Simple tool to create multiple copies of a PNG file.

## Minimum Requirements

* [Python 3.12+](https://www.python.org/downloads/)
* [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Setup

```bash
git clone git@github.com:pythoninthegrass/image_resizer.git
ln -s $(pwd)/image_resizer.py ~/.local/bin/image-resizer
```

## Quickstart

```bash
cd images
λ image-resizer logo.png
Installed 1 package in 2ms
Resizing logo.png using Lanczos algorithm...
Output directory: .
Created: logo_16x16.png (16x16)
Created: logo_32x32.png (32x32)
Created: logo_64x64.png (64x64)
Created: logo_128x128.png (128x128)
Created: logo_512x512.png (512x512)
Completed resizing to 5 sizes
```
