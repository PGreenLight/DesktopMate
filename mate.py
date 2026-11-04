import time

from PyQt5.QtWidgets import QWidget, QApplication, QMenu
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QTimer, QRect

from config import (SPRITESHEET, SPRITE_SIZE, DISPLAY_SIZE,
                    FALL_MS, REACT_MS, TALK_COOLDOWN_S)
from states import STATES, DEFAULT
from dialogue import SpeechBubble, pick_line
import autostart


class Mate(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(DISPLAY_SIZE, DISPLAY_SIZE)
        self.setFocusPolicy(Qt.StrongFocus)

        self.frames = []
        self.load_sheet()
        self.state = None
        self.row = 0
        self.frame = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.set_state(DEFAULT)

        self.bubble = SpeechBubble()
        self._last_spoke = 0.0

        self.menu_app = None
        self.triggers = None
        self.launcher = None
        self.paused = False

        self.move(600, 600)

    def setup_context_menu(self, app, triggers, launcher):
        self.menu_app = app
        self.triggers = triggers
        self.launcher = launcher

    def contextMenuEvent(self, event):
        if not self.menu_app:
            return
        menu = QMenu(self)

        pause_action = menu.addAction("Pause")
        pause_action.setCheckable(True)
        pause_action.setChecked(self.paused)

        def toggle_pause(checked):
            self.paused = checked
            self.set_paused(checked)
            if self.triggers:
                self.triggers.set_paused(checked)

        pause_action.toggled.connect(toggle_pause)

        launch_action = menu.addAction("Launch Spotify")
        if self.launcher:
            launch_action.triggered.connect(lambda: self.launcher.launch(["spotify"]))

        boot_action = menu.addAction("Start on login")
        boot_action.setCheckable(True)
        boot_action.setChecked(autostart.is_enabled())
        boot_action.toggled.connect(autostart.set_enabled)

        menu.addSeparator()
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(self.menu_app.quit)

        menu.exec_(event.globalPos())

    def set_state(self, name):
        if name == self.state:
            return
        spec = STATES[name]
        self.state = name
        self.row = spec["row"]
        self.frame = 0
        self.timer.start(max(1, 1000 // spec["fps"]))
        self.update_mask_and_paint()

    def load_sheet(self):
        sheet = QPixmap(str(SPRITESHEET))
        if sheet.isNull():
            raise FileNotFoundError(
                f"Could not load {SPRITESHEET}. Run: python3 gen_sprite.py"
            )
        rows = sheet.height() // SPRITE_SIZE
        cols = sheet.width() // SPRITE_SIZE
        self.frames = []
        for r in range(rows):
            row_frames = []
            for c in range(cols):
                cell = QRect(c * SPRITE_SIZE, r * SPRITE_SIZE,
                             SPRITE_SIZE, SPRITE_SIZE)
                row_frames.append(sheet.copy(cell))
            self.frames.append(row_frames)

    def tick(self):
        spec = STATES[self.state]
        count = spec["frame_count"]
        self.frame += 1
        if self.frame >= count:
            if spec["loop"]:
                self.frame = 0
            else:
                self.frame = count - 1
                self.timer.stop()
        self.update_mask_and_paint()

    def update_mask_and_paint(self):
        pixmap = self.frames[self.row][self.frame]
        scaled = pixmap.scaled(DISPLAY_SIZE, DISPLAY_SIZE, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.setMask(scaled.mask())
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            QApplication.quit()
            return
        keymap = {
            Qt.Key_1: "idle",
            Qt.Key_2: "talk",
            Qt.Key_3: "grabbed",
            Qt.Key_4: "falling",
        }
        name = keymap.get(event.key())
        if name:
            self.set_state(name)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_offset = event.pos()
            self.set_state("grabbed")

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_offset)
            if self.bubble.isVisible():
                self.bubble.reposition(self)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.set_state("falling")
            QTimer.singleShot(FALL_MS, self._land)

    def _land(self):
        if self.state == "falling":
            self.set_state("idle")

    def on_event(self, name):
        if self.state != "idle":
            return
        self.say(name)

    def say(self, event):
        now = time.monotonic()
        if now - self._last_spoke < TALK_COOLDOWN_S:
            return
        line = pick_line(event)
        if line is None:
            return
        self._last_spoke = now
        self.set_state("talk")
        self.bubble.show_text(line, anchor=self)
        QTimer.singleShot(REACT_MS, self._calm)

    def _calm(self):
        if self.state == "talk":
            self.set_state("idle")

    def set_paused(self, paused):
        self.paused = paused
        if paused:
            self.timer.stop()
        else:
            self.timer.start(max(1, 1000 // STATES[self.state]["fps"]))

    def paintEvent(self, event):
        pixmap = self.frames[self.row][self.frame]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, False)
        target = QRect(0, 0, DISPLAY_SIZE, DISPLAY_SIZE)
        source = QRect(0, 0, SPRITE_SIZE, SPRITE_SIZE)
        painter.drawPixmap(target, pixmap, source)
