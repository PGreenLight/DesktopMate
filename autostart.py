import sys
from pathlib import Path

from config import ROOT

AUTOSTART_DIR = Path.home() / ".config" / "autostart"
DESKTOP_FILE = AUTOSTART_DIR / "desktop-mate.desktop"


def _entry_text():
    python = sys.executable
    main_py = ROOT / "main.py"
    return (
        "[Desktop Entry]\n"
        "Type=Application\n"
        "Name=Desktop Mate\n"
        f"Exec={python} {main_py}\n"
        "X-GNOME-Autostart-enabled=true\n"
    )


def is_enabled():
    return DESKTOP_FILE.exists()


def enable():
    AUTOSTART_DIR.mkdir(parents=True, exist_ok=True)
    DESKTOP_FILE.write_text(_entry_text())


def disable():
    DESKTOP_FILE.unlink(missing_ok=True)


def set_enabled(on):
    enable() if on else disable()
