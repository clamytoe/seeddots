import pytest
from seeddots.dotmap import encode_word, decode_columns

@pytest.mark.parametrize("word", ["abandon", "zoo"])
def test_boundary_words(wl, word):
    col1, col2, col3 = encode_word(word, wl, "ascii")
    decoded = decode_columns(col1, col2, col3, wl, "ascii")
    assert decoded == word
