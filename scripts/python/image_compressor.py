#!/usr/bin/env python3
"""Image Compressor for Web Optimization - CLI & Scanner.

A batch image compression and optimization utility for developers to reduce image
file sizes prior to deploying to the web.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

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


def compress_image(
    input_file: Path,
    destination_file: Path,
    quality: int = 80,
    to_webp: bool = False,
    max_width: int | None = None,
) -> tuple[int, int]:
    """Compress a single image file with the requested quality.

    Returns:
        tuple[int, int]: (original_size_bytes, compressed_size_bytes)
    """
    destination_file.parent.mkdir(parents=True, exist_ok=True)
    original_size = input_file.stat().st_size

    with Image.open(input_file) as img:
        # Optional resizing preserving aspect ratio
        if max_width and img.width > max_width:
            new_height = int(img.height * (max_width / img.width))
            resample_filter = getattr(Image, "Resampling", Image).LANCZOS
            img = img.resize((max_width, new_height), resample_filter)

        if to_webp:
            # WebP natively supports both RGB and transparent RGBA
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA" if "transparency" in img.info else "RGB")
            img.save(destination_file, format="WEBP", quality=quality, method=6)
        else:
            ext = destination_file.suffix.lower()
            save_format = "JPEG" if ext in {".jpg", ".jpeg"} else "PNG" if ext == ".png" else img.format

            if save_format == "JPEG" and img.mode in ("RGBA", "LA", "P"):
                rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                rgb_img.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
                rgb_img.save(destination_file, format="JPEG", quality=quality, optimize=True)
            elif save_format == "PNG":
                img.save(destination_file, format="PNG", optimize=True)
            else:
                img.save(destination_file, quality=quality, optimize=True)

    compressed_size = destination_file.stat().st_size
    return original_size, compressed_size


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
    parser.add_argument(
        "--to-webp",
        action="store_true",
        help="Convert processed images to modern WebP format (.webp)",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=None,
        help="Optionally resize images to a maximum width (maintains aspect ratio)",
    )
    return parser.parse_args()


def main() -> None:
    """Script entry point."""
    args = parse_arguments()

    if not 1 <= args.quality <= 100:
        print("❌ Error: Quality must be an integer between 1 and 100.", file=sys.stderr)
        sys.exit(1)

    if args.max_width is not None and args.max_width <= 0:
        print("❌ Error: --max-width must be a positive integer.", file=sys.stderr)
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
    if args.to_webp:
        print("🌐 Format conversion: WebP enabled")
    if args.max_width:
        print(f"📐 Max width constraint: {args.max_width}px")
    print()

    for image_path in images:
        destination_name = f"{image_path.stem}.webp" if args.to_webp else image_path.name
        destination = output_dir / destination_name
        try:
            orig, comp = compress_image(
                image_path,
                destination,
                quality=args.quality,
                to_webp=args.to_webp,
                max_width=args.max_width,
            )
            saved = orig - comp
            saved_percent = (saved / orig * 100) if orig > 0 else 0
            print(f"[OK] {image_path.name} -> {destination.name}: {orig}B -> {comp}B ({saved_percent:.1f}% saved)")
        except Exception as exc:
            print(f"[ERROR] Failed {image_path.name}: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()

