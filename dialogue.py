import random

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer

from config import BUBBLE_MS

LINES = {
    "music": [
        "it's music time! 🎶",
        "ooh, is that Spotify?",
        "turn it up~",
    ],
    "late_night": [
        "it's getting late...",
        "you should sleep soon 💤",
        "time to work!",
    ],
    "busy": [
        "whoa, your CPU is sweating!",
        "lots going on, huh?",
        "I can hear the fans spinning!",
        "it dosen't feel green"
    ],
}


def pick_line(event):
    pool = LINES.get(event)
    return random.choice(pool) if pool else None


class SpeechBubble(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        self.label = QLabel()
        self.label.setWordWrap(True)
        self.label.setMaximumWidth(200)
        self.label.setStyleSheet(
            "background: rgba(255, 255, 255, 235);"
            "color: #2b2b3a;"
            "border: 2px solid #7fb4e6;"
            "border-radius: 10px;"
            "padding: 6px 10px;"
            "font-size: 13px;"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hide)

    def reposition(self, anchor):
        ax = anchor.x() + anchor.width() // 2 - self.width() // 2
        ay = anchor.y() - self.height() - 8
        self.move(ax, max(0, ay))

    def show_text(self, text, anchor):
        self.label.setText(text)
        self.adjustSize()
        self.reposition(anchor)
        self.show()
        self.raise_()
        self._hide_timer.start(BUBBLE_MS)
