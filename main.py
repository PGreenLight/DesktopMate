import os
import sys

if "QT_QPA_PLATFORM" not in os.environ and (
    os.environ.get("XDG_SESSION_TYPE") == "wayland" or "WAYLAND_DISPLAY" in os.environ
):
    os.environ["QT_QPA_PLATFORM"] = "xcb"

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon

from mate import Mate
from triggers import Triggers
from actions import Launcher
from tray import build_tray


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("DesktopMate")
    app.setQuitOnLastWindowClosed(False)

    triggers = Triggers()
    launcher = Launcher()

    mate = Mate()
    triggers.triggered.connect(mate.on_event)
    mate.setup_context_menu(app, triggers, launcher)
    mate.show()

    tray = None
    if QSystemTrayIcon.isSystemTrayAvailable():
        tray = build_tray(app, mate, triggers, launcher)
    else:
        print("No system tray available - right click her or press Q to quit.")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
