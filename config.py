import json
from pathlib import Path

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
SPRITESHEET = ASSETS / "spritesheet.png"

CONFIG_DIR = Path.home() / ".config" / "desktop-mate"
CONFIG_FILE = CONFIG_DIR / "settings.json"

SPRITE_SIZE = 32
SCALE = 4
TICK_MS = 100

FALL_MS = 450
REACT_MS = 2500
BUBBLE_MS = 5000
TALK_COOLDOWN_S = 8
LAUNCH_COOLDOWN_S = 30

POLL_MS = 3000
SPOTIFY_PROC = "spotify"
CPU_THRESHOLD = 90
NIGHT_START = 23
NIGHT_END = 5


def _load_user_settings():
    if not CONFIG_FILE.exists():
        return
    try:
        data = json.loads(CONFIG_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return
    g = globals()
    for key, value in data.items():
        name = key.upper()
        if name in g and not name.startswith("_") and name.isupper():
            g[name] = value


_load_user_settings()

DISPLAY_SIZE = SPRITE_SIZE * SCALE
