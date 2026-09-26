# Local Keylogger

A simple, cross-platform keylogger that records your own keystrokes to a local
file (`logs.txt`). Built with Python and [`pynput`](https://pypi.org/project/pynput/).

> **⚠️ Legal & Ethical Warning**
> This tool is intended **only** for personal use on machines you own, or for
> educational purposes in a controlled environment with **explicit consent**
> from the machine's owner. Unauthorized keylogging is **illegal** in most
> countries and a violation of privacy. Do not use it to spy on anyone.

---

## Features

- Logs all keystrokes to `logs.txt` in the current directory.
- Handles normal keys (letters, numbers, symbols) and special keys
  (Shift, Ctrl, Enter, Tab, etc.).
- Separate scripts for **Windows** and **Linux**.
- Auto-detects Wayland on Linux and warns the user.
- Press **ESC** to stop logging.
- Immediate flush to disk — nothing is lost if the script crashes.

---

## Files

| File | Platform | Description |
|------|----------|-------------|
| `windows.py` | Windows | Keylogger for Windows. |
| `linux.py`   | Linux (X11) | Keylogger for Linux. Detects Wayland and exits safely. |
| `logs.txt`   | Any | Output file, created automatically on first keystroke. |
| `README.md`  | Any | This file. |

---

## Requirements

- Python 3.7+
- `pynput`

Install the dependency:

```bash
pip install pynput
```

Or with `pip3` on Linux:

```bash
pip3 install pynput
```

---

## Usage

### Windows
```bash
git clone https://github.com/holyyyyyyyyyyyyyyyyyyyyyyyyy/keylogger/edit/main/windos.py
```
```powershell
python windows.py
```

Or with the Python launcher:

```powershell
py windows.py
```

### Linux (X11 only)
```bash
https://github.com/holyyyyyyyyyyyyyyyyyyyyyyyyy/keylogger/edit/main/linux.py
```
```bash
python3 linux.py
```

> **Wayland users:** `pynput` cannot capture global keystrokes on Wayland.
> Log out and select an **X11 / Xorg** session at the login screen, then run
> `linux.py` again. Check your current session with:
>
> ```bash
> echo $XDG_SESSION_TYPE
> ```

### Stopping the logger

- **Foreground mode:** press **ESC**, or **Ctrl+C** in the terminal.
- **Background mode:** see below.

---

## Running in the Background

### Windows

```powershell
powershell -Command "$p = Start-Process py -ArgumentList 'windows.py' -PassThru -WindowStyle Hidden; $p.Id > keylogger.pid"
```

Stop it:

```powershell
powershell -Command "Stop-Process -Id (Get-Content keylogger.pid) -Force"
```

Or kill all Python processes (less precise):

```powershell
taskkill /IM python.exe /F
taskkill /IM pythonw.exe /F
```

### Linux

```bash
nohup python3 linux.py >/dev/null 2>&1 & echo $! > keylogger.pid
```

Stop it:

```bash
kill $(cat keylogger.pid)
```

Or simply:

```bash
pkill -f linux.py
```

---

## Output

All keystrokes are written to `logs.txt` in the same folder as the script.
Example output:

```
hello world[SPACE]this is a test[ENTER]
[SHIFT]Capitalized[SPACE]text[ENTER]
```

Special keys are wrapped in `[BRACKETS]`. Regular characters appear as typed.

---

## How It Works

Both scripts use `pynput.keyboard.Listener`, which hooks into the operating
system's keyboard event stream:

- `on_press` → called every time a key is pressed; appends the character to
  `logs.txt`.
- `on_release` → called every time a key is released; if the key is `ESC`,
  it returns `False` to stop the listener.

`linux.py` additionally checks the `XDG_SESSION_TYPE` environment variable
before starting, because `pynput` cannot hook global keys under Wayland.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: pynput` | Run `pip install pynput`. |
| Nothing appears in `logs.txt` (Linux) | You're probably on Wayland. Switch to an X11 session. |
| Nothing appears in `logs.txt` (Windows) | Make sure the terminal window has focus, then click into another window and type. |
| Permission denied on Linux | Do **not** use `sudo` under X11 — it breaks the display connection. Run as your normal user. |
| `logs.txt` grows too large | Rotate or delete it manually. There is no auto-rotation. |

---

## Disclaimer

The author is **not responsible** for any misuse of this software. By using
this code, you agree to use it only on systems you own or have explicit
permission to test. Keylogging others without consent is a criminal offense
in many jurisdictions.

---

## License

MIT — see `LICENSE` if you add one.
