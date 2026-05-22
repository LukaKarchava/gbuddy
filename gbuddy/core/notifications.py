"""Desktop notifications and startup registration."""

import subprocess
import sys
from pathlib import Path

from gbuddy.config import APP_DIR, APP_NAME


def notify(title, body):
    try:
        subprocess.run(
            ["notify-send", "-a", APP_NAME, title, body],
            check=False,
            timeout=3,
        )
    except (FileNotFoundError, OSError):
        pass


def autostart_path():
    return Path.home() / ".config" / "autostart" / "gbuddy.desktop"


def set_autostart(enabled):
    path = autostart_path()
    script = APP_DIR / "main.py"
    python = sys.executable

    if enabled:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"[Desktop Entry]\nType=Application\nName={APP_NAME}\n"
            f"Exec={python} {script}\nTerminal=false\n"
            "X-GNOME-Autostart-enabled=true\n",
            encoding="utf-8",
        )
    elif path.exists():
        path.unlink()
