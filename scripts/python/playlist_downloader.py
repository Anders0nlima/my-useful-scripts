#!/usr/bin/env python3
"""YouTube Playlist Media Downloader - CLI & Argument Parser.

A flexible utility for developers to download complete playlists or single videos
from YouTube and supported platforms with video or audio-only extraction.
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


def validate_url(url: str) -> bool:
    """Check if the provided string is a valid web URL."""
    return url.startswith("http://") or url.startswith("https://")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Download YouTube playlists or videos as video (MP4) or audio."
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
        help="URL of the YouTube playlist or video to download",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("./downloads"),
        help="Directory to save downloaded files (default: ./downloads)",
    )
    parser.add_argument(
        "-a",
        "--audio-only",
        action="store_true",
        help="Extract audio only (best audio / MP3 format)",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default=None,
        help="Custom yt-dlp format string (e.g. 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]')",
    )
    parser.add_argument(
        "-s",
        "--simulate",
        action="store_true",
        help="Simulate the download process without downloading actual files (dry run)",
    )
    parser.add_argument(
        "--max-downloads",
        type=int,
        default=None,
        help="Maximum number of videos to download from the playlist",
    )
    return parser.parse_args()


def main() -> None:
    """Script entry point."""
    args = parse_arguments()

    if not validate_url(args.url):
        print("❌ Error: Invalid URL provided. Please provide a valid http/https URL.", file=sys.stderr)
        sys.exit(1)

    if args.max_downloads is not None and args.max_downloads <= 0:
        print("❌ Error: --max-downloads must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output.resolve()
    media_mode = "Audio Only" if args.audio_only else "Video"

    print("🎥 YouTube Playlist Media Downloader")
    print(f"🔗 Target URL: {args.url}")
    print(f"📂 Output Directory: {output_dir}")
    print(f"🎵 Media Mode: {media_mode}")
    if args.simulate:
        print("🔍 SIMULATION MODE enabled - No files will be downloaded to disk.\n")
    else:
        print()


if __name__ == "__main__":
    main()

