import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MEDIA = (".mp4", ".mov", ".webm", ".gif", ".png", ".jpg", ".jpeg",
         ".wav", ".aiff", ".mp3", ".m4a")


def test_no_media_is_tracked():
    """Renders and voiceovers are generated output; they must never be committed."""
    try:
        files = subprocess.run(["git", "ls-files"], cwd=ROOT, check=True,
                               capture_output=True, text=True).stdout.splitlines()
    except (FileNotFoundError, subprocess.CalledProcessError):
        pytest.skip("not a git checkout")
    tracked = [f for f in files if f.lower().endswith(MEDIA)]
    assert not tracked, f"media files are tracked: {tracked}"
