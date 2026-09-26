# Local Keylogger

Simple local keylogger for **Windows and Linux**, built with Python and `pynput`.

## Requirements

* Python 3.7+
* `pynput`

## Windows

Install:

```powershell
py -m pip install pynput
```

Run:

```powershell
py windows.py
```

Press **ESC** to stop.

## Linux

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pynput
```

Run:

```bash
python3 linux.py
```

Press **ESC** to stop.

Check your Linux session:

```bash
echo $XDG_SESSION_TYPE
```

`pynput` generally supports global keyboard monitoring on **X11**. Global
keyboard capture may not work under **Wayland**.

## Output

Keystrokes are saved locally to:

```text
logs.txt
```

The file is created automatically when the first keystroke is recorded.
