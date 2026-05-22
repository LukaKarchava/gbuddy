"""Optional WiFi off when safe hotspot limit is reached."""

import platform
import subprocess


def disable_wifi():
    """Try to turn off WiFi. Returns True if a command ran."""
    system = platform.system()
    try:
        if system == "Linux":
            r = subprocess.run(
                ["nmcli", "radio", "wifi", "off"],
                capture_output=True,
                timeout=8,
            )
            return r.returncode == 0
        if system == "Windows":
            r = subprocess.run(
                [
                    "netsh",
                    "interface",
                    "set",
                    "interface",
                    "Wi-Fi",
                    "admin=disable",
                ],
                capture_output=True,
                timeout=8,
                shell=True,
            )
            return r.returncode == 0
        if system == "Darwin":
            r = subprocess.run(
                ["networksetup", "-setairportpower", "en0", "off"],
                capture_output=True,
                timeout=8,
            )
            return r.returncode == 0
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        pass
    return False
