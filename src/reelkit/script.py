"""Episode scripts: the narration, one segment per on-screen beat.

An episode directory holds a ``script.toml``::

    [meta]
    title = "One word at a time"
    scene = "Demo"               # Manim scene class in scene.py
    format = "vertical"          # vertical | horizontal | square
    slug = "demo"                # output file name

    [segments]
    intro = "A language model writes one word at a time."
"""

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

WORDS_PER_SECOND = 2.7


def output_root() -> Path:
    """Where renders, audio and cards go — never inside the repo.

    ``$REELKIT_OUTPUT`` if set, otherwise ``~/Movies/reelkit``.
    """
    return Path(os.environ.get("REELKIT_OUTPUT", Path.home() / "Movies" / "reelkit")).expanduser()


@dataclass(frozen=True)
class Script:
    root: Path
    title: str
    scene: str
    format: str
    slug: str
    segments: dict[str, str]

    @property
    def work_dir(self) -> Path:
        return output_root() / self.slug

    @property
    def audio_dir(self) -> Path:
        return self.work_dir / "build" / "audio"

    @property
    def media_dir(self) -> Path:
        return self.work_dir / "build" / "media"


def load_script(episode_dir: str | Path) -> Script:
    root = Path(episode_dir).resolve()
    data = tomllib.loads((root / "script.toml").read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    segments = data.get("segments", {})
    if not segments:
        raise ValueError(f"{root / 'script.toml'} has no [segments]")
    return Script(
        root=root,
        title=meta.get("title", root.name),
        scene=meta["scene"],
        format=meta.get("format", "vertical"),
        slug=meta.get("slug", root.name),
        segments=dict(segments),
    )


def estimate_seconds(text: str) -> float:
    """Reading-pace estimate, used to time a scene when no audio exists yet."""
    return round(len(text.split()) / WORDS_PER_SECOND + 0.3, 2)
