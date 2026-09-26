from pathlib import Path

import pytest

from reelkit.cards import build_html, load_card

EXAMPLES = sorted((Path(__file__).resolve().parents[1] / "examples" / "cards").glob("*.toml"))


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.stem)
def test_example_cards_build(path):
    spec = load_card(path)
    doc, w, h = build_html(spec)
    assert w > 0 and h > 0
    assert spec["kicker"] in doc


def test_card_text_is_escaped():
    doc, _, _ = build_html({"type": "timeline", "kicker": "k", "title": "<script>x</script>",
                            "events": [{"year": "2020", "text": "a & b"}]})
    assert "<script>x" not in doc
    assert "&lt;script&gt;" in doc and "a &amp; b" in doc


def test_unknown_card_type_is_rejected():
    with pytest.raises(ValueError):
        build_html({"type": "carousel"})
