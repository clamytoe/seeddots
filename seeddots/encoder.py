"""
encoder.py — Pure encoding/decoding logic for SeedDots.

This module contains:
- BIP39 index → binary conversion
- binary → dotmap conversion
- dotmap → binary conversion
- word → binary helpers
- symbol set definitions
- high-level encode/decode helpers

No I/O, no CLI, no printing.
"""

from __future__ import annotations

from typing import List, Tuple


# ---------------------------------------------------------------------------
# Symbol sets (1-bit, 0-bit)
# ---------------------------------------------------------------------------

SYMBOL_SETS = {
    "dot": ("● ", "○ "),
    "ascii": ("1 ", "0 "),
    "block": ("█ ", "░ "),
    "rune": ("⊙ ", "∘ "),
}


# ---------------------------------------------------------------------------
# Core binary helpers
# ---------------------------------------------------------------------------

def index_to_binary(index: int) -> str:
    """Convert a BIP39 index (1–2048) into a 12-bit binary string."""
    return format(index, "012b")


def binary_to_dotmap(binary: str, symbol_set: str = "dot") -> List[str]:
    """
    Convert a 12-bit binary string into 3 dotmap columns of 4 bits each.
    Returns a list of 3 strings.
    """
    one, zero = SYMBOL_SETS.get(symbol_set, SYMBOL_SETS["dot"])

    return [
        "".join(one if bit == "1" else zero for bit in binary[0:4]),
        "".join(one if bit == "1" else zero for bit in binary[4:8]),
        "".join(one if bit == "1" else zero for bit in binary[8:12]),
    ]


def dotmap_to_binary(col1: str, col2: str, col3: str, symbol_set: str = "dot") -> str:
    """
    Convert 3 dotmap columns back into a 12-bit binary string.
    """
    one, zero = SYMBOL_SETS.get(symbol_set, SYMBOL_SETS["dot"])
    code = col1 + " " + col2 + " " + col3
    binary = "".join("1" if c == one.strip() else "0" for c in (code.replace(" ", "")))
    return binary


# ---------------------------------------------------------------------------
# Word-level helpers
# ---------------------------------------------------------------------------

def word_to_binary(word: str, wordlist: List[str]) -> str:
    """
    Convert a BIP39 word into its 12-bit binary representation.
    """
    index = wordlist.index(word) + 1
    return index_to_binary(index)


def encode_word(word: str, wordlist: List[str], symbol_set: str) -> Tuple[str, str, str]:
    """
    Encode a single BIP39 word into a 3-column dotmap tuple.
    """
    binary = word_to_binary(word, wordlist)
    col1, col2, col3 = binary_to_dotmap(binary, symbol_set)
    return col1, col2, col3


def decode_columns(
    col1: str, col2: str, col3: str, wordlist: List[str], symbol_set: str
) -> str:
    """
    Decode 3 dotmap columns back into a BIP39 word.
    """
    binary = dotmap_to_binary(col1, col2, col3, symbol_set)
    index = int(binary, 2)
    return wordlist[index - 1]


# ---------------------------------------------------------------------------
# Optional: preview helper (pure logic)
# ---------------------------------------------------------------------------

def preview_dotmap(word: str, wordlist: List[str], symbol_set: str = "dot") -> List[str]:
    """
    Return the dotmap columns for a word (no printing).
    """
    binary = word_to_binary(word, wordlist)
    return binary_to_dotmap(binary, symbol_set)
