"""
utils.py — Utility functions for SeedDots.

This module contains:
- BIP39 wordlist loading
- file parsing helpers
- phrase resolution (file, clipboard, direct input)
- verification of decoded phrases
- printable card generation (markdown + SVG)

No CLI, no Click, no Rich.
"""

from __future__ import annotations

from typing import List, Tuple, Optional
from importlib.resources import files
from PIL import Image, ImageDraw, ImageFont

import pyperclip

# LOGO_PATTERNS = {
#     "dark": [
#         "● ● ● ● ● ● ● ● ● ",
#         "● ● ○ ○ ● ○ ○ ● ● ",
#         "● ○ ● ● ● ○ ● ○ ● ",
#         "● ● ○ ○ ● ○ ● ○ ● ",
#         "● ● ● ○ ● ○ ● ○ ● ",
#         "● ○ ○ ● ● ○ ○ ● ● ",
#     ],
#     "light": [
#         "○ ○ ○ ○ ○ ○ ○ ○ ○ ",
#         "○ ○ ● ● ○ ● ● ○ ○ ",
#         "○ ● ○ ○ ○ ● ○ ● ○ ",
#         "○ ○ ● ● ○ ● ○ ● ○ ",
#         "○ ○ ○ ● ○ ● ○ ● ○ ",
#         "○ ● ● ○ ○ ● ● ○ ○ ",
#     ],
# }
LOGO_MATRIX = {
    "dark": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 0, 0, 1, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 1, 0, 0, 1, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 1, 1, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "light": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
}


# ---------------------------------------------------------------------------
# Wordlist loading
# ---------------------------------------------------------------------------


def load_wordlist(path: str = "bip39_english.txt") -> List[str]:
    """
    Load the BIP39 wordlist from the package data directory.
    """
    wordlist_path = files("seeddots.data").joinpath(path)
    return wordlist_path.read_text(encoding="utf-8").splitlines()


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------


def normalize_encoded(text: str) -> str:
    """
    Normalize encoded text to only include 0 and 1.
    """
    return "".join(ch for ch in text if ch in "01")


# ---------------------------------------------------------------------------
# File parsing
# ---------------------------------------------------------------------------


def parse_pass_phrase_file(file_path: str) -> Optional[str]:
    """
    Read a file containing a mnemonic phrase.
    Returns the phrase as a string, or None on error.
    """
    try:
        with open(file_path, "r", encoding="ascii") as f:
            return f.read().strip()
    except UnicodeDecodeError:
        return None
    except Exception:
        return None


def parse_dot_file(file_path: str) -> Optional[List[str]]:
    """
    Read a file containing dotmap lines.
    Returns a list of lines, or None on error.
    """
    try:
        with open(file_path, "r", encoding="ascii") as f:
            return [line.strip() for line in f.readlines()]
    except UnicodeDecodeError:
        return None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Phrase resolution
# ---------------------------------------------------------------------------


def resolve_phrase_input(
    file: Optional[str],
    from_clipboard: bool,
    phrase: Optional[str],
) -> Optional[str]:
    """
    Resolve the mnemonic phrase from:
    - a file
    - clipboard
    - direct argument
    """
    if file:
        return parse_pass_phrase_file(file)

    if from_clipboard:
        content = pyperclip.paste().strip()
        return content if content else None

    if phrase:
        return phrase

    return None


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------


def verify_phrase(
    decoded_words: List[str],
    input_lines: List[str],
    wordlist: List[str],
    symbol_set: str,
    *,
    encode_fn,
) -> Tuple[bool, Optional[List[Tuple[int, str, str, str]]]]:
    """
    Verify that the decoded words match the original dotmap input.

    Returns:
        (True, None) if verified
        (False, mismatches) if mismatches found
    """
    reencoded_lines = []

    for word in decoded_words:
        try:
            col1, col2, col3 = encode_fn(word, wordlist, symbol_set)
            reencoded_lines.append(f"{col1} {col2} {col3}")
        except ValueError:
            return False, [(0, word, "N/A", "Word not found")]

    mismatches = []
    for i, (orig, recon) in enumerate(zip(input_lines, reencoded_lines)):
        orig = normalize_encoded(orig)
        recon = normalize_encoded(recon)
        if orig.strip() != recon.strip():
            mismatches.append((i + 1, decoded_words[i], orig, recon))

    if mismatches:
        return False, mismatches

    return True, None


# ---------------------------------------------------------------------------
# Printable card generation
# ---------------------------------------------------------------------------


def generate_markdown_card(entries: List[Tuple[int, str, int, str]]) -> str:
    """
    Generate a Markdown stamping card for OneKey plates.
    """
    lines = [
        "# 🔐 OneKey Stamping Card\n",
        "| # | Word | Index | Binary |",
        "|---|------|--------|--------|",
    ]

    for i, word, index, binary in entries:
        lines.append(f"| {i} | {word} | {index:04} | {binary} |")

    lines.append("\n🕯️ Print and align this card over your OneKey plate for stamping.")
    return "\n".join(lines)


def generate_svg_card(entries: List[Tuple[int, str, int, str]]) -> str:
    """
    Generate an SVG stamping card for OneKey plates.
    """
    svg_header = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="{}">'.format(
            30 * len(entries) + 40
        )
    )
    svg_footer = "</svg>"
    rows = []

    for i, (num, word, index, binary) in enumerate(entries):
        y = 30 * i + 30
        rows.append(
            f'<text x="10" y="{y}" font-family="monospace" font-size="14">{num:02}. {word} ({index:04})</text>'
        )
        for j, bit in enumerate(binary):
            cx = 150 + j * 12
            fill = "#000" if bit == "1" else "#ccc"
            rows.append(f'<circle cx="{cx}" cy="{y - 5}" r="5" fill="{fill}" />')

    return "\n".join([svg_header] + rows + [svg_footer])


def logo_gen(style: str = "dark") -> str:
    """Return the ASCII logo as a string."""
    filled = "●"
    empty = "○"
    rows = LOGO_MATRIX[style]

    lines = []
    for row in rows:
        line = " ".join(filled if v else empty for v in row)
        lines.append(line)

    return "\n".join(lines)


def save_logo_png(style: str, output: str, size: int = 64) -> None:
    """Render the logo as a PNG with transparent background.
    1 = filled circle + outline
    0 = outline only (transparent fill)
    """
    rows = LOGO_MATRIX[style]
    dot = size
    padding = size // 2

    width = len(rows[0]) * dot + padding * 2
    height = len(rows) * dot + padding * 2

    # Transparent background
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outline + fill color
    fg = (255, 255, 255, 255) if style == "dark" else (0, 0, 0, 255)

    for y, row in enumerate(rows):
        for x, v in enumerate(row):
            cx = padding + x * dot + dot // 2
            cy = padding + y * dot + dot // 2
            r = dot // 2 - 4

            if v == 1:
                # Filled + outline
                draw.ellipse(
                    (cx - r, cy - r, cx + r, cy + r),
                    fill=fg,
                    outline=fg,
                    width=3,
                )
            else:
                # Outline only, transparent fill
                draw.ellipse(
                    (cx - r, cy - r, cx + r, cy + r),
                    fill=None,
                    outline=fg,
                    width=3,
                )

    img.save(output)
