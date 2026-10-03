"""Hi19 Kernel — консольное ядро, запускающее графическую оболочку HiPE."""

import importlib
import os
import sys
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MESSAGES = {
    'ru': {
        'welcome': "\n=== Hi19 Kernel v1.1 ===",
        'help_intro': "Ядро загружено. Введите 'help' для списка команд.",
        'gui_start': "Инициализация графической оболочки HiPE...",
        'gui_end': "Графическая оболочка закрыта. Возврат в ядро.",
        'exit': "Завершение работы ядра...",
        'help': ("Доступные команды:\n"
                 "  HiPE - запуск графической среды\n"
                 "  ver  - версия ядра\n"
                 "  cls  - очистить экран\n"
                 "  exit - выход в обычный CMD"),
        'ver': "Hi19 Kernel v1.1",
        'unknown': "Ошибка: Команда '{cmd}' не найдена в ядре.",
        'interrupt': "\nПринудительное завершение...",
        'gui_not_found': ("Ошибка: не найдена папка Hi19GRAFICS с файлом gui.py.\n"
                          "Искали рядом с ядром и в C:\\Hi19GRAFICS."),
        'no_pyqt': ("Ошибка: не установлена библиотека PyQt6.\n"
                    "Установите её командой: pip install PyQt6"),
        'gui_error': "Ошибка графической оболочки:",
    },
    'en': {
        'welcome': "\n=== Hi19 Kernel v1.1 ===",
        'help_intro': "Kernel loaded. Type 'help' for a list of commands.",
        'gui_start': "Initializing HiPE graphical environment...",
        'gui_end': "Graphical environment closed. Back to the kernel.",
        'exit': "Shutting down the kernel...",
        'help': ("Available commands:\n"
                 "  HiPE - launch graphical environment\n"
                 "  ver  - kernel version\n"
                 "  cls  - clear the screen\n"
                 "  exit - exit to standard CMD"),
        'ver': "Hi19 Kernel v1.1",
        'unknown': "Error: Command '{cmd}' not found in the kernel.",
        'interrupt': "\nForced shutdown...",
        'gui_not_found': ("Error: the Hi19GRAFICS folder with gui.py was not found.\n"
                          "Looked next to the kernel and in C:\\Hi19GRAFICS."),
        'no_pyqt': ("Error: the PyQt6 library is not installed.\n"
                    "Install it with: pip install PyQt6"),
        'gui_error': "Graphical environment error:",
    },
}


def configure_streams():
    """Не даём консоли падать на символах, которых нет в её кодировке."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors='replace')
        except (AttributeError, ValueError, OSError):
            pass


def find_gui_dir():
    """Ищет папку Hi19GRAFICS: рядом с ядром, внутри него и на диске C:."""
    candidates = [
        os.path.join(os.path.dirname(BASE_DIR), "Hi19GRAFICS"),
        os.path.join(BASE_DIR, "Hi19GRAFICS"),
        r"C:\Hi19GRAFICS",
    ]
    for path in candidates:
        if os.path.isfile(os.path.join(path, "gui.py")):
            return path
    return None


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def start_gui(lang):
    msg = MESSAGES[lang]
    gui_dir = find_gui_dir()
    if gui_dir is None:
        print(msg['gui_not_found'])
        return

    if gui_dir not in sys.path:
        sys.path.insert(0, gui_dir)

    print(msg['gui_start'])
    try:
        gui = importlib.import_module("gui")
    except ImportError as e:
        if 'PyQt6' in str(e) or getattr(e, 'name', '') and 'PyQt6' in e.name:
            print(msg['no_pyqt'])
        else:
            print(msg['gui_error'])
            traceback.print_exc()
        return
    except Exception:
        print(msg['gui_error'])
        traceback.print_exc()
        return

    try:
        # Язык, выбранный в ядре, передаётся в графическую оболочку
        gui.run(lang)
        print(msg['gui_end'])
    except Exception:
        print(msg['gui_error'])
        traceback.print_exc()


def choose_language():
    print("Select Language / Выберите язык:")
    print("1 - Русский")
    print("2 - English")
    choice = input("Choice / Выбор (1/2): ").strip()
    return 'en' if choice == '2' else 'ru'


def main():
    configure_streams()

    try:
        lang = choose_language()
    except (KeyboardInterrupt, EOFError):
        print()
        return

    msg = MESSAGES[lang]
    print(msg['welcome'])
    print(msg['help_intro'])

    while True:
        try:
            cmd = input("Hi19> ").strip()
        except KeyboardInterrupt:
            print(msg['interrupt'])
            break
        except EOFError:
            print()
            print(msg['exit'])
            break

        if not cmd:
            continue

        name = cmd.lower()
        if name == "hipe":
            start_gui(lang)
        elif name == "exit":
            print(msg['exit'])
            break
        elif name == "help":
            print(msg['help'])
        elif name == "ver":
            print(msg['ver'])
        elif name in ("cls", "clear"):
            clear_screen()
        else:
            print(msg['unknown'].format(cmd=cmd))


if __name__ == "__main__":
    main()
