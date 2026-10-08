#!/usr/bin/env python3
"""Batch File Renamer - CLI & Argument Parser.

A flexible utility for developers to standardize file names across directories
using prefixes, suffixes, date tags, text replacement, and sequence padding.
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


def get_target_files(directory: Path, extension_filter: str | None = None) -> list[Path]:
    """Retrieve all files in the target directory (excluding subdirectories and hidden files)."""
    if not directory.exists() or not directory.is_dir():
        raise ValueError(f"Target directory does not exist or is not a directory: {directory}")

    files: list[Path] = []
    for item in sorted(directory.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        if extension_filter:
            ext = extension_filter if extension_filter.startswith(".") else f".{extension_filter}"
            if item.suffix.lower() != ext.lower():
                continue
        files.append(item)
    return files


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Batch rename files using prefix, suffix, date, replace, or sequence padding."
    )
    parser.add_argument(
        "-d",
        "--dir",
        type=Path,
        required=True,
        help="Path to the directory containing files to rename",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        default="",
        help="Prefix string to prepend to filenames",
    )
    parser.add_argument(
        "-s",
        "--suffix",
        type=str,
        default="",
        help="Suffix string to append before file extension",
    )
    parser.add_argument(
        "--date-prefix",
        action="store_true",
        help="Prepend current date (YYYY-MM-DD_) to filenames",
    )
    parser.add_argument(
        "--replace",
        type=str,
        default=None,
        help="Target substring to search and replace in filenames",
    )
    parser.add_argument(
        "--with-text",
        type=str,
        default="",
        help="Replacement text to use with --replace (default: empty string)",
    )
    parser.add_argument(
        "--sequence",
        action="store_true",
        help="Append zero-padded sequence numbers (e.g. _001, _002)",
    )
    parser.add_argument(
        "--filter-ext",
        type=str,
        default=None,
        help="Optional file extension filter to process only matching files (e.g. .jpg or png)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate rename operations without modifying actual files",
    )
    return parser.parse_args()


def main() -> None:
    """Script entry point."""
    args = parse_arguments()

    try:
        files = get_target_files(args.dir, extension_filter=args.filter_ext)
    except Exception as exc:
        print(f"❌ Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if not files:
        print(f"⚠️ No matching files found in: {args.dir.resolve()}")
        return

    print(f"📂 Target Directory: {args.dir.resolve()}")
    print(f"🔍 Discovered {len(files)} file(s) to process.")
    if args.dry_run:
        print("🔍 DRY RUN MODE enabled - No files will be renamed.\n")


if __name__ == "__main__":
    main()

