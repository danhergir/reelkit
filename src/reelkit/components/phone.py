"""A phone message with a predictive-text bar: the everyday version of next-token prediction."""

from manim import LEFT, RIGHT, Line, RoundedRectangle, Scene, VGroup

from .. import formats
from ..text import glyphs, txt
from ..theme import DEFAULT, Theme


class PhoneAutocomplete:
    """Not a VGroup on purpose: the typed message is replaced on ``accept``, so
    scenes fade ``parts`` individually instead of one stale group."""

    def __init__(self, typed: str, suggestions: list[str], *, bubble_y: float = 2.0,
                 bar_y: float = 0.5, scale: float = 0.7, theme: Theme = DEFAULT):
        fmt = formats.current()
        lx, w = fmt.left_x, fmt.max_w
        self.theme, self.scale, self.suggestions = theme, scale, list(suggestions)

        self.bubble = RoundedRectangle(corner_radius=0.35, width=5.4, height=1.1, stroke_width=0,
                                       fill_color=theme.track, fill_opacity=1)
        self.bubble.move_to([lx, bubble_y, 0], aligned_edge=LEFT)
        self.msg = txt(typed, scale, theme=theme)
        self.msg.move_to(self.bubble.get_left() + RIGHT * 0.45, aligned_edge=LEFT)

        self.keybar = RoundedRectangle(corner_radius=0.2, width=w, height=0.95, stroke_width=0,
                                       fill_color=theme.panel, fill_opacity=1)
        self.keybar.move_to([lx + w / 2, bar_y, 0])
        n = len(self.suggestions)
        self.chips = VGroup(*[txt(s, 0.6, theme.dim, theme=theme) for s in self.suggestions])
        for k, chip in enumerate(self.chips):
            chip.move_to([lx + w * (k + 0.5) / n, bar_y, 0])
        self.seps = VGroup(*[Line([lx + w * k / n, bar_y - 0.28, 0], [lx + w * k / n, bar_y + 0.28, 0],
                                  stroke_color=theme.muted, stroke_width=1.5) for k in range(1, n)])

    @property
    def parts(self):
        """Message first (bubble, text), then keyboard (bar, chips, separators)."""
        return [self.bubble, self.msg, self.keybar, self.chips, self.seps]

    def accept(self, scene: Scene, index: int, full_text: str, run_time: float = 0.6):
        chip = self.chips[index]
        scene.play(chip.animate.set_color(self.theme.accent), run_time=0.3)
        new = txt(full_text, self.scale, theme=self.theme)
        new.shift(self.msg[0].get_center() - new[0].get_center())
        target = new[-glyphs(self.suggestions[index]):].copy()
        moving = chip.copy()
        scene.play(moving.animate.move_to(target).match_height(target).set_color(self.theme.fg),
                   chip.animate.set_color(self.theme.dim), run_time=run_time)
        scene.remove(self.msg, moving)
        scene.add(new)
        self.msg = new
