"""A Manim scene that paces itself to its voiceover.

    class MyEpisode(VoiceScene):
        episode_dir = Path(__file__).parent

        def construct(self):
            self.vo("hook")            # start the "hook" segment's audio now
            self.play(Write(title))    # animate while it plays
            self.hold()                # wait until the line finishes (+ a short pad)

``hold(pad=-0.6)`` returns 0.6 s before the line ends — useful to land an
animation on its last word. Without generated audio the scene still renders,
silent, timed from a reading-pace estimate of each segment.
"""

import json
from pathlib import Path

from manim import Scene

from ..script import estimate_seconds, load_script
from .macos import MANIFEST


class VoiceScene(Scene):
    episode_dir: Path | str | None = None

    def setup(self):
        if self.episode_dir is None:
            raise TypeError(f"{type(self).__name__} must set episode_dir")
        self.script = load_script(self.episode_dir)
        manifest = self.script.audio_dir / MANIFEST
        self.has_audio = manifest.exists()
        if self.has_audio:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            stale = [k for k, t in self.script.segments.items() if data["texts"].get(k) != t]
            if stale:
                raise RuntimeError(f"voiceover is out of date for {stale}; "
                                   "regenerate it with `reelkit voice`")
            self.durations = data["segments"]
        else:
            self.durations = {k: estimate_seconds(t) for k, t in self.script.segments.items()}
        self._vo_end = 0.0

    def vo(self, key: str):
        """Start segment ``key``: its audio begins at the current moment of the scene."""
        if key not in self.durations:
            raise KeyError(f"segment {key!r} is not in {self.script.root / 'script.toml'}")
        if self.has_audio:
            self.add_sound(str(self.script.audio_dir / f"{key}.wav"))
        self._vo_end = self.renderer.time + self.durations[key]

    def hold(self, pad: float = 0.25, minimum: float = 0.0):
        """Wait until the current segment ends, plus ``pad`` (negative returns early)."""
        remaining = max(self._vo_end + pad - self.renderer.time, minimum)
        if remaining > 1 / 60:
            self.wait(remaining)
