"""
Simple local keylogger - logs your own keystrokes to logs.txt
Requires: pip install pynput

Press ESC to stop logging.
"""

from pynput import keyboard

LOG_FILE = "logs.txt"


def on_press(key):
    try:
        # Normal character keys (letters, numbers, symbols)
        char = key.char
    except AttributeError:
        # Special keys (Enter, Shift, Ctrl, etc.)
        char = f"[{key.name.upper()}]"

    # Enter gets a newline for readability
    if key == keyboard.Key.enter:
        char = "\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(char)
        f.flush()  # make sure it's written immediately


def on_release(key):
    if key == keyboard.Key.esc:
        print("\nESC pressed - stopping logger.")
        return False  # returning False stops the listener


def main():
    print(f"Logging keystrokes to '{LOG_FILE}'. Press ESC to stop.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
