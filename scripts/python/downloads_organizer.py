#!/usr/bin/env python3
"""Downloads Organizer - Core Engine.

A modular automation script that organizes files into categorized subdirectories
based on file extensions. Supports custom paths, duplicate renaming, and dry-run mode.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
import shutil


# Mapping categories to sets of file extensions (extensions with leading dot, lowercased).
CATEGORY_EXTENSIONS: dict[str, set[str]] = {
    "Documents": {
        ".pdf",
        ".docx",
        ".doc",
        ".txt",
        ".xlsx",
        ".xls",
        ".pptx",
        ".ppt",
        ".csv",
        ".odt",
        ".ods",
        ".odp",
        ".rtf",
        ".md",
    },
}


def get_default_downloads_dir() -> Path:
    """Return the default Downloads directory for the current operating system."""
    return Path.home() / "Downloads"


def get_unique_destination_path(target_folder: Path, original_filename: str) -> Path:
    """Generate a collision-safe destination file path.

    If a file with the same name already exists in target_folder,
    appends a numeric counter: 'file (1).ext', 'file (2).ext', etc.
    """
    destination = target_folder / original_filename
    if not destination.exists():
        return destination

    stem = Path(original_filename).stem
    suffix = Path(original_filename).suffix
    counter = 1

    while True:
        new_name = f"{stem} ({counter}){suffix}"
        candidate = target_folder / new_name
        if not candidate.exists():
            return candidate
        counter += 1


def get_category_for_extension(extension: str) -> str | None:
    """Determine the matching category for a given file extension."""
    ext = extension.lower()
    for category, extensions in CATEGORY_EXTENSIONS.items():
        if ext in extensions:
            return category
    return None


def organize_directory(directory: Path, dry_run: bool = False) -> dict[str, int]:
    """Scan the directory and organize files into categorized subfolders."""
    if not directory.exists() or not directory.is_dir():
        raise ValueError(f"Target path does not exist or is not a directory: {directory}")

    results: dict[str, int] = {cat: 0 for cat in CATEGORY_EXTENSIONS}
    results["Skipped"] = 0

    print(f"\n📂 Scanning directory: {directory.resolve()}")
    if dry_run:
        print("🔍 DRY RUN MODE enabled - No files will be moved.\n")

    # Only process items directly under target folder (skip subfolders)
    for item in directory.iterdir():
        # Skip subfolders, hidden files, and temporary downloads
        if not item.is_file():
            continue
        if item.name.startswith(".") or item.suffix.lower() in {".crdownload", ".part", ".tmp"}:
            continue

        category = get_category_for_extension(item.suffix)
        if not category:
            results["Skipped"] += 1
            continue

        category_folder = directory / category
        destination_path = get_unique_destination_path(category_folder, item.name)

        if dry_run:
            print(f"[DRY RUN] Would move: {item.name} -> {category}/{destination_path.name}")
        else:
            category_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(destination_path))
            print(f"[MOVED] {item.name} -> {category}/{destination_path.name}")

        results[category] = results.get(category, 0) + 1

    return results


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Organize files into categorized subfolders based on file extensions."
    )
    parser.add_argument(
        "-p",
        "--path",
        type=Path,
        default=None,
        help="Custom target directory path to organize (defaults to ~/Downloads)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the organization process without actually moving any files",
    )
    return parser.parse_args()


def main() -> None:
    """Script entry point."""
    args = parse_arguments()
    target_dir = args.path if args.path else get_default_downloads_dir()

    try:
        results = organize_directory(target_dir, dry_run=args.dry_run)
    except Exception as exc:
        print(f"❌ Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print("\n📊 Summary:")
    moved_total = sum(count for cat, count in results.items() if cat != "Skipped")
    for category, count in results.items():
        if count > 0:
            print(f"  - {category}: {count} file(s)")
    print(f"Total organized files: {moved_total}")


if __name__ == "__main__":
    main()

