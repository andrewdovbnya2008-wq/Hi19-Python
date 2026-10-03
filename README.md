# Hi19 OS English

A mini Python-based operating environment featuring a console kernel and the HiPE graphical desktop. On startup, the kernel lets you select the interface language (Russian or English), and that language is passed on to the GUI.

## 🛠 Installation

> **Important:** Python 3.9 or newer is required. Contains AI-generated content.

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

# Hi19 OS Russian

Мини-операционная среда на Python с консольным ядром и графической оболочкой HiPE. При запуске ядро предлагает выбрать язык интерфейса (русский или английский), и этот язык передаётся в графическую оболочку.

## 🛠 Установка

> **Важно:** потребуется Python 3.9 или новее. Контент содержит ИИ.

1. Установите библиотеку PyQt6:
   ```bash
   pip install PyQt6
   ```
   (необязательно) для реальной загрузки CPU/RAM в Диспетчере:
   ```bash
   pip install psutil
   ```
2. Положите папки `Hi19CMD` и `Hi19GRAFICS` рядом друг с другом (можно в корень диска `C:\`, можно в любое другое место — ядро найдёт графику само).
3. (необязательно) Чтобы запускать командой `Hi19` из любого места, переместите `Hi19.bat` в `C:\Windows` (нужны права администратора). Если папки лежат в `C:\`, bat-файл найдёт ядро сам.

## 🚀 Использование

Откройте CMD и введите: `Hi19`

Выберите язык:

- `1` — Русский
- `2` — English

Команды ядра: `HiPE` (запуск графики), `help`, `ver`, `cls`, `exit`.

В графической оболочке: Проводник, Блокнот, Калькулятор, Терминал, Диспетчер, Галерея, Змейка и Настройки (фон рабочего стола и цвет акцента).
