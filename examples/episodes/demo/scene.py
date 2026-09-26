"""A minimal episode: one sentence, one prediction step. Probabilities are illustrative."""

from pathlib import Path

from manim import DOWN, LEFT, UP, FadeIn, FadeOut, Write

from reelkit import formats, load_script
from reelkit.components import TokenBars, fly_in, sentence
from reelkit.text import place, txt
from reelkit.theme import DEFAULT as T
from reelkit.voice import VoiceScene

HERE = Path(__file__).resolve().parent
formats.use(load_script(HERE).format)


class Demo(VoiceScene):
    episode_dir = HERE

    def construct(self):
        title = place(txt("A language model writes\none word at a time.", 0.95, bold=True), 1.5)
        self.vo("intro")
        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.5)
        self.hold()
        self.play(FadeOut(title), run_time=0.4)

        self.vo("scores")
        s = sentence("The cat sat on the")
        self.play(Write(s), run_time=0.9)
        bars = TokenBars([("mat", 0.58), ("floor", 0.21), ("sofa", 0.09), ("roof", 0.03)])
        self.play(*bars.intro(), run_time=0.5)
        self.play(*bars.grow(), run_time=1.0)
        self.hold()

        self.vo("pick")
        self.play(*bars.highlight(0, T.accent), run_time=0.45)
        s = fly_in(self, s, "The cat sat on the mat", "mat", bars.label(0), color=T.accent)
        self.play(FadeOut(bars), run_time=0.4)
        self.hold(pad=1.0)
