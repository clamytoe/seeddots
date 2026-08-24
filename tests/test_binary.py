from seeddots.dotmap import binary_to_dotmap
from seeddots.encoder import dotmap_to_binary


def test_binary_roundtrip_ascii():
    binary = "000000000001"
    col1, col2, col3 = binary_to_dotmap(binary, "ascii")
    recon = dotmap_to_binary(col1, col2, col3, "ascii")
    assert recon == binary
