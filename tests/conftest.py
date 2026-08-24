import pytest
from seeddots.utils import load_wordlist

@pytest.fixture
def wl():
    return load_wordlist("bip39_english.txt")

@pytest.fixture
def abandon_index(wl):
    return wl.index("abandon")

@pytest.fixture
def abandon_binary(abandon_index):
    # index_to_binary expects 1-based index
    return format(abandon_index, "012b")
