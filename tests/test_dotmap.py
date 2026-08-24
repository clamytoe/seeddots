import pytest

from seeddots.encoder import word_to_binary
from seeddots.utils import load_wordlist

# Known mappings from OneKey punch examples
test_cases = [
    ("abandon", "000000000001"),  # index 0 + 1 = 1
    ("once", "010011010101"),  # index 1236 + 1 = 1237
    ("one", "010011010110"),  # index 1237 + 1 = 1238
    ("onion", "010011010111"),  # index 1238 + 1 = 1239
]


@pytest.mark.parametrize("word,expected_binary", test_cases)
def test_word_to_binary(word, expected_binary):
    wordlist = load_wordlist()
    assert word_to_binary(word, wordlist) == expected_binary


def test_no_zero_binary():
    wordlist = load_wordlist()
    for word in wordlist:
        binary = word_to_binary(word, wordlist)
        assert binary != "000000000000", f"{word} returned zero binary!"
