"""App-wide constants and paths."""

from pathlib import Path

APP_NAME = "GBuddy"
APP_TAGLINE = "your internet companion"
APP_DIR = Path(__file__).resolve().parent.parent
SESSION_GOAL_MB = 500
MILESTONE_PERCENTS = [25, 50, 75, 100]

# Typography stack (falls back gracefully per OS)
FONT_DISPLAY = ("SF Pro Display", "Segoe UI Variable Display", "Segoe UI", "Helvetica Neue")
FONT_BODY = ("SF Pro Text", "Segoe UI Variable Text", "Segoe UI", "Helvetica Neue")
FONT_MONO = ("SF Mono", "Cascadia Mono", "Consolas")
