"""Static cards (PNG) in the same visual language as the videos.

A card is a TOML spec rendered to HTML and screenshotted with headless Chrome::

    type = "timeline"            # or "reference"
    kicker = "Benchmark saturation"
    title = "Every time it falls, they build a harder one."
    foot = "Optional closing line."
    accent = "warn"              # theme role or hex; default "accent"

    [[events]]                   # timeline cards
    year = "2018"
    text = "GLUE ships."
    emphasis = "Optional highlighted tail"
    highlight = true

    [[rows]]                     # reference cards
    claim = "It's way cheaper now"
    name = "Distillation"
    author = "Hinton"
    year = "2015"
    note = "Cheapening known capability is a tradition"
"""

import html
import shutil
import subprocess
import tempfile
import tomllib
from importlib.resources import files
from pathlib import Path

from ..theme import DEFAULT, Theme

SIZES = {"timeline": (1200, 675), "reference": (1200, 1000)}
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
]


def load_card(path: str | Path) -> dict:
    return tomllib.loads(Path(path).read_text(encoding="utf-8"))


def _e(s: str | None) -> str:
    return html.escape(s or "").replace("\n", "<br>")


def _timeline(spec: dict) -> str:
    out = []
    for ev in spec.get("events", []):
        tail = f" <b>{_e(ev['emphasis'])}</b>" if ev.get("emphasis") else ""
        hit = " hit" if ev.get("highlight") else ""
        out.append(f'<div class="ev"><div class="dot{hit}"></div>'
                   f'<div class="yr">{_e(ev["year"])}</div>'
                   f'<div class="tx">{_e(ev["text"])}{tail}</div></div>')
    return f'<div class="tl">{"".join(out)}</div>'


def _reference(spec: dict) -> str:
    out = []
    for r in spec.get("rows", []):
        author = f", {_e(r['author'])}" if r.get("author") else ""
        year = f' <span class="yr">· {_e(r["year"])}</span>' if r.get("year") else ""
        out.append(f'<tr><td class="q">"{_e(r["claim"])}"</td>'
                   f'<td class="a"><b>{_e(r["name"])}</b>{author}{year}<br>{_e(r.get("note"))}</td></tr>')
    return f'<table>{"".join(out)}</table>'


BUILDERS = {"timeline": _timeline, "reference": _reference}


def build_html(spec: dict, theme: Theme = DEFAULT) -> tuple[str, int, int]:
    """Return ``(html, width, height)`` for a card spec."""
    kind = spec.get("type")
    if kind not in BUILDERS:
        raise ValueError(f"unknown card type {kind!r}; expected one of {sorted(BUILDERS)}")
    w, h = spec.get("width", SIZES[kind][0]), spec.get("height", SIZES[kind][1])
    accent = theme.color(spec.get("accent", "accent"))
    root = (f":root{{--w:{w}px;--h:{h}px;--bg:{theme.bg};--fg:{theme.fg};--dim:{theme.dim};"
            f"--muted:{theme.muted};--track:{theme.track};--accent:{accent};"
            f"--mono:'{theme.mono}';--sans:'{theme.sans}'}}")
    css = files("reelkit.cards").joinpath("base.css").read_text(encoding="utf-8")
    body = BUILDERS[kind](spec)
    foot = f'<div class="foot">{_e(spec["foot"])}</div>' if spec.get("foot") else ""
    doc = (f'<!doctype html><meta charset="utf-8"><style>{root}{css}</style>'
           f'<body class="{kind}"><div class="accent"></div><div class="kicker">{_e(spec.get("kicker"))}</div>'
           f'<h1>{_e(spec.get("title"))}</h1>{body}{foot}')
    return doc, w, h


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if Path(c).exists() or shutil.which(c):
            return c
    raise FileNotFoundError("Chrome or Chromium is needed to render cards")


def render_card(spec: dict, out_png: str | Path, scale: int = 2, theme: Theme = DEFAULT) -> Path:
    doc, w, h = build_html(spec, theme)
    out_png = Path(out_png).resolve()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "card.html"
        page.write_text(doc, encoding="utf-8")
        subprocess.run([find_chrome(), "--headless", "--disable-gpu", "--hide-scrollbars",
                        f"--force-device-scale-factor={scale}", f"--window-size={w},{h}",
                        f"--screenshot={out_png}", page.as_uri()],
                       check=True, capture_output=True)
    return out_png
