#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "Pillow>=11.3.0",
# ]
# [tool.uv]
# exclude-newer = "2025-08-31T00:00:00Z"
# ///

# pyright: reportMissingImports=false

"""
PNG Lanczos Resizer
A self-contained Python application that resizes PNG images using Lanczos compression
to multiple predefined sizes: 16x16, 32x32, 64x64, 128x128, 512x512
"""

import sys
import argparse
from pathlib import Path
from PIL import Image
from textwrap import dedent
from typing import List, Tuple


class PNGLanczosResizer:
    """Handles PNG image resizing using Lanczos algorithm"""

    DEFAULT_SIZES = [(16, 16), (32, 32), (64, 64), (128, 128), (512, 512)]

    def __init__(
        self,
        input_path: str,
        output_dir: str = None,
        sizes: List[Tuple[int, int]] = None,
    ):
        """
        Initialize the resizer

        Args:
            input_path: Path to input PNG file
            output_dir: Directory to save resized images (default: same as input)
            sizes: List of (width, height) tuples for output sizes
        """
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir) if output_dir else self.input_path.parent
        self.sizes = sizes or self.DEFAULT_SIZES

        self._validate_input()

    def _validate_input(self) -> None:
        """Validate input file and create output directory if needed"""
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_path}")

        if not self.input_path.suffix.lower() == ".png":
            raise ValueError("Input file must be a PNG image")

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _generate_output_filename(self, size: Tuple[int, int]) -> Path:
        """Generate output filename based on size"""
        stem = self.input_path.stem
        width, height = size
        return self.output_dir / f"{stem}_{width}x{height}.png"

    def resize_image(self, size: Tuple[int, int]) -> None:
        """
        Resize image to specified size using Lanczos algorithm

        Args:
            size: Target (width, height) tuple
        """
        try:
            with Image.open(self.input_path) as img:
                # Convert to RGBA if not already (preserves transparency)
                if img.mode != "RGBA":
                    img = img.convert("RGBA")

                # Resize using Lanczos algorithm
                resized_img = img.resize(size, Image.Resampling.LANCZOS)

                # Generate output path
                output_path = self._generate_output_filename(size)

                # Save with PNG compression
                resized_img.save(output_path, "PNG", optimize=True, compress_level=9)

                print(f"Created: {output_path} ({size[0]}x{size[1]})")

        except Exception as e:
            print(f"Error resizing to {size}: {e}")

    def resize_all(self) -> None:
        """Resize image to all specified sizes"""
        print(f"Resizing {self.input_path} using Lanczos algorithm...")
        print(f"Output directory: {self.output_dir}")

        for size in self.sizes:
            self.resize_image(size)

        print(f"Completed resizing to {len(self.sizes)} sizes")

    def get_original_dimensions(self) -> Tuple[int, int]:
        """Get dimensions of original image"""
        with Image.open(self.input_path) as img:
            return img.size


def parse_size_string(size_str: str) -> Tuple[int, int]:
    """Parse size string like '64x64' into tuple"""
    try:
        width, height = map(int, size_str.lower().split("x"))
        return (width, height)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid size format: {size_str}. Use format: WIDTHxHEIGHT"
        )


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Resize PNG images using Lanczos compression",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent("""
            Examples:
              %(prog)s input.png
              %(prog)s input.png -o resized/
              %(prog)s input.png -s 64x64 128x128 256x256
              %(prog)s input.png -o output/ -s 48x48 96x96
            """),
    )

    parser.add_argument("input", help="Input PNG file path")

    parser.add_argument(
        "-o",
        "--output",
        help="Output directory (default: same as input file)",
        default=None,
    )

    parser.add_argument(
        "-s",
        "--sizes",
        nargs="+",
        type=parse_size_string,
        help="Custom sizes in WIDTHxHEIGHT format (default: 16x16 32x32 64x64 128x128 512x512)",
        default=None,
    )

    parser.add_argument(
        "--info", action="store_true", help="Show original image dimensions"
    )

    # Show help and exit with 0 if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    try:
        resizer = PNGLanczosResizer(
            input_path=args.input, output_dir=args.output, sizes=args.sizes
        )

        if args.info:
            original_size = resizer.get_original_dimensions()
            print(f"Original dimensions: {original_size[0]}x{original_size[1]}")

        resizer.resize_all()

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
