import shutil
import subprocess
import time

from config import LAUNCH_COOLDOWN_S


class Launcher:
    def __init__(self, cooldown_s=LAUNCH_COOLDOWN_S):
        self.cooldown = cooldown_s
        self._last = {}

    def launch(self, cmd):
        program = cmd[0]
        if shutil.which(program) is None:
            return False
        now = time.monotonic()
        if now - self._last.get(program, 0) < self.cooldown:
            return False
        self._last[program] = now
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        return True
