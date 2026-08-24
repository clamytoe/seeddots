from seeddots.utils import verify_phrase
from seeddots.dotmap import encode_word


def test_verification_success(wl):
    decoded = ["abandon"]
    col1, col2, col3 = encode_word("abandon", wl, "ascii")
    input_lines = [f"{col1} {col2} {col3}"]
    ok, info = verify_phrase(decoded, input_lines, wl, "ascii", encode_fn=encode_word)
    assert ok
    assert info is None


def test_verification_failure(wl):
    decoded = ["abandon"]
    input_lines = ["0000 0000 0010"]  # wrong last bit
    ok, info = verify_phrase(decoded, input_lines, wl, "ascii", encode_fn=encode_word)
    assert not ok
    assert info
    assert info[0][1] == "abandon"
