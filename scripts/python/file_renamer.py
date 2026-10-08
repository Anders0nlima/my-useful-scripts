#!/usr/bin/env python3
"""Batch File Renamer - CLI & Argument Parser.

A flexible utility for developers to standardize file names across directories
using prefixes, suffixes, date tags, text replacement, and sequence padding.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 output encoding across all operating systems and shells
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def compute_new_filename(
    original_path: Path,
    index: int = 1,
    total_count: int = 1,
    prefix: str = "",
    suffix: str = "",
    date_prefix: bool = False,
    replace_target: str | None = None,
    replace_with: str = "",
    sequence: bool = False,
) -> str:
    """Compute the transformed filename according to formatting rules."""
    stem = original_path.stem
    ext = original_path.suffix

    if replace_target is not None:
        stem = stem.replace(replace_target, replace_with)

    if sequence:
        pad_width = max(3, len(str(total_count)))
        stem = f"{stem}_{index:0{pad_width}d}"

    if prefix:
        stem = f"{prefix}{stem}"

    if date_prefix:
        today_prefix = datetime.now().strftime("%Y-%m-%d_")
        stem = f"{today_prefix}{stem}"

    if suffix:
        stem = f"{stem}{suffix}"

    return f"{stem}{ext}"


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


class RenameOperation:
    """Represents a planned rename operation with safety status."""

    def __init__(self, source: Path, destination: Path, status: str, message: str = ""):
        self.source = source
        self.destination = destination
        self.status = status  # 'RENAME', 'UNCHANGED', 'CONFLICT'
        self.message = message


def plan_rename_operations(
    files: list[Path],
    args: argparse.Namespace,
) -> list[RenameOperation]:
    """Calculate and validate planned rename operations, checking for name collisions."""
    operations: list[RenameOperation] = []
    seen_destinations: dict[Path, Path] = {}
    total_files = len(files)

    for index, file_path in enumerate(files, start=1):
        new_name = compute_new_filename(
            file_path,
            index=index,
            total_count=total_files,
            prefix=args.prefix,
            suffix=args.suffix,
            date_prefix=args.date_prefix,
            replace_target=args.replace,
            replace_with=args.with_text,
            sequence=args.sequence,
        )
        dest_path = file_path.parent / new_name

        if dest_path == file_path:
            operations.append(RenameOperation(file_path, dest_path, "UNCHANGED", "No change required"))
            continue

        if dest_path in seen_destinations:
            conflict_file = seen_destinations[dest_path]
            operations.append(
                RenameOperation(
                    file_path,
                    dest_path,
                    "CONFLICT",
                    f"Destination conflict with '{conflict_file.name}'",
                )
            )
            continue

        if dest_path.exists():
            operations.append(
                RenameOperation(
                    file_path,
                    dest_path,
                    "CONFLICT",
                    f"Destination file '{dest_path.name}' already exists on disk",
                )
            )
            continue

        seen_destinations[dest_path] = file_path
        operations.append(RenameOperation(file_path, dest_path, "RENAME"))

    return operations


def main() -> None:
    """Script entry point."""
    args = parse_arguments()

    has_rules = any([
        args.prefix,
        args.suffix,
        args.date_prefix,
        args.replace is not None,
        args.sequence,
    ])
    if not has_rules:
        print(
            "⚠️ No renaming rules specified (use --prefix, --suffix, --date-prefix, --replace, or --sequence).",
            file=sys.stderr,
        )
        sys.exit(1)

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
    else:
        print()

    operations = plan_rename_operations(files, args)

    conflicts = [op for op in operations if op.status == "CONFLICT"]
    if conflicts:
        print(f"❌ Detected {len(conflicts)} conflict(s). Aborting to prevent data loss:\n", file=sys.stderr)
        for conflict in conflicts:
            print(f"  - {conflict.source.name} -> {conflict.destination.name}: {conflict.message}", file=sys.stderr)
        sys.exit(1)

    renamed_count = 0
    unchanged_count = 0

    for op in operations:
        if op.status == "UNCHANGED":
            unchanged_count += 1
            print(f"[UNCHANGED] {op.source.name}")
        elif args.dry_run:
            renamed_count += 1
            print(f"[DRY RUN] {op.source.name} -> {op.destination.name}")
        else:
            op.source.rename(op.destination)
            renamed_count += 1
            print(f"[RENAMED] {op.source.name} -> {op.destination.name}")

    print("\n📊 Summary:")
    print(f"  - Total files scanned: {len(files)}")
    print(f"  - Files to rename: {renamed_count}" if args.dry_run else f"  - Files renamed: {renamed_count}")
    print(f"  - Files unchanged: {unchanged_count}")


if __name__ == "__main__":
    main()

