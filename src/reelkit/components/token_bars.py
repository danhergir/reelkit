"""Candidate next tokens with a probability bar each."""

from manim import LEFT, RIGHT, FadeIn, GrowFromEdge, Rectangle, Text, VGroup

from .. import formats
from ..theme import DEFAULT, Theme


class TokenBars(VGroup):
    """One row per candidate: ``"token"  [bar]  62%``.

    Each row is ``VGroup(label, track, bar, pct)``. Build it, then play
    ``intro()`` and ``grow()``; ``highlight(i, color)`` marks a row.
    """

    def __init__(self, candidates, *, top_y: float = 1.2, spacing: float = 1.0,
                 right_x: float | None = None, label_scale: float = 0.62,
                 bar_height: float = 0.46, theme: Theme = DEFAULT, **kwargs):
        super().__init__(**kwargs)
        self.theme = theme
        self.candidates = list(candidates)
        fmt = formats.current()
        right_x = fmt.right_x - 0.9 if right_x is None else right_x

        labels = [Text(f'"{tok}"', font=theme.mono, color=theme.dim).scale(label_scale)
                  for tok, _ in self.candidates]
        x0 = fmt.left_x + max(l.width for l in labels) + 0.35
        track_w = right_x - x0
        if track_w <= 0.5:
            raise ValueError("labels too wide for the frame; shorten tokens or lower label_scale")

        for j, ((_, p), label) in enumerate(zip(self.candidates, labels)):
            y = top_y - j * spacing
            label.move_to([fmt.left_x, y, 0], aligned_edge=LEFT)
            track = Rectangle(width=track_w, height=bar_height, stroke_width=0,
                              fill_color=theme.track, fill_opacity=1)
            track.move_to([x0, y, 0], aligned_edge=LEFT)
            bar = Rectangle(width=max(track_w * p, 0.06), height=bar_height, stroke_width=0,
                            fill_color=theme.muted, fill_opacity=1)
            bar.move_to([x0, y, 0], aligned_edge=LEFT)
            pct = Text(f"{round(p * 100)}%", font=theme.mono, color=theme.muted).scale(0.55)
            pct.next_to(track, RIGHT, buff=0.2)
            self.add(VGroup(label, track, bar, pct))

    def label(self, i: int):
        return self[i][0]

    def intro(self):
        """Labels and empty tracks."""
        return [FadeIn(VGroup(r[0], r[1])) for r in self]

    def grow(self):
        """Bars grow to their probability; percentages appear."""
        return [GrowFromEdge(r[2], LEFT) for r in self] + [FadeIn(r[3]) for r in self]

    def highlight(self, i: int, color: str):
        r = self[i]
        return [r[2].animate.set_fill(color), r[0].animate.set_color(color),
                r[3].animate.set_color(color)]
