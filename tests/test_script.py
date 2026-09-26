import re
from pathlib import Path

from reelkit import load_script
from reelkit.script import estimate_seconds

ROOT = Path(__file__).resolve().parents[1]
EPISODES = sorted(p for p in (ROOT / "examples" / "episodes").iterdir() if (p / "script.toml").exists())


def test_there_is_at_least_one_episode():
    assert EPISODES


def test_episode_scripts_load():
    for ep in EPISODES:
        s = load_script(ep)
        assert s.scene and s.format in {"vertical", "horizontal", "square"}
        assert all(text.strip() for text in s.segments.values())


def test_scene_and_script_segments_match():
    # Every self.vo("key") in the scene must exist in script.toml, and every
    # scripted segment must be used — otherwise narration and picture drift apart.
    for ep in EPISODES:
        used = set(re.findall(r'self\.vo\("([A-Za-z0-9_]+)"\)', (ep / "scene.py").read_text()))
        assert used == set(load_script(ep).segments), ep.name


def test_estimate_grows_with_length():
    assert estimate_seconds("uno dos tres cuatro cinco") > estimate_seconds("uno")
