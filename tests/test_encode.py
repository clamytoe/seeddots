import pytest
from seeddots.dotmap import encode_word, binary_to_dotmap

@pytest.mark.parametrize("symbol_set", ["ascii", "dot", "block", "rune"])
def test_encode_word_symbol_sets(wl, symbol_set):
    col1, col2, col3 = encode_word("abandon", wl, symbol_set)
    assert len(col1.split()) == 4
    assert len(col2.split()) == 4
    assert len(col3.split()) == 4
    assert isinstance(col1, str)
