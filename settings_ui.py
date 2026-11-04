import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QSpinBox, QCheckBox, QPushButton, QLabel, QGroupBox
)
from PyQt5.QtCore import Qt

import config
import autostart


class SettingsDialog(QDialog):
    def __init__(self, mate=None, triggers=None, parent=None):
        super().__init__(parent)
        self.mate = mate
        self.triggers = triggers

        self.setWindowTitle("Desktop Mate Settings")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(320)

        main_layout = QVBoxLayout(self)

        appearance_group = QGroupBox("Appearance")
        app_layout = QFormLayout(appearance_group)

        self.scale_spin = QSpinBox()
        self.scale_spin.setRange(1, 10)
        self.scale_spin.setValue(config.SCALE)
        app_layout.addRow("Sprite Scale:", self.scale_spin)

        main_layout.addWidget(appearance_group)

        behavior_group = QGroupBox("Behavior & Senses")
        beh_layout = QFormLayout(behavior_group)

        self.cooldown_spin = QSpinBox()
        self.cooldown_spin.setRange(1, 120)
        self.cooldown_spin.setSuffix(" s")
        self.cooldown_spin.setValue(config.TALK_COOLDOWN_S)
        beh_layout.addRow("Speech Cooldown:", self.cooldown_spin)

        self.cpu_spin = QSpinBox()
        self.cpu_spin.setRange(10, 100)
        self.cpu_spin.setSuffix(" %")
        self.cpu_spin.setValue(config.CPU_THRESHOLD)
        beh_layout.addRow("CPU Alert Threshold:", self.cpu_spin)

        self.night_start_spin = QSpinBox()
        self.night_start_spin.setRange(0, 23)
        self.night_start_spin.setSuffix(":00")
        self.night_start_spin.setValue(config.NIGHT_START)
        beh_layout.addRow("Late Night Start:", self.night_start_spin)

        self.night_end_spin = QSpinBox()
        self.night_end_spin.setRange(0, 23)
        self.night_end_spin.setSuffix(":00")
        self.night_end_spin.setValue(config.NIGHT_END)
        beh_layout.addRow("Late Night End:", self.night_end_spin)

        self.poll_spin = QSpinBox()
        self.poll_spin.setRange(500, 30000)
        self.poll_spin.setSingleStep(500)
        self.poll_spin.setSuffix(" ms")
        self.poll_spin.setValue(config.POLL_MS)
        beh_layout.addRow("Sense Poll Rate:", self.poll_spin)

        main_layout.addWidget(behavior_group)

        system_group = QGroupBox("System")
        sys_layout = QVBoxLayout(system_group)
        self.autostart_check = QCheckBox("Start on login")
        self.autostart_check.setChecked(autostart.is_enabled())
        sys_layout.addWidget(self.autostart_check)

        main_layout.addWidget(system_group)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.save_btn = QPushButton("Save")
        self.save_btn.setDefault(True)
        self.save_btn.clicked.connect(self.save)
        btn_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(btn_layout)

    def save(self):
        new_scale = self.scale_spin.value()
        new_cooldown = self.cooldown_spin.value()
        new_cpu = self.cpu_spin.value()
        new_night_start = self.night_start_spin.value()
        new_night_end = self.night_end_spin.value()
        new_poll = self.poll_spin.value()

        config.SCALE = new_scale
        config.DISPLAY_SIZE = config.SPRITE_SIZE * new_scale
        config.TALK_COOLDOWN_S = new_cooldown
        config.CPU_THRESHOLD = new_cpu
        config.NIGHT_START = new_night_start
        config.NIGHT_END = new_night_end
        config.POLL_MS = new_poll

        config.save_user_settings({
            "SCALE": new_scale,
            "TALK_COOLDOWN_S": new_cooldown,
            "CPU_THRESHOLD": new_cpu,
            "NIGHT_START": new_night_start,
            "NIGHT_END": new_night_end,
            "POLL_MS": new_poll,
        })

        autostart.set_enabled(self.autostart_check.isChecked())

        if self.mate:
            self.mate.apply_scale()

        if self.triggers:
            self.triggers.timer.setInterval(new_poll)

        self.accept()


_settings_instance = None


def open_settings(mate=None, triggers=None):
    global _settings_instance
    if _settings_instance is None or not _settings_instance.isVisible():
        _settings_instance = SettingsDialog(mate=mate, triggers=triggers)
        _settings_instance.show()
    else:
        _settings_instance.activateWindow()
        _settings_instance.raise_()
