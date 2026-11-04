from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon

import autostart


def build_tray(app, mate, triggers, launcher):
    icon = QIcon(mate.frames[0][0])
    tray = QSystemTrayIcon(icon)
    tray.setToolTip("Desktop Mate")

    menu = QMenu()

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

    menu.addSeparator()
    quit_item = menu.addAction("Quit")
    quit_item.triggered.connect(app.quit)

    tray.setContextMenu(menu)
    tray.show()
    return tray, menu
