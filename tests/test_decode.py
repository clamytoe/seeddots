import pytest
from seeddots.dotmap import decode_columns


@pytest.mark.parametrize("data, expected", [
    (["0000 0000 0001", "ascii"], "abandon"),
    (["0 0 0 0  0 0 0 0  0 0 0 1", "ascii"], "abandon"),
    (["○○○○ ○○○○ ○○○●", "dot"], "abandon"),
])
def test_decode_columns_formats(wl, data, expected):
    line = data[0]
    symbol_set = data[1]
    if len(line) == 14:
        col1, col2, col3 = line.split()
    elif len(line) == 25:
        parts = line.split("  ")
        chars = [char.replace(" ", "") for char in parts]
        col1 = "".join(chars[0:4])
        col2 = "".join(chars[4:8])
        col3 = "".join(chars[8:12])
    else:
        raise ValueError("Invalid test input format")

    assert decode_columns(col1, col2, col3, wl, symbol_set) == expected
