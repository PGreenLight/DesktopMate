from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon

import autostart
import config
from settings_ui import open_settings


def build_tray(app, mate, triggers, launcher):
    icon = QIcon(mate.frames[0][0])
    tray = QSystemTrayIcon(icon)
    tray.setToolTip("Desktop Mate")

    menu = QMenu()

    comp_menu = menu.addMenu("Companion")
    comp_actions = {}

    def choose_companion(c):
        mate.set_companion(c)
        tray.setIcon(QIcon(mate.frames[0][0]))
        for name, act in comp_actions.items():
            act.setChecked(name == c)

    for comp in config.COMPANIONS:
        act = comp_menu.addAction(comp.capitalize())
        act.setCheckable(True)
        act.setChecked(config.COMPANION.lower() == comp)
        act.triggered.connect(lambda checked, c=comp: choose_companion(c))
        comp_actions[comp] = act

    pause = menu.addAction("Pause")
    pause.setCheckable(True)

    def on_pause(checked):
        mate.set_paused(checked)
        triggers.set_paused(checked)

    pause.toggled.connect(on_pause)

    launch = menu.addAction("Launch Spotify")
    launch.triggered.connect(lambda: launcher.launch(["spotify"]))

    boot = menu.addAction("Start on login")
    boot.setCheckable(True)
    boot.setChecked(autostart.is_enabled())
    boot.toggled.connect(autostart.set_enabled)

    settings_item = menu.addAction("Settings...")
    settings_item.triggered.connect(lambda: open_settings(mate=mate, triggers=triggers))

    update_item = menu.addAction("Check for Updates...")
    update_item.triggered.connect(lambda: open_settings(mate=mate, triggers=triggers, check_updates=True))

    menu.addSeparator()
    quit_item = menu.addAction("Quit")
    quit_item.triggered.connect(app.quit)

    tray.setContextMenu(menu)
    tray.show()
    return tray, menu
