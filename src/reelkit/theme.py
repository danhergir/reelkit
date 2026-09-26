"""The visual language shared by videos and cards."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    bg: str = "#0B0E14"
    fg: str = "#E6EDF3"
    dim: str = "#93A1B1"
    muted: str = "#6E7A8A"
    accent: str = "#58A6FF"
    good: str = "#56D07F"
    bad: str = "#F0766B"
    warn: str = "#E3B341"
    track: str = "#1C2430"
    panel: str = "#111722"
    mono: str = "Menlo"
    sans: str = "Helvetica Neue"

    def color(self, name: str) -> str:
        """Resolve a role name ("accent", "good", ...) or pass a hex color through."""
        return name if name.startswith("#") else getattr(self, name)


DEFAULT = Theme()
