#!/usr/bin/env python3
"""GBuddy entry point — run this file to start the app."""

import sys
from pathlib import Path

# Allow running from project folder without installing package
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gbuddy.ui.app_window import GBuddyApp


def main():
    app = GBuddyApp()
    app.mainloop()


if __name__ == "__main__":
    main()
