import subprocess
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from config import ROOT


class UpdateWorker(QThread):
    finished = pyqtSignal(bool, bool, str)

    def run(self):
        try:
            fetch = subprocess.run(
                ["git", "fetch"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=15,
            )
            if fetch.returncode != 0:
                err = fetch.stderr.strip() or "Failed to connect to remote repository."
                self.finished.emit(False, False, err)
                return

            local_rev = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()

            remote_rev = subprocess.run(
                ["git", "rev-parse", "@{u}"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()

            if not local_rev or not remote_rev:
                self.finished.emit(False, False, "Could not resolve git branches.")
                return

            if local_rev == remote_rev:
                self.finished.emit(True, False, f"DesktopMate is up to date ({local_rev[:7]})")
                return

            pull = subprocess.run(
                ["git", "pull", "--ff-only"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=25,
            )
            if pull.returncode != 0:
                err = pull.stderr.strip() or pull.stdout.strip() or "Pull conflict or error."
                self.finished.emit(False, False, f"Pull failed: {err}")
                return

            subprocess.run(
                [sys.executable, str(ROOT / "gen_sprite.py")],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=10,
            )

            new_rev = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()

            self.finished.emit(True, True, f"Updated to {new_rev[:7]}! Restart to apply.")

        except subprocess.TimeoutExpired:
            self.finished.emit(False, False, "Update check timed out.")
        except Exception as e:
            self.finished.emit(False, False, f"Error: {str(e)}")


def restart_app():
    subprocess.Popen([sys.executable, str(ROOT / "main.py")])
    QApplication.quit()
