# GBuddy ●
**Your calm hotspot companion.**

GBuddy is a premium desktop utility designed to protect your mobile data when using a phone hotspot on your laptop. It provides real-time tracking, a gentle mascot companion, and automatic protection features.

![GBuddy Icon](icon.png)

## Features
- **Real-time Tracking:** See exactly how much data your laptop is consuming.
- **Safe Limit:** Set a custom limit in GB; GBuddy will warn you before you hit it.
- **Auto-Disconnect:** Automatically turn off WiFi on Linux when your limit is reached to save data.
- **Premium Design:** Modern, minimal UI with smooth animations and a friendly mascot.
- **Autostart:** Optionally start with your laptop to keep protection always active.

## Installation

### From Source
1. Clone the repository.
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python main.py
   ```

### Build Standalone (Linux/Windows)
Run the build script to create a single executable:
```bash
python build.py
```
Check the `dist/` folder for the `GBuddy` executable.

## How it Works
GBuddy monitors your network interface counters using `psutil`. It calculates the delta since the session started and compares it against your chosen "Safe Limit". 

On Linux, it uses `nmcli` to safely toggle the WiFi radio if the auto-protect feature is enabled.

## Platforms
- **Linux:** Full support (including Auto-disconnect).
- **Windows/macOS:** Tracking supported; Auto-disconnect coming soon.

---
Crafted with precision by Luka Karchava.
