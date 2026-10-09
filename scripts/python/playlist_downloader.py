#!/usr/bin/env python3
"""YouTube Playlist Media Downloader - CLI & Argument Parser.

A flexible utility for developers to download complete playlists or single videos
from YouTube and supported platforms with video or audio-only extraction.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Any

import yt_dlp

# Ensure UTF-8 output encoding across all operating systems and shells
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def validate_url(url: str) -> bool:
    """Check if the provided string is a valid web URL."""
    return url.startswith("http://") or url.startswith("https://")


def build_ydl_options(
    output_dir: Path,
    audio_only: bool = False,
    custom_format: str | None = None,
    simulate: bool = False,
    max_downloads: int | None = None,
) -> tuple[dict[str, Any], bool]:
    """Construct configuration options for yt_dlp.YoutubeDL."""
    output_dir.mkdir(parents=True, exist_ok=True)
    has_ffmpeg = shutil.which("ffmpeg") is not None
    has_node = shutil.which("node") is not None

    outtmpl = str(output_dir / "%(playlist_title|)s%(playlist_title&/|)s%(title)s.%(ext)s")

    ydl_opts: dict[str, Any] = {
        "outtmpl": outtmpl,
        "ignoreerrors": True,
        "simulate": simulate,
        "quiet": False,
        "no_warnings": False,
    }

    # Automatically enable Node.js runtime for modern YouTube player API if present
    if has_node:
        ydl_opts["js_runtimes"] = {"node": {"path": "node"}}

    if max_downloads:
        ydl_opts["max_downloads"] = max_downloads

    if audio_only:
        ydl_opts["format"] = "ba/b"
        if has_ffmpeg:
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
    elif custom_format:
        ydl_opts["format"] = custom_format

    return ydl_opts, has_ffmpeg


def download_media(
    url: str,
    output_dir: Path,
    audio_only: bool = False,
    custom_format: str | None = None,
    simulate: bool = False,
    max_downloads: int | None = None,
) -> dict[str, Any]:
    """Execute download process using yt-dlp."""
    ydl_opts, has_ffmpeg = build_ydl_options(
        output_dir=output_dir,
        audio_only=audio_only,
        custom_format=custom_format,
        simulate=simulate,
        max_downloads=max_downloads,
    )

    summary: dict[str, Any] = {
        "title": "Unknown",
        "entries_count": 0,
        "success": False,
        "has_ffmpeg": has_ffmpeg,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=not simulate)
        if info:
            summary["success"] = True
            summary["title"] = info.get("title", "Unknown")
            if "entries" in info:
                entries = [e for e in info.get("entries", []) if e is not None]
                summary["entries_count"] = len(entries)
                summary["is_playlist"] = True
            else:
                summary["entries_count"] = 1
                summary["is_playlist"] = False

    return summary


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

    try:
        summary = download_media(
            url=args.url,
            output_dir=output_dir,
            audio_only=args.audio_only,
            custom_format=args.format,
            simulate=args.simulate,
            max_downloads=args.max_downloads,
        )
    except Exception as exc:
        print(f"❌ Error during download: {exc}", file=sys.stderr)
        sys.exit(1)

    print("\n📊 Summary:")
    print(f"  - Target Title: {summary.get('title')}")
    print(f"  - Total items processed: {summary.get('entries_count', 0)}")
    print(f"  - FFmpeg available: {'Yes' if summary.get('has_ffmpeg') else 'No (using native stream fallback)'}")
    print(f"  - Status: {'Completed successfully' if summary.get('success') else 'Completed with warnings/errors'}")


if __name__ == "__main__":
    main()

