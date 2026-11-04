# DesktopMate

A customizable, lightweight desktop companion built with Python and PyQt5.

## Features

- **Cross-WM Compatibility**: Runs seamlessly on X11 (floating & tiling like i3, bspwm, dwm) and Wayland (via XWayland).
- **Interactive Animations**: Idle breathing, talking, dragging (grabbed), and falling reactions.
- **Senses & Triggers**: Reacts to system load, time of day, and music playback.
- **Control**: System tray icon with toggleable pause, autostart on login, and direct on-sprite right-click context menu fallback.

## Requirements

- Python 3.8+
- PyQt5
- Pillow
- psutil

Install dependencies:
```bash
pip install PyQt5 Pillow psutil
```

## Running

Generate or rebuild the spritesheet:
```bash
python3 gen_sprite.py
```

Launch DesktopMate:
```bash
python3 main.py
```
