# DesktopMate

A lightweight, reactive pixel-art desktop companion for Linux that lives on your screen, reacts to your system, and keeps you company while you work or game.

Built with Python and PyQt5, DesktopMate runs seamlessly across both floating and tiling window managers on X11 and Wayland.

---

## Companions

DesktopMate includes four built-in animated companions with unique pixel-art spritesheets and distinct personality dialogues:

- **Cat** (Default): An adorable cream kitten with twitching ears, red collar with a golden bell, sparkling eyes, and a swishing tail. Likes sleeping, purrs when petted, and offers sassy remarks.
- **Dog**: A playful caramel puppy with bouncy floppy ears, wagging tail, and happy panting expressions. Loves music, brings endless energy, and gives encouraging cheers.
- **Alien**: A cosmic visitor with an extraterrestrial spacesuit, starry eyes, and a glowing, pulsating antenna. Analyzes your terrestrial habits and monitors thermal emissions.
- **Robot**: A retro-futuristic metallic bot featuring animated cyan visor matrix eyes, dials, and rocket thruster sparks. Provides technical diagnostics and system load status.

You can switch between companions on the fly from the Settings dialog, the system tray, or the on-sprite right-click menu.

---

## Features

- **Interactive Physics & Animations**:
  - **Petting**: Rapidly move the cursor back and forth over your companion to pet them and trigger happy purrs, tail wags, and heart reactions!
  - **Fling & Toss Physics**: Pick up your companion and throw them across the screen! They fly with momentum, bounce off display edges, and land gracefully.
  - **Autonomous Wandering**: Companions occasionally take walks around your screen, stop, and look around.
  - **Idle Napping**: When your system sits idle for a while, your companion curls up and takes a peaceful nap until you wake them.
  - **Drag & Drop**: Click and hold anywhere on the companion to reposition them.
  - **Falling**: Smooth drop physics and startled expressions when released mid-air.
- **System Senses & Dynamic Dialogue**:
  - **Music**: Detects active music players like Spotify and reacts to your tunes.
  - **High CPU Load**: Warns you with companion-specific remarks when your machine is working hard.
  - **Battery & Power**: Alerts you when your laptop battery drops low (< 20%) and celebrates when plugged into power.
  - **Late Night Reminders**: Gently nudges you to get some sleep past midnight.
  - **Idle Thoughts**: Shares cute random thoughts and observations during quiet periods.
- **Broad Window Manager Compatibility**:
  - **Tiling WMs**: Uses bypass window hints so managers like i3, bspwm, dwm, and awesome never trap your companion in a tile grid.
  - **Wayland Support**: Automatic XWayland fallback ensures coordinate dragging, tossing, and placement work properly on Hyprland, Sway, GNOME Wayland, and KDE Wayland.
  - **Compositing Fallback**: Includes 1-bit transparency mask clipping for lightweight X11 environments running without a compositor (e.g., bare Openbox or IceWM without picom).
- **Settings & Control**:
  - **Graphical Settings UI**: Adjust sprite scale (1x to 10x), autonomous wandering, idle sleep, speech cooldown, CPU sensitivity, night hours, sense polling rates, and companion skins.
  - **System Tray & Context Menu**: Full control surface available both in the tray bar and via right-click on the sprite itself for trayless setups.
  - **One-Click Updates**: Built-in update checker in Settings and tray menus pulls the latest changes from GitHub and offers an instant restart.
  - **Start on Login**: One-click autostart configuration for standard desktop environments.

---

## Installation

### Prerequisites

- Linux (X11 or Wayland with XWayland)
- Python 3.8+

### Install Dependencies

```bash
pip install PyQt5 Pillow psutil
```

---

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/PGreenLight/DesktopMate.git
   cd DesktopMate
   ```

2. (Optional) Generate or regenerate all companion spritesheets:
   ```bash
   python3 gen_sprite.py
   ```

3. Launch DesktopMate:
   ```bash
   python3 main.py
   ```

---

## Controls

| Action | Control |
| :--- | :--- |
| **Pet** | Move cursor rapidly left and right over the companion |
| **Drag & Move** | Left-click and hold anywhere on the companion |
| **Throw / Toss** | Drag and quickly release with speed to fling across the screen |
| **Wake Up** | Click, pet, or drag a sleeping companion |
| **Open Menu** | Right-click the companion or system tray icon |
| **Settings** | Select **Settings...** in the context menu or tray |
| **Check for Updates** | Select **Check for Updates...** in the menu or Settings dialog |
| **Switch Companion** | Open **Companion** submenu in the tray or right-click menu |
| **Pause Animations/Senses** | Toggle **Pause** in the menu |
| **Quit** | Click **Quit** in the menu, or focus the window and press `Q` |
| **Manual Animation Test** | Focus the window and press `1` (Idle), `2` (Talk), `3` (Grabbed), `4` (Falling) |

---

## Configuration

Settings are saved automatically to `~/.config/desktop-mate/settings.json` when adjusted through the Settings UI.

Example configuration file:

```json
{
  "COMPANION": "cat",
  "SCALE": 4,
  "ALLOW_WANDER": true,
  "ALLOW_SLEEP": true,
  "CPU_THRESHOLD": 85,
  "NIGHT_START": 23,
  "NIGHT_END": 5,
  "TALK_COOLDOWN_S": 8,
  "POLL_MS": 3000
}
```

---

## Customization

- **Sprites**: Add or replace spritesheets in the `assets/` folder (`32x32` pixels per cell).
- **Lines**: Edit or add phrases in `dialogue.py` under the `COMPANION_LINES` dictionary.
- **Senses**: Add new system monitoring hooks in `triggers.py`.
