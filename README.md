# reelkit

Short explainer videos and static cards about how AI works, built on [Manim](https://www.manim.community/).

reelkit separates the **library** — a visual theme, reusable animated components,
voiceover sync, output formats — from **episodes**, each one a narration script
plus a short scene that tells one story. Episodes can live anywhere; keep your own
in a separate folder or repository.

> Status: 0.1, early. macOS-first: voiceover uses the system's `say` voices and
> cards render with Chrome.

## What's in it

| | |
| --- | --- |
| `TokenBars` | Candidate next tokens with a probability bar each |
| `sentence`, `fly_in`, `append_in_place` | A sentence that grows one token at a time without the earlier words moving |
| `PhoneAutocomplete` | A phone message with a predictive-text bar |
| `VoiceScene` | A scene that paces itself to its voiceover: `vo("key")` starts a line, `hold()` waits for it to end |
| `formats` | Vertical 9:16, horizontal 16:9, square |
| `cards` | Static PNG cards (timeline, reference table) in the same visual language |

## Install

```bash
brew install pango ffmpeg            # system libraries Manim needs
python3.12 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Use

```bash
# Spanish voices installed on this Mac
.venv/bin/reelkit voices --locale es_

# Generate the narration, then render the example episode with it
.venv/bin/reelkit render examples/episodes/demo --voice "Samantha"
# → ~/Movies/reelkit/demo/demo.mp4

# Quick low-resolution preview while iterating (silent if no voice was generated)
.venv/bin/reelkit render examples/episodes/demo --draft

# A static card
.venv/bin/reelkit card examples/cards/glossary.toml
```

Everything generated — video, audio, cards — goes to `~/Movies/reelkit/`
(override with `REELKIT_OUTPUT`), never into the repository. A test fails if a
media file is ever tracked.

The Enhanced/Premium Apple voices sound much more natural than the compact
defaults. Download them in *System Settings → Accessibility → Spoken Content →
System Voice → Manage Voices*.

## Writing an episode

An episode is a folder with two files:

- **`script.toml`** — the narration, one segment per on-screen beat. Editable
  without touching code.
- **`scene.py`** — a `VoiceScene` that shows each beat while its segment plays.

```python
self.vo("hook")                 # the "hook" line starts now
self.play(Write(title))         # animate while it plays
self.hold()                     # wait for the line to finish
self.hold(pad=-0.6)             # …or return early to land on its last word
```

If the script changes after the audio was generated, rendering stops and asks
you to regenerate it, so picture and narration can't drift apart. A test checks
that every segment in the script is used by the scene and vice versa.

## Tests

```bash
.venv/bin/pytest
```

## License

MIT — see [LICENSE](LICENSE).
