"""reelkit command line.

    reelkit voices [--locale es_]
    reelkit voice  EPISODE --voice NAME [--rate WPM]
    reelkit render EPISODE [--voice NAME] [--rate WPM] [--draft]
    reelkit card   SPEC.toml [-o OUT.png]
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from .script import load_script, output_root


def cmd_voices(args):
    from .voice.macos import list_voices
    for name in list_voices(args.locale):
        print(name)


def cmd_voice(args):
    from .voice.macos import synthesize
    script = load_script(args.episode)
    print(f"voiceover → {script.audio_dir}")
    synthesize(script.segments, script.audio_dir, args.voice, args.rate)


def cmd_render(args):
    script = load_script(args.episode)
    if args.voice:
        cmd_voice(args)
    media = script.media_dir
    env = {**os.environ, "REELKIT_DRAFT": "1" if args.draft else "0"}
    name = f"{script.slug}-draft" if args.draft else script.slug
    cmd = [sys.executable, "-m", "manim", "render", str(script.root / "scene.py"), script.scene,
           "-o", name, "--media_dir", str(media), "--progress_bar", "none"]
    print("render →", " ".join(cmd[3:]))
    subprocess.run(cmd, check=True, env=env, cwd=script.root)

    rendered = max(media.rglob(f"{name}.mp4"), key=lambda p: p.stat().st_mtime)
    out = script.work_dir / f"{name}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(rendered, out)
    print(f"done → {out}")


def cmd_card(args):
    from .cards import load_card, render_card
    spec_path = Path(args.spec)
    out = Path(args.output) if args.output else output_root() / "cards" / f"{spec_path.stem}.png"
    print(f"card → {render_card(load_card(spec_path), out)}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="reelkit", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    v = sub.add_parser("voices", help="list installed macOS voices")
    v.add_argument("--locale", default="", help='filter by locale prefix, e.g. "es_"')
    v.set_defaults(func=cmd_voices)

    for name, func, needs_voice in (("voice", cmd_voice, True), ("render", cmd_render, False)):
        s = sub.add_parser(name, help=f"{name} an episode directory")
        s.add_argument("episode")
        s.add_argument("--voice", required=needs_voice, help='e.g. "Paulina (Premium)"')
        s.add_argument("--rate", type=int, default=195, help="words per minute")
        if name == "render":
            s.add_argument("--draft", action="store_true", help="half resolution, 15 fps")
        s.set_defaults(func=func)

    c = sub.add_parser("card", help="render a static card from a TOML spec")
    c.add_argument("spec")
    c.add_argument("-o", "--output")
    c.set_defaults(func=cmd_card)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
