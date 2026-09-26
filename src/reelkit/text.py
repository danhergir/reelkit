"""Text helpers that respect the current format's margins."""

from manim import BOLD, LEFT, NORMAL, Mobject, Text

from . import formats
from .theme import DEFAULT, Theme


def txt(s: str, scale: float = 0.6, color: str | None = None, *, bold: bool = False,
        mono: bool = False, theme: Theme = DEFAULT, max_w: float | None = None) -> Text:
    """Text in the theme's fonts, shrunk to fit the frame if it would overflow."""
    t = Text(s, font=theme.mono if mono else theme.sans, color=color or theme.fg,
             weight=BOLD if bold else NORMAL).scale(scale)
    limit = max_w or formats.current().max_w
    if t.width > limit:
        t.scale_to_fit_width(limit)
    return t


def place(m: Mobject, y: float, x: float | None = None) -> Mobject:
    """Left-align ``m`` on the frame margin (or at ``x``), vertically centred on ``y``."""
    return m.move_to([formats.current().left_x if x is None else x, y, 0], aligned_edge=LEFT)


def glyphs(s: str) -> int:
    """How many glyphs Manim renders for ``s`` — whitespace and newlines draw nothing."""
    return len("".join(s.split()))
