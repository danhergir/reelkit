"""A sentence that grows one token at a time.

Each step builds the longer sentence as a fresh Text and aligns its first glyph
with the previous one, so the words already on screen never move.
"""

from manim import LEFT, UL, FadeIn, Mobject, Scene, Text

from .. import formats
from ..text import glyphs, txt
from ..theme import DEFAULT, Theme


def sentence(text: str, *, scale: float = 0.95, top_y: float | None = None,
             theme: Theme = DEFAULT) -> Text:
    fmt = formats.current()
    top_y = fmt.frame_height / 2 - 3.3 if top_y is None else top_y
    m = txt(text, scale, bold=True, theme=theme)
    return m.move_to([fmt.left_x, top_y, 0], aligned_edge=UL)


def _grown(current: Text, new_text: str, theme: Theme, **kwargs) -> Text:
    new = sentence(new_text, theme=theme, **kwargs)
    return new.shift(current[0].get_center() - new[0].get_center())


def fly_in(scene: Scene, current: Text, new_text: str, word: str, source: Mobject, *,
           color: str, run_time: float = 0.8, theme: Theme = DEFAULT, **kwargs) -> Text:
    """Fly ``word`` from ``source`` (e.g. a TokenBars label) to the end of the sentence."""
    new = _grown(current, new_text, theme, **kwargs)
    target = new[-glyphs(word):].copy()
    moving = target.copy().scale(0.6).move_to(source).set_color(color)
    scene.play(FadeIn(moving), run_time=0.15)
    scene.play(moving.animate.move_to(target).scale(1 / 0.6).set_color(theme.fg),
               run_time=run_time)
    scene.remove(current, moving)
    scene.add(new)
    return new


def append_in_place(scene: Scene, current: Text, new_text: str, word: str, *,
                    run_time: float = 0.4, theme: Theme = DEFAULT, **kwargs) -> Text:
    """Fade ``word`` in at the end of the sentence, no source."""
    new = _grown(current, new_text, theme, **kwargs)
    tail = new[-glyphs(word):]
    scene.play(FadeIn(tail, shift=LEFT * 0.2), run_time=run_time)
    scene.remove(current, tail)
    scene.add(new)
    return new
