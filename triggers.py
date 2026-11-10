import random
import subprocess
import time
from datetime import datetime

import psutil
from PyQt5.QtCore import QObject, QTimer, pyqtSignal

from config import (POLL_MS, SPOTIFY_PROC, CPU_THRESHOLD,
                    NIGHT_START, NIGHT_END)


class Triggers(QObject):
    triggered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._prev = {}
        self._last_event_time = time.monotonic()
        self.detectors = [
            ("music", self._music_playing, "music"),
            ("night", self._late_night,    "late_night"),
            ("busy",  self._high_cpu,      "busy"),
            ("battery_low", self._battery_low, "battery_low"),
            ("charging", self._battery_charging, "charging"),
        ]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check)
        self.timer.start(POLL_MS)

    def set_paused(self, paused):
        if paused:
            self.timer.stop()
        else:
            self.timer.start(POLL_MS)

    def check(self):
        fired = False
        for key, detect, event_name in self.detectors:
            now = bool(detect())
            if now and not self._prev.get(key, False):
                self.triggered.emit(event_name)
                self._last_event_time = time.monotonic()
                fired = True
            self._prev[key] = now

        if not fired and (time.monotonic() - self._last_event_time > 240):
            if random.random() < 0.15:
                self.triggered.emit("idle_thought")
                self._last_event_time = time.monotonic()

    def _music_playing(self):
        try:
            return subprocess.run(
                ["pgrep", "-i", SPOTIFY_PROC],
                capture_output=True,
            ).returncode == 0
        except FileNotFoundError:
            return False

    def _late_night(self):
        hour = datetime.now().hour
        if NIGHT_START <= NIGHT_END:
            return NIGHT_START <= hour < NIGHT_END
        return hour >= NIGHT_START or hour < NIGHT_END

    def _high_cpu(self):
        return psutil.cpu_percent() >= CPU_THRESHOLD

    def _battery_low(self):
        try:
            b = psutil.sensors_battery()
            if b is not None and not b.power_plugged and b.percent <= 20:
                return True
        except Exception:
            pass
        return False

    def _battery_charging(self):
        try:
            b = psutil.sensors_battery()
            if b is not None and b.power_plugged:
                return True
        except Exception:
            pass
        return False
