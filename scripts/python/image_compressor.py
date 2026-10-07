#!/usr/bin/env python3
"""Image Compressor for Web Optimization - CLI & Scanner.

A batch image compression and optimization utility for developers to reduce image
file sizes prior to deploying to the web.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure UTF-8 output encoding across all operating systems and shells
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# Set of recognized image file extensions
SUPPORTED_EXTENSIONS: set[str] = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tiff",
}


def find_image_files(input_path: Path) -> list[Path]:
    """Discover all supported image files from a file path or directory."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")

    if input_path.is_file():
        if input_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            return [input_path]
        return []

    # If it is a directory, find all files with supported extensions (non-recursive)
    images: list[Path] = []
    for item in sorted(input_path.iterdir()):
        if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
            images.append(item)
    return images


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Batch compress images for web optimization while preserving originals."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="Path to an image file or directory containing images to compress",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output directory to save compressed images (default: <input>/compressed)",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=80,
        help="Compression quality from 1 to 100 (default: 80)",
    )
    return parser.parse_args()


def main() -> None:
    """Script entry point."""
    args = parse_arguments()

    if not 1 <= args.quality <= 100:
        print("❌ Error: Quality must be an integer between 1 and 100.", file=sys.stderr)
        sys.exit(1)

    try:
        images = find_image_files(args.input)
    except Exception as exc:
        print(f"❌ Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if not images:
        print(f"⚠️ No supported images found in: {args.input}")
        return

    output_dir = args.output if args.output else (
        args.input.parent / "compressed" if args.input.is_file() else args.input / "compressed"
    )

    print(f"🔍 Found {len(images)} image(s) to process.")
    print(f"📂 Output directory: {output_dir.resolve()}")
    print(f"⚙️ Target quality: {args.quality}%")


if __name__ == "__main__":
    main()

