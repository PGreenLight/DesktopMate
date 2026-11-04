# DesktopMate

A customizable, lightweight desktop companion built with Python and PyQt5.

## Features

- **Cross-WM Compatibility**: Runs seamlessly on X11 (floating & tiling like i3, bspwm, dwm) and Wayland (via XWayland).
- **Interactive Animations**: Idle breathing, talking, dragging (grabbed), and falling reactions.
- **Senses & Triggers**: Reacts to system load, time of day, and music playback.
- **Multiple Companions**: Choose between Cat, Dog, Alien, and Robot with unique pixel-art animations.
- **Control & Settings UI**: Interactive Settings dialog accessible from the system tray or right-click menu, companion look switcher, toggleable pause, and autostart on login.

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
