from seeddots.utils import generate_markdown_card, generate_svg_card


def test_generate_markdown_card():
    entries = [(1, "abandon", 0, "000000000001")]
    md = generate_markdown_card(entries)
    assert "abandon" in md
    assert "000000000001" in md

def test_generate_svg_card():
    entries = [(1, "abandon", 0, "000000000001")]
    svg = generate_svg_card(entries)
    assert "<svg" in svg
    assert "abandon" in svg
