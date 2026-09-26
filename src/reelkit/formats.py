"""Output formats. Call ``use()`` at module level in a scene file, before the scene class.

Frame units are chosen so one unit is roughly the same size on screen in every
format: a vertical frame is 9 x 16 units, a horizontal one 16 x 9.

Set ``REELKIT_DRAFT=1`` to render at half resolution and 15 fps while iterating.
"""

import os
from dataclasses import dataclass

from manim import config

from .theme import DEFAULT, Theme


@dataclass(frozen=True)
class Format:
    name: str
    pixel_width: int
    pixel_height: int
    frame_width: float
    frame_height: float
    margin: float = 0.7

    @property
    def left_x(self) -> float:
        return -self.frame_width / 2 + self.margin

    @property
    def right_x(self) -> float:
        return self.frame_width / 2 - self.margin

    @property
    def max_w(self) -> float:
        return self.frame_width - 2 * self.margin


VERTICAL = Format("vertical", 1080, 1920, 9, 16)
HORIZONTAL = Format("horizontal", 1920, 1080, 16, 9)
SQUARE = Format("square", 1080, 1080, 9, 9)
FORMATS = {f.name: f for f in (VERTICAL, HORIZONTAL, SQUARE)}

_current = VERTICAL


def use(fmt: Format | str, fps: int = 30, theme: Theme = DEFAULT) -> Format:
    global _current
    if isinstance(fmt, str):
        fmt = FORMATS[fmt]
    draft = os.environ.get("REELKIT_DRAFT") == "1"
    config.pixel_width = fmt.pixel_width // (2 if draft else 1)
    config.pixel_height = fmt.pixel_height // (2 if draft else 1)
    config.frame_width = fmt.frame_width
    config.frame_height = fmt.frame_height
    config.frame_rate = 15 if draft else fps
    config.background_color = theme.bg
    _current = fmt
    return fmt


def current() -> Format:
    return _current
