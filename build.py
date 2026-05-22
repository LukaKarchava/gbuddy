import os
import subprocess
import sys
import platform

def build():
    print("Preparing GBuddy build...")
    
    # Requirements
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    system = platform.system()
    icon_file = "icon.png"
    if system == "Windows":
        icon_file = "icon.ico"
    
    # Base command
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        f"--icon={icon_file}",
        "--add-data=gbuddy:gbuddy",
        "--add-data=icon.png:.",
    ]
    
    # Add customtkinter data if needed
    import customtkinter
    ctk_path = os.path.dirname(customtkinter.__file__)
    cmd.extend(["--add-data", f"{ctk_path}:customtkinter"])

    cmd.append("main.py")
    cmd.extend(["--name", "GBuddy"])

    print(f"Running build command: {' '.join(cmd)}")
    subprocess.check_call(cmd)
    print("\nBuild complete! Check the 'dist' folder.")

if __name__ == "__main__":
    build()
