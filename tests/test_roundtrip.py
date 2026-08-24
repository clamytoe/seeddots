from seeddots.dotmap import encode_word, decode_columns


def test_roundtrip_phrase(wl):
    phrase = ["abandon", "ability", "able"]
    encoded = [encode_word(w, wl, "ascii") for w in phrase]
    decoded = [decode_columns(c1, c2, c3, wl, "ascii") for c1, c2, c3 in encoded]
    assert decoded == phrase
