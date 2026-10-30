#!/usr/bin/env python3
"""Secure Password Generator - CLI.

Generates cryptographically secure passwords with Python's `secrets` module.
Length and character classes are configurable, every enabled class is
guaranteed to appear at least once, and an entropy-based strength score is
reported for each password.

Usage:
    python scripts/python/password_generator.py
    python scripts/python/password_generator.py --length 24 --no-symbols
    python scripts/python/password_generator.py -l 32 --no-uppercase --copy

Flags:
    -l, --length     Password length (default: 16)
    --no-symbols     Exclude punctuation symbols
    --no-numbers     Exclude digits
    --no-uppercase   Exclude uppercase letters
    --copy           Copy the password to the clipboard (optional dependency:
                     `pip install pyperclip`)

Lowercase letters are always included. The password is printed to stdout and
the strength report to stderr, so `PASSWORD=$(python password_generator.py)`
captures only the password.
"""

from __future__ import annotations

import argparse
import math
import secrets
import string
import sys

# Ensure UTF-8 output encoding across all operating systems and shells
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_LENGTH = 16

# Upper bounds (in bits) for each strength label, checked in order.
STRENGTH_LEVELS: list[tuple[float, str]] = [
    (28, "Very weak"),
    (36, "Weak"),
    (60, "Reasonable"),
    (128, "Strong"),
]


def build_character_sets(
    use_uppercase: bool = True,
    use_numbers: bool = True,
    use_symbols: bool = True,
) -> list[str]:
    """Return the enabled character classes. Lowercase letters are always included."""
    character_sets = [string.ascii_lowercase]
    if use_uppercase:
        character_sets.append(string.ascii_uppercase)
    if use_numbers:
        character_sets.append(string.digits)
    if use_symbols:
        character_sets.append(string.punctuation)
    return character_sets


def generate_password(length: int, character_sets: list[str]) -> str:
    """Generate a password containing at least one character from every set."""
    if length < len(character_sets):
        raise ValueError(
            f"length must be at least {len(character_sets)} to include every enabled character type"
        )

    pool = "".join(character_sets)
    characters = [secrets.choice(charset) for charset in character_sets]
    characters += [secrets.choice(pool) for _ in range(length - len(characters))]
    secrets.SystemRandom().shuffle(characters)
    return "".join(characters)


def estimate_entropy_bits(length: int, pool_size: int) -> float:
    """Estimate entropy as length * log2(pool size).

    This is a slight overestimate, because one character from each enabled
    class is guaranteed rather than drawn from the whole pool.
    """
    return length * math.log2(pool_size)


def strength_label(entropy_bits: float) -> str:
    """Map an entropy estimate to a human-readable strength label."""
    for upper_bound, label in STRENGTH_LEVELS:
        if entropy_bits < upper_bound:
            return label
    return "Very strong"


def copy_to_clipboard(text: str) -> bool:
    """Copy text with pyperclip if it is installed. Return True on success."""
    try:
        import pyperclip
    except ImportError:
        print(
            "⚠️ --copy requires pyperclip (pip install pyperclip); the password was not copied.",
            file=sys.stderr,
        )
        return False

    try:
        pyperclip.copy(text)
    except pyperclip.PyperclipException as exc:
        print(f"⚠️ Could not copy to the clipboard: {exc}", file=sys.stderr)
        return False
    return True


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a cryptographically secure password."
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=DEFAULT_LENGTH,
        help=f"Password length (default: {DEFAULT_LENGTH})",
    )
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude punctuation symbols",
    )
    parser.add_argument(
        "--no-numbers",
        action="store_true",
        help="Exclude digits",
    )
    parser.add_argument(
        "--no-uppercase",
        action="store_true",
        help="Exclude uppercase letters",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy the password to the clipboard (requires pyperclip)",
    )
    return parser.parse_args()


def main() -> None:
    """Script entry point."""
    args = parse_arguments()

    character_sets = build_character_sets(
        use_uppercase=not args.no_uppercase,
        use_numbers=not args.no_numbers,
        use_symbols=not args.no_symbols,
    )

    try:
        password = generate_password(args.length, character_sets)
    except ValueError as exc:
        print(f"❌ Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(password)

    pool_size = len("".join(character_sets))
    entropy_bits = estimate_entropy_bits(args.length, pool_size)
    print(
        f"🔐 Entropy: ~{entropy_bits:.1f} bits ({strength_label(entropy_bits)})",
        file=sys.stderr,
    )

    if args.copy and copy_to_clipboard(password):
        print("📋 Copied to clipboard.", file=sys.stderr)


if __name__ == "__main__":
    main()
