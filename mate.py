import random
import time

from PyQt5.QtWidgets import QWidget, QApplication, QMenu
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint

import config
from config import (SPRITE_SIZE, FALL_MS, REACT_MS, TALK_COOLDOWN_S)
from states import STATES, DEFAULT
from dialogue import SpeechBubble, pick_line
import autostart
from settings_ui import open_settings


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
        self.setFixedSize(config.DISPLAY_SIZE, config.DISPLAY_SIZE)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)

        self.frames = []
        self.load_sheet()
        self.state = None
        self.row = 0
        self.frame = 0

        self.paused = False
        self.sleeping = False
        self._last_spoke = 0.0
        self._last_active = time.monotonic()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.set_state(DEFAULT)

        self.bubble = SpeechBubble()
        self.menu_app = None
        self.triggers = None
        self.launcher = None

        self._pet_history = []
        self._drag_history = []

        self.toss_vx = 0.0
        self.toss_vy = 0.0
        self.tossing = False
        self.physics_timer = QTimer(self)
        self.physics_timer.timeout.connect(self._physics_tick)

        self.wander_target_x = None
        self.wander_step_timer = QTimer(self)
        self.wander_step_timer.timeout.connect(self._wander_step)

        self.idle_check_timer = QTimer(self)
        self.idle_check_timer.timeout.connect(self._idle_check)
        self.idle_check_timer.start(5000)

        self.move(600, 600)

    def apply_scale(self):
        self.setFixedSize(config.DISPLAY_SIZE, config.DISPLAY_SIZE)
        self.update_mask_and_paint()
        if self.bubble.isVisible():
            self.bubble.reposition(self)

    def set_companion(self, name):
        config.COMPANION = name
        config.SPRITESHEET = config.get_spritesheet(name)
        config.save_user_settings({"COMPANION": name})
        self.load_sheet()
        self.update_mask_and_paint()

    def setup_context_menu(self, app, triggers, launcher):
        self.menu_app = app
        self.triggers = triggers
        self.launcher = launcher

    def contextMenuEvent(self, event):
        if not self.menu_app:
            return
        self.wake_up()
        menu = QMenu(self)

        comp_menu = menu.addMenu("Companion")
        for comp in config.COMPANIONS:
            act = comp_menu.addAction(comp.capitalize())
            act.setCheckable(True)
            act.setChecked(config.COMPANION.lower() == comp)
            act.triggered.connect(lambda checked, c=comp: self.set_companion(c))

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

        settings_action = menu.addAction("Settings...")
        settings_action.triggered.connect(lambda: open_settings(mate=self, triggers=self.triggers))

        menu.addSeparator()
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(self.menu_app.quit)

        menu.exec_(event.globalPos())

    def set_state(self, name):
        if name == self.state and not self.sleeping:
            return
        spec = STATES[name]
        self.state = name
        self.row = spec["row"]
        self.frame = 0
        if not self.paused and not self.sleeping:
            self.timer.start(max(1, 1000 // spec["fps"]))
        self.update_mask_and_paint()

    def load_sheet(self, sheet_path=None):
        target = sheet_path or config.get_spritesheet()
        sheet = QPixmap(str(target))
        if sheet.isNull():
            raise FileNotFoundError(
                f"Could not load {target}. Run: python3 gen_sprite.py"
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
        if self.sleeping:
            return
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
        scaled = pixmap.scaled(config.DISPLAY_SIZE, config.DISPLAY_SIZE, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.setMask(scaled.mask())
        self.update()

    def keyPressEvent(self, event):
        self.wake_up()
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
        self.wake_up()
        if self.tossing:
            self.physics_timer.stop()
            self.tossing = False
        if self.wander_step_timer.isActive():
            self.wander_step_timer.stop()

        if event.button() == Qt.LeftButton:
            self.drag_offset = event.pos()
            self._drag_history = [(time.monotonic(), event.globalPos().x(), event.globalPos().y())]
            self.set_state("grabbed")

    def mouseMoveEvent(self, event):
        now = time.monotonic()
        self._last_active = now

        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_offset)
            if self.bubble.isVisible():
                self.bubble.reposition(self)
            self._drag_history.append((now, event.globalPos().x(), event.globalPos().y()))
            if len(self._drag_history) > 6:
                self._drag_history.pop(0)
        else:
            self._check_pet(event.pos().x())

    def _check_pet(self, current_x):
        now = time.monotonic()
        self._pet_history.append((now, current_x))
        self._pet_history = [(t, x) for t, x in self._pet_history if now - t <= 1.0]

        if len(self._pet_history) >= 6:
            reversals = 0
            dx_total = 0
            last_dir = 0
            for i in range(1, len(self._pet_history)):
                diff = self._pet_history[i][1] - self._pet_history[i - 1][1]
                dx_total += abs(diff)
                current_dir = 1 if diff > 2 else (-1 if diff < -2 else 0)
                if current_dir != 0 and current_dir != last_dir:
                    if last_dir != 0:
                        reversals += 1
                    last_dir = current_dir

            if reversals >= 3 and dx_total >= 60:
                self._pet_history.clear()
                self.on_pet()

    def on_pet(self):
        self.wake_up()
        if self.state in ("grabbed", "falling") or self.tossing:
            return
        self.say("pet")

    def mouseReleaseEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        now = time.monotonic()
        vx, vy = 0.0, 0.0
        if len(self._drag_history) >= 2:
            old_t, old_x, old_y = self._drag_history[0]
            dt = now - old_t
            if 0.01 <= dt <= 0.25:
                cur_x, cur_y = event.globalPos().x(), event.globalPos().y()
                vx = (cur_x - old_x) / (dt * 60)
                vy = (cur_y - old_y) / (dt * 60)
                vx = max(-35.0, min(35.0, vx))
                vy = max(-35.0, min(35.0, vy))

        self._drag_history.clear()

        if abs(vx) > 4.0 or abs(vy) > 4.0:
            self.toss_vx = vx
            self.toss_vy = vy
            self.tossing = True
            self.set_state("falling")
            self.say("tossed")
            self.physics_timer.start(16)
        else:
            self.set_state("falling")
            QTimer.singleShot(FALL_MS, self._land)

    def _physics_tick(self):
        if not self.tossing:
            self.physics_timer.stop()
            return

        screen = QApplication.primaryScreen().availableGeometry()
        x = self.x() + int(self.toss_vx)
        y = self.y() + int(self.toss_vy)

        self.toss_vy += 0.8
        self.toss_vx *= 0.985

        if x < screen.left():
            x = screen.left()
            self.toss_vx = -self.toss_vx * 0.65
        elif x + config.DISPLAY_SIZE > screen.right():
            x = screen.right() - config.DISPLAY_SIZE
            self.toss_vx = -self.toss_vx * 0.65

        if y < screen.top():
            y = screen.top()
            self.toss_vy = -self.toss_vy * 0.65
        elif y + config.DISPLAY_SIZE >= screen.bottom():
            y = screen.bottom() - config.DISPLAY_SIZE
            self.toss_vy = -self.toss_vy * 0.5
            self.toss_vx *= 0.8
            if abs(self.toss_vy) < 2.0 and abs(self.toss_vx) < 1.5:
                self.tossing = False
                self.physics_timer.stop()
                self._land()

        self.move(x, y)
        if self.bubble.isVisible():
            self.bubble.reposition(self)

    def _land(self):
        if self.state == "falling" and not self.tossing:
            self.set_state("idle")

    def _idle_check(self):
        if self.paused or self.tossing or self.state != "idle":
            return

        now = time.monotonic()
        if config.ALLOW_SLEEP and not self.sleeping and (now - self._last_active > config.SLEEP_IDLE_S):
            self.sleeping = True
            self.timer.stop()
            self.row = 0
            self.frame = 3
            self.update_mask_and_paint()
            self.say("sleep")
            return

        if config.ALLOW_WANDER and not self.sleeping and not self.wander_step_timer.isActive():
            if random.random() < 0.35:
                self._start_wander()

    def _start_wander(self):
        screen = QApplication.primaryScreen().availableGeometry()
        dist = random.choice([-1, 1]) * random.randint(60, 160)
        target = self.x() + dist
        target = max(screen.left() + 10, min(screen.right() - config.DISPLAY_SIZE - 10, target))
        if abs(target - self.x()) > 15:
            self.wander_target_x = target
            self.wander_step_timer.start(30)

    def _wander_step(self):
        if self.wander_target_x is None or self.state != "idle" or self.sleeping or self.paused:
            self.wander_step_timer.stop()
            return

        dx = self.wander_target_x - self.x()
        if abs(dx) <= 3:
            self.move(self.wander_target_x, self.y())
            self.wander_step_timer.stop()
            self.wander_target_x = None
            if self.bubble.isVisible():
                self.bubble.reposition(self)
            return

        step = 3 if dx > 0 else -3
        self.move(self.x() + step, self.y())
        if self.bubble.isVisible():
            self.bubble.reposition(self)

    def wake_up(self):
        self._last_active = time.monotonic()
        if self.sleeping:
            self.sleeping = False
            self.set_state("idle")
            self.say("wake")

    def on_event(self, name):
        if self.state in ("grabbed", "falling") or self.tossing:
            return
        self.wake_up()
        self.say(name)

    def say(self, event):
        now = time.monotonic()
        if event not in ("pet", "tossed", "wake", "sleep") and (now - self._last_spoke < config.TALK_COOLDOWN_S):
            return
        line = pick_line(event, config.COMPANION)
        if line is None:
            return
        self._last_spoke = now
        if not self.sleeping and not self.tossing and self.state != "grabbed":
            self.set_state("talk")
            QTimer.singleShot(REACT_MS, self._calm)
        self.bubble.show_text(line, anchor=self)

    def _calm(self):
        if self.state == "talk" and not self.sleeping and not self.tossing:
            self.set_state("idle")

    def set_paused(self, paused):
        self.paused = paused
        if paused:
            self.timer.stop()
            self.physics_timer.stop()
            self.wander_step_timer.stop()
        else:
            if not self.sleeping:
                self.timer.start(max(1, 1000 // STATES[self.state]["fps"]))

    def paintEvent(self, event):
        pixmap = self.frames[self.row][self.frame]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, False)
        target = QRect(0, 0, config.DISPLAY_SIZE, config.DISPLAY_SIZE)
        source = QRect(0, 0, SPRITE_SIZE, SPRITE_SIZE)
        painter.drawPixmap(target, pixmap, source)
