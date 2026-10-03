# Hi19 OS

A mini Python-based operating environment featuring a console kernel and the HiPE graphical desktop. On startup, the kernel lets you select the interface language (Russian or English), and that language is passed on to the GUI.

## 🛠 Installation

> **Important:** Python 3.9 or newer is required.

1. Install the PyQt6 library:
   ```bash
   pip install PyQt6
   ```
   (optional) for real CPU/RAM readings in the Task Manager:
   ```bash
   pip install psutil
   ```
2. Put the `Hi19CMD` and `Hi19GRAFICS` folders next to each other (the root of `C:\` works, but any location is fine — the kernel finds the GUI by itself).
3. (optional) To launch it with the `Hi19` command from anywhere, move `Hi19.bat` to `C:\Windows` (requires Administrator privileges). If the folders are in `C:\`, the bat file finds the kernel on its own.

## 🚀 Usage

Open CMD and type: `Hi19`

Select your language:

- `1` — Russian
- `2` — English

Kernel commands: `HiPE` (launch the GUI), `help`, `ver`, `cls`, `exit`.

The desktop includes: Explorer, Notepad, Calculator, Terminal, Task Manager, Gallery, Snake and Settings (desktop background and accent color).
