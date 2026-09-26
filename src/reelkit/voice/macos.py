"""Voiceover with macOS system voices (``say``). Free and local.

The Enhanced/Premium voices sound far more natural than the compact defaults;
download them in System Settings → Accessibility → Spoken Content → System Voice
→ Manage Voices, then pass their exact name, e.g. ``"Paulina (Premium)"``.
"""

import json
import subprocess
from pathlib import Path

MANIFEST = "durations.json"


def _run(*cmd: str) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def list_voices(locale_prefix: str = "") -> list[str]:
    """Installed voice names, optionally filtered by locale (e.g. ``"es_"``)."""
    voices = []
    for line in _run("say", "-v", "?").splitlines():
        head = line.split("#", 1)[0].rstrip()
        name, _, locale = head.rpartition(" ")
        if locale.startswith(locale_prefix):
            voices.append(name.strip())
    return voices


def synthesize(segments: dict[str, str], out_dir: Path, voice: str, rate: int = 185,
               log=print) -> dict[str, float]:
    """Speak every segment to ``out_dir/<key>.wav`` and write a manifest of durations.

    The manifest also stores each segment's text, so a scene can refuse to use
    audio that no longer matches its script.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    durations = {}
    for key, text in segments.items():
        aiff, wav = out_dir / f"{key}.aiff", out_dir / f"{key}.wav"
        _run("say", "-v", voice, "-r", str(rate), "-o", str(aiff), text)
        _run("ffmpeg", "-v", "error", "-y", "-i", str(aiff), "-ar", "48000", "-ac", "1", str(wav))
        aiff.unlink()
        dur = float(_run("ffprobe", "-v", "error", "-show_entries", "format=duration",
                         "-of", "csv=p=0", str(wav)))
        durations[key] = round(dur, 3)
        log(f"  {key:<16} {dur:5.2f}s  {text}")

    (out_dir / MANIFEST).write_text(json.dumps(
        {"voice": voice, "rate": rate, "segments": durations, "texts": dict(segments)},
        indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"  voice: {voice} · {rate} wpm · {sum(durations.values()):.1f}s spoken")
    return durations
