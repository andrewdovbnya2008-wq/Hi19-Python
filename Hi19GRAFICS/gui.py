# -*- coding: utf-8 -*-
"""HiPE — графическая оболочка Hi19 OS (PyQt6).

Запускается ядром: gui.run(lang), где lang — 'ru' или 'en'.
Можно запускать и напрямую: python gui.py
"""

import datetime
import getpass
import json
import math
import os
import random
import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QFrame,
    QToolButton, QTreeWidget, QTreeWidgetItem, QHeaderView, QMessageBox,
    QGraphicsDropShadowEffect, QMenu, QComboBox, QProgressBar, QFileDialog,
    QInputDialog
)
from PyQt6.QtCore import Qt, QTimer, QTime, QDate, QSize, QEvent, QRect, QByteArray
from PyQt6.QtGui import (
    QIcon, QColor, QPainter, QAction, QPixmap, QFontDatabase, QTextCursor,
    QShortcut, QKeySequence
)

try:
    from PyQt6.QtSvg import QSvgRenderer
except ImportError:  # без QtSvg иконки грузятся напрямую из файла
    QSvgRenderer = None

try:
    import psutil
except ImportError:  # psutil необязателен — тогда показываем симуляцию
    psutil = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")

# ==============================================================================
# 1. ЛОКАЛИЗАЦИЯ
# ==============================================================================

STRINGS = {
    'ru': {
        'lang_code': 'RU', 'lang_name': 'Русский',
        'start': 'Пуск', 'search': 'Поиск...', 'pinned': 'Закрепленные',
        'no_results': 'Ничего не найдено',
        'pc': 'Этот ПК', 'explorer': 'Проводник', 'notepad': 'Блокнот',
        'calculator': 'Калькулятор', 'terminal': 'Терминал', 'settings': 'Настройки',
        'taskmgr': 'Диспетчер', 'viewer': 'Галерея', 'snake': 'Змейка',
        'refresh': 'Обновить', 'new_file': 'Новый файл',
        'bg_color': 'Фон рабочего стола:', 'theme': 'Тема:',
        'bg_blue': 'Синий', 'bg_purple': 'Фиолетовый', 'bg_green': 'Зелёный',
        'bg_dark': 'Тёмный', 'bg_sunset': 'Закат',
        'acc_blue': 'Синяя', 'acc_green': 'Зелёная', 'acc_red': 'Красная',
        'acc_purple': 'Фиолетовая', 'acc_orange': 'Оранжевая',
        'lang_info': 'Язык интерфейса: {lang}',
        'user': 'кот',
        'power_title': 'Выключение', 'power_confirm': 'Завершить работу HiPE?',
        'ctx_refresh': 'Обновить рабочий стол', 'ctx_terminal': 'Открыть в Терминале',
        'ctx_explorer': 'Открыть Проводник', 'ctx_personalize': 'Персонализация',
        'up': 'Вверх', 'name': 'Имя', 'size': 'Размер', 'type': 'Тип',
        'folder': 'Папка', 'file': 'Файл', 'error': 'Ошибка',
        'path_not_found': 'Путь не найден: {path}',
        'access_error': 'Нет доступа: {err}',
        'items_count': 'Элементов: {n}', 'empty_folder': 'Папка пуста',
        'new_file_prompt': 'Имя нового файла:', 'bad_name': 'Недопустимое имя файла',
        'file_exists': 'Файл уже существует',
        'unsupported_type': 'Этот тип файла не поддерживается',
        'open': 'Открыть', 'save': 'Сохранить', 'untitled': 'Без имени',
        'open_file_title': 'Открыть файл', 'save_file_title': 'Сохранить',
        'unsaved_title': 'Несохранённые изменения',
        'unsaved_text': 'Сохранить изменения в «{name}»?',
        'file_too_big': 'Файл слишком большой (больше 5 МБ)',
        'cant_decode': 'Не удалось прочитать файл как текст',
        'viewer_hint': 'Откройте изображение', 'open_image': 'Открыть файл',
        'open_image_title': 'Открыть картинку', 'images_filter': 'Изображения',
        'prev': '◀ Назад', 'next': 'Далее ▶',
        'cant_load_image': 'Не удалось загрузить изображение:\n{path}',
        'cpu': 'Загрузка CPU', 'ram': 'Использование RAM', 'processes': 'Процессы',
        'proc_header': 'PID    Имя           Память',
        'score': 'Счёт: {n}', 'game_over': 'Игра окончена',
        'press_restart': 'Пробел — новая игра', 'paused': 'Пауза',
        'snake_hint': 'Стрелки/WASD — ход, пробел — пауза',
        'term_welcome': 'HiPE Терминал v1.1\nВведите help для списка команд.\n',
        'term_help': ('Команды: help, cls, ver, ping, matrix, echo, dir, cd, pwd,\n'
                      'type, mkdir, date, time, whoami, exit'),
        'term_unknown': "'{cmd}' не является внутренней или внешней командой.",
        'term_dir_of': 'Содержимое папки {path}',
        'term_not_dir': 'Папка не найдена: {path}',
        'term_not_file': 'Файл не найден: {path}',
        'term_file_big': 'Файл слишком большой для просмотра',
        'term_created': 'Папка создана: {path}',
        'term_need_arg': 'Не хватает аргумента',
        'term_exists': 'Уже существует: {path}',
        'term_denied': 'Ошибка: {err}',
        'ver': 'HiPE OS 11 (сборка 2026)',
        'calc_div_zero': 'Деление на ноль', 'calc_error': 'Ошибка',
        'calc_too_long': 'Слишком длинное выражение',
    },
    'en': {
        'lang_code': 'EN', 'lang_name': 'English',
        'start': 'Start', 'search': 'Search...', 'pinned': 'Pinned',
        'no_results': 'Nothing found',
        'pc': 'This PC', 'explorer': 'Explorer', 'notepad': 'Notepad',
        'calculator': 'Calculator', 'terminal': 'Terminal', 'settings': 'Settings',
        'taskmgr': 'Task Manager', 'viewer': 'Gallery', 'snake': 'Snake',
        'refresh': 'Refresh', 'new_file': 'New file',
        'bg_color': 'Desktop background:', 'theme': 'Theme:',
        'bg_blue': 'Blue', 'bg_purple': 'Purple', 'bg_green': 'Green',
        'bg_dark': 'Dark', 'bg_sunset': 'Sunset',
        'acc_blue': 'Blue', 'acc_green': 'Green', 'acc_red': 'Red',
        'acc_purple': 'Purple', 'acc_orange': 'Orange',
        'lang_info': 'Interface language: {lang}',
        'user': 'cat',
        'power_title': 'Shut down', 'power_confirm': 'Close HiPE?',
        'ctx_refresh': 'Refresh desktop', 'ctx_terminal': 'Open in Terminal',
        'ctx_explorer': 'Open Explorer', 'ctx_personalize': 'Personalize',
        'up': 'Up', 'name': 'Name', 'size': 'Size', 'type': 'Type',
        'folder': 'Folder', 'file': 'File', 'error': 'Error',
        'path_not_found': 'Path not found: {path}',
        'access_error': 'Access denied: {err}',
        'items_count': 'Items: {n}', 'empty_folder': 'Folder is empty',
        'new_file_prompt': 'New file name:', 'bad_name': 'Invalid file name',
        'file_exists': 'File already exists',
        'unsupported_type': 'This file type is not supported',
        'open': 'Open', 'save': 'Save', 'untitled': 'Untitled',
        'open_file_title': 'Open file', 'save_file_title': 'Save',
        'unsaved_title': 'Unsaved changes',
        'unsaved_text': 'Save changes to "{name}"?',
        'file_too_big': 'File is too large (over 5 MB)',
        'cant_decode': 'Could not read the file as text',
        'viewer_hint': 'Open an image', 'open_image': 'Open file',
        'open_image_title': 'Open image', 'images_filter': 'Images',
        'prev': '◀ Prev', 'next': 'Next ▶',
        'cant_load_image': 'Could not load the image:\n{path}',
        'cpu': 'CPU Usage', 'ram': 'RAM Usage', 'processes': 'Processes',
        'proc_header': 'PID    Name          Memory',
        'score': 'Score: {n}', 'game_over': 'Game over',
        'press_restart': 'Space — new game', 'paused': 'Paused',
        'snake_hint': 'Arrows/WASD — move, space — pause',
        'term_welcome': 'HiPE Terminal v1.1\nType help for a list of commands.\n',
        'term_help': ('Commands: help, cls, ver, ping, matrix, echo, dir, cd, pwd,\n'
                      'type, mkdir, date, time, whoami, exit'),
        'term_unknown': "'{cmd}' is not recognized as an internal or external command.",
        'term_dir_of': 'Directory of {path}',
        'term_not_dir': 'Directory not found: {path}',
        'term_not_file': 'File not found: {path}',
        'term_file_big': 'File is too large to display',
        'term_created': 'Directory created: {path}',
        'term_need_arg': 'Missing argument',
        'term_exists': 'Already exists: {path}',
        'term_denied': 'Error: {err}',
        'ver': 'HiPE OS 11 (Build 2026)',
        'calc_div_zero': 'Division by zero', 'calc_error': 'Error',
        'calc_too_long': 'Expression is too long',
    },
}

CURRENT_LANG = 'ru'


def set_language(lang):
    global CURRENT_LANG
    CURRENT_LANG = lang if lang in STRINGS else 'ru'


def tr(key, **kwargs):
    """Возвращает строку на текущем языке (с запасным вариантом на русском)."""
    text = STRINGS.get(CURRENT_LANG, {}).get(key)
    if text is None:
        text = STRINGS['ru'].get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            return text
    return text


# ==============================================================================
# 2. ИКОНКИ И НАСТРОЙКИ
# ==============================================================================

EMOJI_FALLBACKS = {
    'win': '🪟', 'pc': '💻', 'explorer': '📁', 'notepad': '📝', 'calculator': '🧮',
    'terminal': '🖥️', 'settings': '⚙️', 'taskmgr': '📊', 'viewer': '🖼️',
    'player': '🎵', 'snake': '🐍'
}

_SVG_HEAD = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">'

# Встроенные иконки: если файла нет в cache/, он создаётся автоматически.
# Интернет больше не нужен (раньше недостающие иконки качались с GitHub).
BUILTIN_SVGS = {
    'win': (_SVG_HEAD +
            '<rect x="3" y="3" width="8" height="8" rx="1" fill="#FFFFFF"/>'
            '<rect x="13" y="3" width="8" height="8" rx="1" fill="#FFFFFF"/>'
            '<rect x="3" y="13" width="8" height="8" rx="1" fill="#FFFFFF"/>'
            '<rect x="13" y="13" width="8" height="8" rx="1" fill="#FFFFFF"/></svg>'),
    'taskmgr': (_SVG_HEAD +
                '<rect x="3" y="12" width="4" height="9" rx="1" fill="#FFFFFF"/>'
                '<rect x="10" y="6" width="4" height="15" rx="1" fill="#FFFFFF"/>'
                '<rect x="17" y="3" width="4" height="18" rx="1" fill="#FFFFFF"/></svg>'),
    'viewer': (_SVG_HEAD +
               '<rect x="3" y="4" width="18" height="16" rx="2" stroke="#FFFFFF" stroke-width="1.8"/>'
               '<circle cx="9" cy="10" r="1.8" fill="#FFFFFF"/>'
               '<path d="M4 18L9.5 13L13 16L16 13L20 17" stroke="#FFFFFF" stroke-width="1.8" '
               'stroke-linecap="round" stroke-linejoin="round"/></svg>'),
    'player': (_SVG_HEAD +
               '<path d="M9 18V6L19 4V16" stroke="#FFFFFF" stroke-width="1.8" '
               'stroke-linecap="round" stroke-linejoin="round"/>'
               '<circle cx="6.5" cy="18" r="2.5" fill="#FFFFFF"/>'
               '<circle cx="16.5" cy="16" r="2.5" fill="#FFFFFF"/></svg>'),
    'snake': (_SVG_HEAD +
              '<path d="M18 5H8a3 3 0 0 0 0 6H16a3 3 0 0 1 0 6H6" stroke="#FFFFFF" '
              'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
              '<circle cx="18.5" cy="5" r="1.3" fill="#FFFFFF"/></svg>'),
}

# Старые иконки из кэша были закрашены в #212121 и на тёмном интерфейсе
# были практически невидимы — перекрашиваем в белый при загрузке.
DARK_FILL = '#212121'
LIGHT_FILL = '#FFFFFF'


class IconManager:
    _cache = {}

    @classmethod
    def get_icon(cls, name):
        """Возвращает (QIcon, None) или (None, emoji), если иконку не удалось загрузить."""
        if name not in cls._cache:
            cls._cache[name] = cls._load(name)
        return cls._cache[name]

    @classmethod
    def clear(cls):
        cls._cache.clear()

    @classmethod
    def _load(cls, name):
        path = os.path.join(CACHE_DIR, f"{name}.svg")
        try:
            os.makedirs(CACHE_DIR, exist_ok=True)
        except OSError:
            pass

        data = None
        if os.path.isfile(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = f.read()
            except (OSError, UnicodeDecodeError):
                data = None
        if data is None and name in BUILTIN_SVGS:
            data = BUILTIN_SVGS[name]
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(data)
            except OSError:
                pass

        if data:
            data = data.replace(DARK_FILL, LIGHT_FILL)
            icon = cls._icon_from_svg(data, path)
            if icon is not None and not icon.isNull():
                return icon, None
        return None, EMOJI_FALLBACKS.get(name, '📄')

    @staticmethod
    def _icon_from_svg(data, path):
        if QSvgRenderer is not None:
            renderer = QSvgRenderer(QByteArray(data.encode('utf-8')))
            if renderer.isValid():
                pixmap = QPixmap(96, 96)
                pixmap.fill(Qt.GlobalColor.transparent)
                painter = QPainter(pixmap)
                renderer.render(painter)
                painter.end()
                return QIcon(pixmap)
        return QIcon(path) if os.path.isfile(path) else None


BACKGROUNDS = {
    'blue': ('#141E30', '#243B55'),
    'purple': ('#2B1055', '#5B6FB5'),
    'green': ('#0F2027', '#2C5364'),
    'dark': ('#0F0F0F', '#2B2B2B'),
    'sunset': ('#4B134F', '#C94B4B'),
}
ACCENTS = {
    'blue': '#0078D7', 'green': '#107C10', 'red': '#E81123',
    'purple': '#8E44AD', 'orange': '#D83B01',
}
DEFAULT_SETTINGS = {'background': 'blue', 'accent': 'blue'}


def load_settings():
    settings = dict(DEFAULT_SETTINGS)
    try:
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            if data.get('background') in BACKGROUNDS:
                settings['background'] = data['background']
            if data.get('accent') in ACCENTS:
                settings['accent'] = data['accent']
    except (OSError, ValueError):
        pass
    return settings


def save_settings(settings):
    try:
        with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def mono_font(point_size=10):
    font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
    font.setPointSize(point_size)
    return font


def default_root():
    """Корень файловой системы для Проводника: C:\\ в Windows, иначе домашняя папка."""
    if sys.platform == "win32" and os.path.isdir("C:\\"):
        return "C:\\"
    return os.path.expanduser("~")


def human_size(num):
    size = float(num)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{int(size)} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{num} B"


# ==============================================================================
# 3. КАЛЬКУЛЯТОР: безопасный разбор выражений (без eval)
# ==============================================================================

_OPERATORS = {'+': '+', '-': '-', '−': '-', '*': '*', '×': '*', '/': '/',
              '÷': '/', '%': '%', '(': '(', ')': ')'}


def _tokenize(text):
    tokens = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit() or ch == '.':
            j, dots = i, 0
            while j < n and (text[j].isdigit() or text[j] == '.'):
                if text[j] == '.':
                    dots += 1
                j += 1
            chunk = text[i:j]
            if dots > 1 or chunk == '.':
                raise ValueError("bad number")
            # экспоненциальная запись (результат вида 1e-07)
            if j < n and text[j] in 'eE':
                k = j + 1
                if k < n and text[k] in '+-':
                    k += 1
                if k < n and text[k].isdigit():
                    while k < n and text[k].isdigit():
                        k += 1
                    chunk = text[i:k]
                    j = k
            tokens.append(('num', float(chunk)))
            i = j
        elif ch in _OPERATORS:
            tokens.append(('op', _OPERATORS[ch]))
            i += 1
        else:
            raise ValueError("bad character")
    return tokens


class _Parser:
    """expr := term (('+'|'-') term)*;  term := unary (('*'|'/') unary)*"""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def take(self):
        token = self.peek()
        self.pos += 1
        return token

    def parse(self):
        if not self.tokens:
            raise ValueError("empty")
        value = self.expr()
        if self.peek() is not None:
            raise ValueError("unexpected token")
        return value

    def expr(self):
        value = self.term()
        while self.peek() in (('op', '+'), ('op', '-')):
            op = self.take()[1]
            right = self.term()
            value = value + right if op == '+' else value - right
        return value

    def term(self):
        value = self.unary()
        while self.peek() in (('op', '*'), ('op', '/')):
            op = self.take()[1]
            right = self.unary()
            if op == '*':
                value *= right
            else:
                if right == 0:
                    raise ZeroDivisionError
                value /= right
        return value

    def unary(self):
        if self.peek() == ('op', '-'):
            self.take()
            return -self.unary()
        if self.peek() == ('op', '+'):
            self.take()
            return self.unary()
        return self.postfix()

    def postfix(self):
        value = self.primary()
        while self.peek() == ('op', '%'):
            self.take()
            value /= 100.0
        return value

    def primary(self):
        token = self.take()
        if token is None:
            raise ValueError("unexpected end")
        if token[0] == 'num':
            return token[1]
        if token == ('op', '('):
            value = self.expr()
            if self.take() != ('op', ')'):
                raise ValueError("missing )")
            return value
        raise ValueError("unexpected token")


def evaluate_expression(text):
    """Считает выражение. Бросает ValueError / ZeroDivisionError / OverflowError."""
    result = _Parser(_tokenize(text)).parse()
    if not math.isfinite(result):
        raise OverflowError
    return result


def format_number(value):
    if value == int(value) and abs(value) < 1e15:
        return str(int(value))
    return f"{value:.12g}"


# ==============================================================================
# 4. ДВИЖОК ОКОН
# ==============================================================================

class TitleBar(QFrame):
    """Заголовок окна: перетаскивание и двойной клик для разворота."""

    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.setObjectName("HiPETitleBar")
        self.setFixedHeight(35)
        # Селектор по имени — иначе рамка каскадом попадёт на все дочерние QLabel
        self.setStyleSheet(
            "#HiPETitleBar { background: transparent; "
            "border-bottom: 1px solid rgba(255, 255, 255, 15); }")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.owner.begin_drag(event.globalPosition().toPoint())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if bool(event.buttons() & Qt.MouseButton.LeftButton):
            self.owner.drag_to(event.globalPosition().toPoint())

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.owner.toggle_maximize()


class HiPEWindow(QFrame):
    _next_pid = 1000

    def __init__(self, title, icon_name, parent_os, width=650, height=450):
        super().__init__(parent_os.desktop)
        self.parent_os = parent_os
        self.title_text = title
        self.icon_name = icon_name
        self.is_maximized = False
        self.old_geometry = None
        self._drag_start_global = None
        self._drag_start_pos = None

        HiPEWindow._next_pid += random.randint(1, 37)
        self.pid = HiPEWindow._next_pid
        self.mem_mb = random.randint(18, 90)

        self.setObjectName("HiPEWindow")
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.resize(width, height)

        offset = (len(parent_os.windows) % 8) * 30
        self.move(100 + offset, 60 + offset)
        parent_os.windows.append(self)

        # Селектор по имени + явный цвет для QLabel: без этого подписи на тёмном
        # фоне окна рисовались чёрным по тёмному
        self.setStyleSheet("""
            #HiPEWindow {
                background-color: rgba(25, 25, 25, 245);
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 8px;
            }
            #HiPEWindow QLabel { color: white; background: transparent; border: none; }
        """)
        self._apply_shadow()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Title Bar
        self.title_bar = TitleBar(self)
        tb_layout = QHBoxLayout(self.title_bar)
        tb_layout.setContentsMargins(10, 0, 5, 0)

        icon_obj, emoji = IconManager.get_icon(icon_name)
        icon_lbl = QLabel()
        if icon_obj:
            icon_lbl.setPixmap(icon_obj.pixmap(18, 18))
        else:
            icon_lbl.setText(emoji)
        tb_layout.addWidget(icon_lbl)

        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet("color: white; font-weight: bold; font-size: 13px;")
        tb_layout.addWidget(self.title_lbl)
        tb_layout.addStretch(1)

        btn_style = ("QPushButton { background: transparent; color: white; border: none; "
                     "font-size: 14px; border-radius: 4px; } "
                     "QPushButton:hover { background: rgba(255, 255, 255, 30); }")
        btn_close_style = ("QPushButton { background: transparent; color: white; border: none; "
                           "font-size: 14px; border-radius: 4px; } "
                           "QPushButton:hover { background: #E81123; }")

        self.btn_min = QPushButton("–")
        self.btn_min.setFixedSize(30, 25)
        self.btn_min.setStyleSheet(btn_style)
        self.btn_min.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_min.clicked.connect(self.minimize)

        self.btn_max = QPushButton("□")
        self.btn_max.setFixedSize(30, 25)
        self.btn_max.setStyleSheet(btn_style)
        self.btn_max.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_max.clicked.connect(self.toggle_maximize)

        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(30, 25)
        self.btn_close.setStyleSheet(btn_close_style)
        self.btn_close.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_close.clicked.connect(self.close_window)

        tb_layout.addWidget(self.btn_min)
        tb_layout.addWidget(self.btn_max)
        tb_layout.addWidget(self.btn_close)
        self.main_layout.addWidget(self.title_bar)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.addWidget(self.content_area, stretch=1)

    # --- оформление -----------------------------------------------------------

    def _apply_shadow(self):
        # setOffset(x, y) — единственный верный вариант (setOffsetY не существует)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

    def set_title(self, text):
        self.title_text = text
        self.title_lbl.setText(text)
        self.parent_os.refresh_taskbar()

    # --- жизненный цикл -------------------------------------------------------

    def on_activated(self):
        """Хук для приложений: куда ставить фокус при активации окна."""

    def activate(self):
        self.show()
        self.raise_()
        self.parent_os.set_active(self)
        self.on_activated()

    def minimize(self):
        self.hide()
        self.parent_os.window_hidden(self)

    def close_window(self):
        if self in self.parent_os.windows:
            self.parent_os.windows.remove(self)
        self.hide()
        self.parent_os.window_hidden(self)
        self.deleteLater()

    # --- перетаскивание и разворот -------------------------------------------

    def begin_drag(self, global_pos):
        self._drag_start_global = global_pos
        self._drag_start_pos = self.pos()
        self.parent_os.set_active(self)
        self.raise_()
        self.parent_os.restack()

    def drag_to(self, global_pos):
        if self.is_maximized or self._drag_start_global is None:
            return
        target = self._drag_start_pos + (global_pos - self._drag_start_global)
        work_w, work_h = self.parent_os.work_area_size()
        x = max(-self.width() + 80, min(target.x(), work_w - 80))
        y = max(0, min(target.y(), work_h - 35))
        self.move(x, y)

    def toggle_maximize(self):
        if not self.is_maximized:
            self.old_geometry = self.geometry()
            work_w, work_h = self.parent_os.work_area_size()
            self.setGeometry(0, 0, work_w, work_h)
            self.setGraphicsEffect(None)  # тень на весь экран только тормозит
            self.btn_max.setText("❐")
            self.is_maximized = True
        else:
            if self.old_geometry:
                self.setGeometry(self.old_geometry)
            self._apply_shadow()
            self.btn_max.setText("□")
            self.is_maximized = False

    def mousePressEvent(self, event):
        self.parent_os.set_active(self)
        self.raise_()
        self.parent_os.restack()
        super().mousePressEvent(event)


# ==============================================================================
# 5. ПРИЛОЖЕНИЯ
# ==============================================================================

class ExplorerApp(HiPEWindow):
    TEXT_EXT = ('.txt', '.py', '.md', '.json', '.xml', '.log', '.ini', '.cfg',
                '.csv', '.bat', '.html', '.css', '.js')
    IMAGE_EXT = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')

    def __init__(self, parent_os, initial_path=None):
        super().__init__(tr('explorer'), 'explorer', parent_os, 720, 500)
        start = initial_path if initial_path and os.path.isdir(initial_path) else default_root()
        self.current_path = start

        nav_layout = QHBoxLayout()
        btn_style = ("QPushButton { background: rgba(255,255,255,20); color: white; "
                     "border-radius: 5px; padding: 5px 10px; } "
                     "QPushButton:hover { background: rgba(255,255,255,40); }")
        btn_up = QPushButton(tr('up'))
        btn_up.setStyleSheet(btn_style)
        btn_up.clicked.connect(self.go_up)

        btn_refresh = QPushButton(tr('refresh'))
        btn_refresh.setStyleSheet(btn_style)
        btn_refresh.clicked.connect(lambda: self.load_directory(self.current_path))

        btn_new = QPushButton(tr('new_file'))
        btn_new.setStyleSheet(btn_style)
        btn_new.clicked.connect(self.create_file)

        self.path_edit = QLineEdit(self.current_path)
        self.path_edit.setStyleSheet(
            "background: rgba(0,0,0,150); color: white; border-radius: 5px; "
            "padding: 5px; font-size: 13px;")
        self.path_edit.returnPressed.connect(self.navigate)

        nav_layout.addWidget(btn_up)
        nav_layout.addWidget(self.path_edit, stretch=1)
        nav_layout.addWidget(btn_refresh)
        nav_layout.addWidget(btn_new)
        self.content_layout.addLayout(nav_layout)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels([tr('name'), tr('size'), tr('type')])
        self.tree.setRootIsDecorated(False)
        self.tree.setStyleSheet(
            "QTreeWidget { background: rgba(15, 15, 15, 200); color: white; "
            "border-radius: 6px; font-size: 13px; } "
            "QTreeWidget::item:selected { background: rgba(255,255,255,40); } "
            "QHeaderView::section { background-color: rgba(40,40,40,230); color: white; "
            "border: none; padding: 4px; }")
        header = self.tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tree.itemDoubleClicked.connect(self.on_item_double_click)
        self.content_layout.addWidget(self.tree, stretch=1)

        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet("color: rgba(255,255,255,160); font-size: 12px;")
        self.content_layout.addWidget(self.status_lbl)

        self.load_directory(self.current_path)

    def on_activated(self):
        self.tree.setFocus()

    def load_directory(self, path):
        # "C:" без слэша означает «текущая папка диска C» — приводим к корню
        if len(path) == 2 and path[1] == ':':
            path += os.sep
        try:
            names = os.listdir(path)
        except OSError as e:
            self.status_lbl.setText(tr('access_error', err=e.strerror or e))
            self.path_edit.setText(self.current_path)
            return

        entries = []
        for name in names:
            full_p = os.path.join(path, name)
            is_dir = os.path.isdir(full_p)
            if is_dir:
                size = "<DIR>"
            else:
                try:
                    size = human_size(os.path.getsize(full_p))
                except OSError:
                    size = "?"
            entries.append((not is_dir, name.casefold(), name, full_p, is_dir, size))
        entries.sort()

        self.tree.clear()
        self.current_path = path
        self.path_edit.setText(path)
        for _, _, name, full_p, is_dir, size in entries:
            icon = "📁" if is_dir else "📄"
            item = QTreeWidgetItem([f"{icon} {name}", size, tr('folder') if is_dir else tr('file')])
            item.setData(0, Qt.ItemDataRole.UserRole, full_p)
            self.tree.addTopLevelItem(item)

        if entries:
            self.status_lbl.setText(tr('items_count', n=len(entries)))
        else:
            self.status_lbl.setText(tr('empty_folder'))

    def go_up(self):
        current = os.path.normpath(self.current_path)
        parent = os.path.dirname(current)
        if parent and parent != current and os.path.isdir(parent):
            self.load_directory(parent)

    def navigate(self):
        p = os.path.expanduser(self.path_edit.text().strip().strip('"'))
        if os.path.isdir(p):
            self.load_directory(p)
        elif os.path.isfile(p):
            self.open_path(p)
            self.path_edit.setText(self.current_path)
        else:
            self.status_lbl.setText(tr('path_not_found', path=p))
            self.path_edit.setText(self.current_path)

    def create_file(self):
        name, ok = QInputDialog.getText(self.parent_os, tr('new_file'), tr('new_file_prompt'))
        name = name.strip()
        if not ok or not name:
            return
        if any(ch in name for ch in '/\\:*?"<>|') or name in ('.', '..'):
            QMessageBox.warning(self.parent_os, tr('error'), tr('bad_name'))
            return
        full_p = os.path.join(self.current_path, name)
        try:
            with open(full_p, 'x', encoding='utf-8'):
                pass
        except FileExistsError:
            QMessageBox.warning(self.parent_os, tr('error'), tr('file_exists'))
            return
        except OSError as e:
            QMessageBox.critical(self.parent_os, tr('error'), str(e))
            return
        self.load_directory(self.current_path)

    def open_path(self, full_p):
        lower = full_p.lower()
        if os.path.isdir(full_p):
            self.load_directory(full_p)
        elif lower.endswith(self.TEXT_EXT):
            self.parent_os.open_app('notepad', full_p)
        elif lower.endswith(self.IMAGE_EXT):
            self.parent_os.open_app('viewer', full_p)
        else:
            self.status_lbl.setText(tr('unsupported_type'))

    def on_item_double_click(self, item, col):
        full_p = item.data(0, Qt.ItemDataRole.UserRole)
        if full_p:
            self.open_path(full_p)


class NotepadApp(HiPEWindow):
    MAX_SIZE = 5 * 1024 * 1024

    def __init__(self, parent_os, file_path=None):
        super().__init__(tr('notepad'), 'notepad', parent_os, 620, 460)
        self.current_file = None

        top_bar = QHBoxLayout()
        btn_open = QPushButton(tr('open'))
        btn_save = QPushButton(tr('save'))
        btn_style = ("QPushButton { background: rgba(255,255,255,20); color: white; "
                     "border-radius: 5px; padding: 5px 15px; } "
                     "QPushButton:hover { background: rgba(255,255,255,40); }")
        btn_open.setStyleSheet(btn_style)
        btn_save.setStyleSheet(btn_style)
        btn_open.clicked.connect(self.open_file)
        btn_save.clicked.connect(self.save_file)
        top_bar.addWidget(btn_open)
        top_bar.addWidget(btn_save)
        top_bar.addStretch()
        self.content_layout.addLayout(top_bar)

        self.editor = QTextEdit()
        self.editor.setAcceptRichText(False)
        self.editor.setFont(mono_font(11))
        self.editor.setStyleSheet(
            "QTextEdit { background-color: #1E1E1E; color: #D4D4D4; "
            "border: 1px solid #333; border-radius: 5px; }")
        self.content_layout.addWidget(self.editor, stretch=1)

        # Ctrl+S / Ctrl+O — только внутри этого блокнота, чтобы окна не конфликтовали
        sc_save = QShortcut(QKeySequence("Ctrl+S"), self.editor)
        sc_save.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        sc_save.activated.connect(self.save_file)
        sc_open = QShortcut(QKeySequence("Ctrl+O"), self.editor)
        sc_open.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        sc_open.activated.connect(self.open_file)

        self.editor.document().modificationChanged.connect(self.update_title)
        self.update_title()

        if file_path:
            self.load_path(file_path)

    def on_activated(self):
        self.editor.setFocus()

    def update_title(self, *args):
        name = os.path.basename(self.current_file) if self.current_file else tr('untitled')
        mark = "*" if self.editor.document().isModified() else ""
        self.set_title(f"{tr('notepad')} — {name}{mark}")

    def load_path(self, path):
        try:
            if os.path.getsize(path) > self.MAX_SIZE:
                QMessageBox.warning(self.parent_os, tr('error'), tr('file_too_big'))
                return False
            with open(path, 'rb') as f:
                raw = f.read()
        except OSError as e:
            QMessageBox.critical(self.parent_os, tr('error'), str(e))
            return False

        text = None
        for encoding in ('utf-8-sig', 'cp1251'):
            try:
                text = raw.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        if text is None:
            QMessageBox.warning(self.parent_os, tr('error'), tr('cant_decode'))
            return False

        self.editor.setPlainText(text)
        self.editor.document().setModified(False)
        self.current_file = path
        self.update_title()
        return True

    def open_file(self):
        start = os.path.dirname(self.current_file) if self.current_file else default_root()
        fn, _ = QFileDialog.getOpenFileName(self.parent_os, tr('open_file_title'), start, "All Files (*)")
        if fn:
            self.load_path(fn)

    def save_file(self):
        """Сохраняет файл. Возвращает True, если запись удалась."""
        if not self.current_file:
            fn, _ = QFileDialog.getSaveFileName(
                self.parent_os, tr('save_file_title'), default_root(),
                "Text Files (*.txt);;All Files (*)")
            if not fn:
                return False
            self.current_file = fn
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
        except OSError as e:
            QMessageBox.critical(self.parent_os, tr('error'), str(e))
            return False
        self.editor.document().setModified(False)
        self.update_title()
        return True

    def close_window(self):
        if self.editor.document().isModified():
            name = os.path.basename(self.current_file) if self.current_file else tr('untitled')
            buttons = (QMessageBox.StandardButton.Save |
                       QMessageBox.StandardButton.Discard |
                       QMessageBox.StandardButton.Cancel)
            answer = QMessageBox.question(
                self.parent_os, tr('unsaved_title'), tr('unsaved_text', name=name), buttons)
            if answer == QMessageBox.StandardButton.Cancel:
                return
            if answer == QMessageBox.StandardButton.Save and not self.save_file():
                return
        super().close_window()


class HistoryLineEdit(QLineEdit):
    """Строка ввода терминала с историей команд (стрелки вверх/вниз)."""

    def __init__(self):
        super().__init__()
        self.history = []
        self.index = 0

    def push(self, text):
        if text and (not self.history or self.history[-1] != text):
            self.history.append(text)
        self.index = len(self.history)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            if self.history and self.index > 0:
                self.index -= 1
                self.setText(self.history[self.index])
        elif event.key() == Qt.Key.Key_Down:
            if self.index < len(self.history) - 1:
                self.index += 1
                self.setText(self.history[self.index])
            else:
                self.index = len(self.history)
                self.clear()
        else:
            super().keyPressEvent(event)


class TerminalApp(HiPEWindow):
    def __init__(self, parent_os, start_dir=None):
        super().__init__(tr('terminal'), 'terminal', parent_os, 680, 420)
        self.cwd = start_dir if start_dir and os.path.isdir(start_dir) else default_root()

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(mono_font(10))
        self.console.setStyleSheet(
            "QTextEdit { background-color: #0C0C0C; color: #00FF00; border-radius: 5px; }")

        self.input_line = HistoryLineEdit()
        self.input_line.setFont(mono_font(10))
        self.input_line.setStyleSheet(
            "background-color: #1F1F1F; color: #00FF00; padding: 5px; border-radius: 3px;")
        self.input_line.returnPressed.connect(self.exec_cmd)

        self.content_layout.addWidget(self.console, stretch=1)
        self.content_layout.addWidget(self.input_line)
        self.write(tr('term_welcome'))

    def on_activated(self):
        self.input_line.setFocus()

    def write(self, text=""):
        # insertPlainText, а не append(): append() воспринимает "<DIR>" как HTML-тег
        self.console.moveCursor(QTextCursor.MoveOperation.End)
        self.console.insertPlainText(text + "\n")
        self.console.ensureCursorVisible()

    def exec_cmd(self):
        line = self.input_line.text().strip()
        self.input_line.clear()
        if not line:
            return
        self.input_line.push(line)
        self.write(f"{self.cwd}> {line}")
        try:
            self.run_command(line)
        except OSError as e:
            self.write(tr('term_denied', err=e.strerror or e))

    def resolve(self, arg):
        arg = arg.strip().strip('"')
        return os.path.normpath(os.path.join(self.cwd, os.path.expanduser(arg)))

    def run_command(self, line):
        parts = line.split(None, 1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd in ("clear", "cls"):
            self.console.clear()
        elif cmd == "help":
            self.write(tr('term_help'))
        elif cmd == "ver":
            self.write(tr('ver'))
        elif cmd == "echo":
            self.write(arg)
        elif cmd == "pwd":
            self.write(self.cwd)
        elif cmd in ("dir", "ls"):
            self.cmd_dir(arg)
        elif cmd == "cd":
            self.cmd_cd(arg)
        elif cmd in ("type", "cat"):
            self.cmd_type(arg)
        elif cmd == "mkdir":
            self.cmd_mkdir(arg)
        elif cmd == "date":
            self.write(datetime.date.today().strftime("%d.%m.%Y"))
        elif cmd == "time":
            self.write(datetime.datetime.now().strftime("%H:%M:%S"))
        elif cmd == "whoami":
            try:
                self.write(getpass.getuser())
            except Exception:
                self.write("hipe")
        elif cmd == "ping":
            self.cmd_ping(arg)
        elif cmd == "matrix":
            for _ in range(8):
                self.write(" ".join("".join(random.choice("01") for _ in range(8)) for _ in range(6)))
        elif cmd == "exit":
            self.close_window()
        else:
            self.write(tr('term_unknown', cmd=parts[0]))

    def cmd_dir(self, arg):
        target = self.resolve(arg) if arg else self.cwd
        if not os.path.isdir(target):
            self.write(tr('term_not_dir', path=target))
            return
        self.write(tr('term_dir_of', path=target))
        names = sorted(os.listdir(target), key=str.casefold)
        for name in names[:500]:
            full_p = os.path.join(target, name)
            if os.path.isdir(full_p):
                self.write(f"{'<DIR>':>12}  {name}")
            else:
                try:
                    size = os.path.getsize(full_p)
                except OSError:
                    size = 0
                self.write(f"{size:>12}  {name}")
        if len(names) > 500:
            self.write(f"... (+{len(names) - 500})")

    def cmd_cd(self, arg):
        if not arg:
            self.write(self.cwd)
            return
        # "D:" без слэша — переход на корень диска
        if len(arg) == 2 and arg[1] == ':':
            arg += os.sep
        target = self.resolve(arg) if not os.path.isabs(arg) else os.path.normpath(arg)
        if os.path.isdir(target):
            self.cwd = target
        else:
            self.write(tr('term_not_dir', path=target))

    def cmd_type(self, arg):
        if not arg:
            self.write(tr('term_need_arg'))
            return
        target = self.resolve(arg)
        if not os.path.isfile(target):
            self.write(tr('term_not_file', path=target))
            return
        if os.path.getsize(target) > 1024 * 1024:
            self.write(tr('term_file_big'))
            return
        with open(target, 'r', encoding='utf-8', errors='replace') as f:
            self.write(f.read())

    def cmd_mkdir(self, arg):
        if not arg:
            self.write(tr('term_need_arg'))
            return
        target = self.resolve(arg)
        if os.path.exists(target):
            self.write(tr('term_exists', path=target))
            return
        os.makedirs(target)
        self.write(tr('term_created', path=target))

    def cmd_ping(self, arg):
        host = arg or "8.8.8.8"
        self.write(f"Pinging {host} with 32 bytes of data:")
        for _ in range(4):
            self.write(f"Reply from {host}: bytes=32 time={random.randint(9, 24)}ms TTL=117")


class TaskManagerApp(HiPEWindow):
    def __init__(self, parent_os):
        super().__init__(tr('taskmgr'), 'taskmgr', parent_os, 420, 520)
        bar_style = ("QProgressBar { color: white; border: 1px solid #555; "
                     "border-radius: 5px; text-align: center; } "
                     "QProgressBar::chunk { background-color: %s; }")
        self.cpu_bar = QProgressBar()
        self.ram_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.ram_bar.setRange(0, 100)
        self.cpu_bar.setStyleSheet(bar_style % "#0078D7")
        self.ram_bar.setStyleSheet(bar_style % "#107C10")

        head_style = "font-weight: bold; font-size: 14px;"
        cpu_lbl = QLabel(tr('cpu'))
        cpu_lbl.setStyleSheet(head_style)
        ram_lbl = QLabel(tr('ram'))
        ram_lbl.setStyleSheet(head_style)
        proc_lbl = QLabel(tr('processes'))
        proc_lbl.setStyleSheet(head_style)

        self.process_list = QTextEdit()
        self.process_list.setReadOnly(True)
        self.process_list.setFont(mono_font(10))
        self.process_list.setStyleSheet(
            "QTextEdit { background: rgba(0,0,0,100); color: white; border-radius: 5px; }")

        self.content_layout.addWidget(cpu_lbl)
        self.content_layout.addWidget(self.cpu_bar)
        self.content_layout.addWidget(ram_lbl)
        self.content_layout.addWidget(self.ram_bar)
        self.content_layout.addWidget(proc_lbl)
        self.content_layout.addWidget(self.process_list, stretch=1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)
        self.update_stats()

    def update_stats(self):
        if psutil is not None:
            try:
                cpu = int(psutil.cpu_percent(interval=None))
                ram = int(psutil.virtual_memory().percent)
            except Exception:
                cpu, ram = random.randint(5, 35), random.randint(40, 60)
        else:
            cpu, ram = random.randint(5, 35), random.randint(40, 60)
        self.cpu_bar.setValue(max(0, min(100, cpu)))
        self.ram_bar.setValue(max(0, min(100, ram)))

        lines = [tr('proc_header'), "-" * 32,
                 f"{1:<6} {'System':<13} 12 MB",
                 f"{42:<6} {'HiPE_Core':<13} 145 MB",
                 f"{105:<6} {'dwm.exe':<13} 45 MB"]
        for w in self.parent_os.windows:
            name = w.title_text[:13]
            lines.append(f"{w.pid:<6} {name:<13} {w.mem_mb} MB")

        scroll = self.process_list.verticalScrollBar()
        position = scroll.value()
        self.process_list.setPlainText("\n".join(lines))
        scroll.setValue(position)


class SnakeWidget(QWidget):
    GRID = 20
    OPPOSITE = {(0, -1): (0, 1), (0, 1): (0, -1), (-1, 0): (1, 0), (1, 0): (-1, 0)}
    KEYS = {
        Qt.Key.Key_Up: (0, -1), Qt.Key.Key_W: (0, -1),
        Qt.Key.Key_Down: (0, 1), Qt.Key.Key_S: (0, 1),
        Qt.Key.Key_Left: (-1, 0), Qt.Key.Key_A: (-1, 0),
        Qt.Key.Key_Right: (1, 0), Qt.Key.Key_D: (1, 0),
    }

    def __init__(self):
        super().__init__()
        self.setMinimumSize(240, 270)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.reset()

    def reset(self):
        self.snake = [(5, 7), (5, 8), (5, 9)]
        self.direction = (0, -1)
        self.pending = []
        self.score = 0
        self.game_over = False
        self.paused = False
        self.food = self.spawn_food()
        self.timer.start(150)
        self.update()

    def spawn_food(self):
        free = [(x, y) for x in range(self.GRID) for y in range(self.GRID)
                if (x, y) not in self.snake]
        return random.choice(free) if free else None

    def mousePressEvent(self, event):
        self.setFocus()
        super().mousePressEvent(event)

    def hideEvent(self, event):
        self.timer.stop()  # свёрнутое окно не играет само по себе
        super().hideEvent(event)

    def showEvent(self, event):
        if not self.game_over and not self.paused:
            self.timer.start(150)
        super().showEvent(event)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Space:
            if self.game_over:
                self.reset()
            else:
                self.paused = not self.paused
                if self.paused:
                    self.timer.stop()
                else:
                    self.timer.start(150)
                self.update()
            return
        new_dir = self.KEYS.get(key)
        if new_dir is None or self.paused or self.game_over:
            super().keyPressEvent(event)
            return
        # Проверяем против последнего поставленного в очередь направления:
        # так быстрые нажатия не развернут змейку на 180° внутри одного тика
        last = self.pending[-1] if self.pending else self.direction
        if new_dir != last and new_dir != self.OPPOSITE[last] and len(self.pending) < 2:
            self.pending.append(new_dir)

    def update_game(self):
        if self.pending:
            self.direction = self.pending.pop(0)
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # хвост освободится на этом шаге, если змейка не растёт
        body = self.snake if new_head == self.food else self.snake[:-1]
        if (not 0 <= new_head[0] < self.GRID or not 0 <= new_head[1] < self.GRID
                or new_head in body):
            self.game_over = True
            self.timer.stop()
            self.update()
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
            if self.food is None:  # поле заполнено — победа
                self.game_over = True
                self.timer.stop()
        else:
            self.snake.pop()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0))

        top = 24  # строка со счётом
        side = min(self.width(), self.height() - top)
        cell = max(side // self.GRID, 1)
        board = cell * self.GRID
        ox = (self.width() - board) // 2
        oy = top + (self.height() - top - board) // 2

        painter.setPen(QColor(200, 200, 200))
        painter.drawText(8, 17, tr('score', n=self.score))

        painter.setPen(QColor(60, 60, 60))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(ox - 1, oy - 1, board + 1, board + 1)

        painter.setPen(Qt.PenStyle.NoPen)
        if self.food is not None:
            painter.setBrush(QColor(255, 50, 50))
            painter.drawEllipse(ox + self.food[0] * cell, oy + self.food[1] * cell, cell, cell)

        for i, (sx, sy) in enumerate(self.snake):
            painter.setBrush(QColor(120, 255, 120) if i == 0 else QColor(50, 200, 50))
            painter.drawRect(ox + sx * cell, oy + sy * cell, cell - 1, cell - 1)

        overlay = None
        if self.game_over:
            overlay = tr('game_over') + "\n" + tr('press_restart')
        elif self.paused:
            overlay = tr('paused')
        if overlay:
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(QRect(ox, oy, board, board),
                             Qt.AlignmentFlag.AlignCenter.value, overlay)


class SnakeGameApp(HiPEWindow):
    def __init__(self, parent_os):
        super().__init__(tr('snake'), 'snake', parent_os, 420, 500)
        self.game_widget = SnakeWidget()
        self.content_layout.addWidget(self.game_widget, stretch=1)
        hint = QLabel(tr('snake_hint'))
        hint.setStyleSheet("color: rgba(255,255,255,140); font-size: 11px;")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(hint)

    def on_activated(self):
        self.game_widget.setFocus()


class ImageViewerApp(HiPEWindow):
    EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')
    pixmap = None  # на уровне класса: resizeEvent может прийти до __init__

    def __init__(self, parent_os, img_path=None):
        super().__init__(tr('viewer'), 'viewer', parent_os, 640, 520)
        self.pixmap = None
        self.current_path = None
        self.siblings = []
        self.sibling_index = 0

        self.img_label = QLabel(tr('viewer_hint'))
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setMinimumSize(100, 100)
        self.img_label.setStyleSheet("color: white; font-size: 16px;")

        btn_style = ("QPushButton { background: %s; color: white; padding: 8px; "
                     "border-radius: 4px; } QPushButton:hover { background: rgba(255,255,255,50); }")
        top_bar = QHBoxLayout()
        btn_open = QPushButton(tr('open_image'))
        btn_open.setStyleSheet(btn_style % parent_os.accent)
        btn_open.clicked.connect(self.open_img)
        self.btn_prev = QPushButton(tr('prev'))
        self.btn_next = QPushButton(tr('next'))
        for btn in (self.btn_prev, self.btn_next):
            btn.setStyleSheet(btn_style % "rgba(255,255,255,25)")
            btn.setEnabled(False)
        self.btn_prev.clicked.connect(lambda: self.step(-1))
        self.btn_next.clicked.connect(lambda: self.step(1))
        top_bar.addWidget(btn_open)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_prev)
        top_bar.addWidget(self.btn_next)

        self.content_layout.addLayout(top_bar)
        self.content_layout.addWidget(self.img_label, stretch=1)

        if img_path:
            self.load_img(img_path)

    def open_img(self):
        start = os.path.dirname(self.current_path) if self.current_path else default_root()
        flt = f"{tr('images_filter')} (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        fn, _ = QFileDialog.getOpenFileName(self.parent_os, tr('open_image_title'), start, flt)
        if fn:
            self.load_img(fn)

    def load_img(self, path):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            self.pixmap = None
            self.img_label.setPixmap(QPixmap())
            self.img_label.setText(tr('cant_load_image', path=path))
            return
        self.pixmap = pixmap
        self.current_path = path
        self.set_title(f"{tr('viewer')} — {os.path.basename(path)}")
        self.collect_siblings(path)
        self.show_scaled()

    def collect_siblings(self, path):
        folder = os.path.dirname(path)
        try:
            names = sorted(os.listdir(folder), key=str.casefold)
        except OSError:
            names = []
        self.siblings = [os.path.join(folder, n) for n in names
                         if n.lower().endswith(self.EXTENSIONS)]
        try:
            self.sibling_index = self.siblings.index(path)
        except ValueError:
            self.siblings = [path]
            self.sibling_index = 0
        enabled = len(self.siblings) > 1
        self.btn_prev.setEnabled(enabled)
        self.btn_next.setEnabled(enabled)

    def step(self, delta):
        if len(self.siblings) < 2:
            return
        self.sibling_index = (self.sibling_index + delta) % len(self.siblings)
        self.load_img(self.siblings[self.sibling_index])

    def show_scaled(self):
        if self.pixmap is None:
            return
        scaled = self.pixmap.scaled(
            self.img_label.size(), Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        self.img_label.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.show_scaled()


class CalculatorApp(HiPEWindow):
    OPS = ('+', '−', '×', '÷')
    ROWS = [
        ['C', '⌫', '(', ')'],
        ['7', '8', '9', '÷'],
        ['4', '5', '6', '×'],
        ['1', '2', '3', '−'],
        ['0', '.', '%', '+'],
    ]
    KEYMAP = {'*': '×', '/': '÷', '-': '−', ',': '.'}
    MAX_LEN = 80

    def __init__(self, parent_os):
        super().__init__(tr('calculator'), 'calculator', parent_os, 320, 460)
        self.expr = ""
        self.just_evaluated = False
        self.showing_error = False

        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.display.setFixedHeight(56)
        self.display.setStyleSheet(
            "background: rgba(0,0,0,170); color: white; border-radius: 6px; "
            "padding: 0 10px; font-size: 24px;")
        self.content_layout.addWidget(self.display)

        grid = QGridLayout()
        grid.setSpacing(6)
        for r, row in enumerate(self.ROWS):
            for c, key in enumerate(row):
                grid.addWidget(self.make_button(key), r, c)
        self.content_layout.addLayout(grid, stretch=1)

        eq = self.make_button('=')
        eq.setStyleSheet(
            "QPushButton { background: %s; color: white; border-radius: 6px; font-size: 20px; } "
            "QPushButton:hover { background: rgba(255,255,255,60); }" % parent_os.accent)
        self.content_layout.addWidget(eq)

    def make_button(self, key):
        btn = QPushButton(key)
        btn.setMinimumHeight(48)
        btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Enter/пробел не должны «нажимать» кнопки
        bg = "rgba(255,255,255,45)" if key in self.OPS or key in 'C⌫' else "rgba(255,255,255,22)"
        btn.setStyleSheet(
            "QPushButton { background: %s; color: white; border-radius: 6px; font-size: 18px; } "
            "QPushButton:hover { background: rgba(255,255,255,60); }" % bg)
        btn.clicked.connect(lambda checked=False, k=key: self.press(k))
        return btn

    def on_activated(self):
        self.setFocus()

    def set_display(self, text):
        self.display.setText(text if text else "0")

    def show_error(self, key):
        self.expr = ""
        self.showing_error = True
        self.just_evaluated = False
        self.display.setText(tr(key))

    def press(self, key):
        if key == 'C':
            self.expr = ""
            self.just_evaluated = False
            self.showing_error = False
            self.set_display("")
            return
        if key == '=':
            self.calculate()
            return

        if self.showing_error:
            self.expr = ""
            self.showing_error = False
        if key == '⌫':
            self.expr = self.expr[:-1]
            self.just_evaluated = False
            self.set_display(self.expr)
            return

        if self.just_evaluated:
            # после «=» оператор продолжает вычисление, остальное начинает новое
            if key not in self.OPS and key != '%':
                self.expr = ""
            self.just_evaluated = False

        if len(self.expr) >= self.MAX_LEN:
            return
        if key in self.OPS:
            if not self.expr:
                if key != '−':
                    return  # выражение не может начинаться с + × ÷
            elif self.expr[-1] in self.OPS and not (key == '−' and self.expr[-1] in '×÷'):
                self.expr = self.expr[:-1]  # заменяем предыдущий оператор
                if not self.expr and key != '−':
                    return
        self.expr += key
        self.set_display(self.expr)

    def calculate(self):
        if not self.expr:
            return
        try:
            result = evaluate_expression(self.expr)
        except ZeroDivisionError:
            self.show_error('calc_div_zero')
            return
        except (ValueError, OverflowError):
            self.show_error('calc_error')
            return
        text = format_number(result)
        self.expr = text
        self.just_evaluated = True
        self.set_display(text)

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Equal):
            self.press('=')
        elif key == Qt.Key.Key_Backspace:
            self.press('⌫')
        elif key in (Qt.Key.Key_Escape, Qt.Key.Key_Delete):
            self.press('C')
        elif text:
            ch = self.KEYMAP.get(text, text)
            if ch.isdigit() or ch in '.()%+−×÷':
                self.press(ch)
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)


class SettingsApp(HiPEWindow):
    def __init__(self, parent_os):
        super().__init__(tr('settings'), 'settings', parent_os, 440, 300)
        combo_style = ("QComboBox { background: rgba(0,0,0,150); color: white; "
                       "border-radius: 5px; padding: 6px; } "
                       "QComboBox QAbstractItemView { background: #222; color: white; "
                       "selection-background-color: #0078D7; }")
        label_style = "font-size: 14px; font-weight: bold;"

        bg_lbl = QLabel(tr('bg_color'))
        bg_lbl.setStyleSheet(label_style)
        self.bg_combo = QComboBox()
        self.bg_combo.setStyleSheet(combo_style)
        for key in BACKGROUNDS:
            self.bg_combo.addItem(tr('bg_' + key), key)
        self.bg_combo.setCurrentIndex(max(0, self.bg_combo.findData(parent_os.settings['background'])))

        acc_lbl = QLabel(tr('theme'))
        acc_lbl.setStyleSheet(label_style)
        self.acc_combo = QComboBox()
        self.acc_combo.setStyleSheet(combo_style)
        for key in ACCENTS:
            self.acc_combo.addItem(tr('acc_' + key), key)
        self.acc_combo.setCurrentIndex(max(0, self.acc_combo.findData(parent_os.settings['accent'])))

        lang_lbl = QLabel(tr('lang_info', lang=tr('lang_name')))
        lang_lbl.setStyleSheet("color: rgba(255,255,255,170); font-size: 12px;")

        self.content_layout.addWidget(bg_lbl)
        self.content_layout.addWidget(self.bg_combo)
        self.content_layout.addWidget(acc_lbl)
        self.content_layout.addWidget(self.acc_combo)
        self.content_layout.addSpacing(10)
        self.content_layout.addWidget(lang_lbl)
        self.content_layout.addStretch(1)

        # Подключаем сигналы после установки начальных значений
        self.bg_combo.currentIndexChanged.connect(self.on_bg_changed)
        self.acc_combo.currentIndexChanged.connect(self.on_accent_changed)

    def on_bg_changed(self, index):
        key = self.bg_combo.currentData()
        if key in BACKGROUNDS:
            self.parent_os.apply_setting('background', key)

    def on_accent_changed(self, index):
        key = self.acc_combo.currentData()
        if key in ACCENTS:
            self.parent_os.apply_setting('accent', key)


# Реестр приложений: ключ -> класс. Settings и Taskmgr открываются в одном экземпляре.
APP_CLASSES = {
    'explorer': ExplorerApp,
    'notepad': NotepadApp,
    'calculator': CalculatorApp,
    'terminal': TerminalApp,
    'taskmgr': TaskManagerApp,
    'viewer': ImageViewerApp,
    'snake': SnakeGameApp,
    'settings': SettingsApp,
}
SINGLE_INSTANCE = ('taskmgr', 'settings')


# ==============================================================================
# 6. ПАНЕЛЬ ЗАДАЧ И ПУСК
# ==============================================================================

class StartMenu(QFrame):
    COLUMNS = 4

    def __init__(self, parent_os):
        super().__init__(parent_os.desktop)
        self.parent_os = parent_os
        self.setObjectName("HiPEStartMenu")
        self.setFixedSize(550, 600)
        self.hide()
        self.setStyleSheet(
            "#HiPEStartMenu { background-color: rgba(30, 30, 30, 240); "
            "border: 1px solid rgba(255, 255, 255, 30); border-radius: 12px; }")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(tr('search'))
        self.search_box.setFixedHeight(40)
        self.search_box.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150); color: white; "
            "border: 1px solid rgba(255, 255, 255, 30); border-radius: 20px; "
            "padding-left: 15px; font-size: 14px;")
        self.search_box.textChanged.connect(self.filter_apps)
        self.search_box.returnPressed.connect(self.launch_first_match)
        layout.addWidget(self.search_box)
        layout.addSpacing(15)

        pinned = QLabel(tr('pinned'))
        pinned.setStyleSheet("color: white; font-weight: bold; font-size: 15px; "
                             "background: transparent; border: none;")
        layout.addWidget(pinned)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.app_buttons = []  # (app_id, название, кнопка)
        for app_id in APP_CLASSES:
            name = tr(app_id)
            btn = QToolButton()
            btn.setFixedSize(100, 90)
            icon_obj, emoji = IconManager.get_icon(app_id)
            if icon_obj:
                btn.setText(name)
                btn.setIcon(icon_obj)
                btn.setIconSize(QSize(36, 36))
            else:
                btn.setText(f"{emoji}\n{name}")
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setStyleSheet(
                "QToolButton { background: transparent; color: white; border: none; "
                "border-radius: 8px; font-size: 12px; } "
                "QToolButton:hover { background: rgba(255, 255, 255, 20); }")
            btn.clicked.connect(lambda checked=False, a=app_id: self.launch_app(a))
            self.app_buttons.append((app_id, name, btn))
        layout.addLayout(self.grid)

        self.no_results = QLabel(tr('no_results'))
        self.no_results.setStyleSheet("color: rgba(255,255,255,150); background: transparent; border: none;")
        self.no_results.hide()
        layout.addWidget(self.no_results)
        layout.addStretch(1)

        user_bar = QHBoxLayout()
        user_lbl = QLabel(f"👤 <b style='font-size: 14px;'>{tr('user')}</b>")
        user_lbl.setStyleSheet("color: white; background: transparent; border: none;")
        btn_power = QPushButton("⏻")
        btn_power.setFixedSize(40, 40)
        btn_power.setStyleSheet(
            "QPushButton { background: transparent; color: white; font-size: 20px; "
            "border: none; border-radius: 8px; } QPushButton:hover { background: #FF4D4D; }")
        btn_power.clicked.connect(self.power_off)
        user_bar.addWidget(user_lbl)
        user_bar.addStretch()
        user_bar.addWidget(btn_power)
        layout.addLayout(user_bar)

        self.filter_apps("")

    def filter_apps(self, text):
        needle = text.strip().casefold()
        # убираем всё из сетки и раскладываем заново только подходящие
        for _, _, btn in self.app_buttons:
            self.grid.removeWidget(btn)
            btn.hide()
        shown = 0
        for app_id, name, btn in self.app_buttons:
            if needle in name.casefold() or needle in app_id:
                self.grid.addWidget(btn, shown // self.COLUMNS, shown % self.COLUMNS)
                btn.show()
                shown += 1
        self.no_results.setVisible(shown == 0)

    def launch_first_match(self):
        needle = self.search_box.text().strip().casefold()
        for app_id, name, _ in self.app_buttons:
            if needle in name.casefold() or needle in app_id:
                self.launch_app(app_id)
                return

    def launch_app(self, app_id):
        self.hide()
        self.parent_os.open_app(app_id)

    def power_off(self):
        self.hide()
        answer = QMessageBox.question(
            self.parent_os, tr('power_title'), tr('power_confirm'),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer == QMessageBox.StandardButton.Yes:
            self.parent_os.close()

    def show_menu(self):
        self.search_box.clear()
        self.reposition()
        self.show()
        self.raise_()
        self.search_box.setFocus()

    def reposition(self):
        desktop = self.parent_os.desktop
        taskbar_h = self.parent_os.taskbar.height() if self.parent_os.taskbar else 55
        x = max(0, (desktop.width() - self.width()) // 2)
        y = max(0, desktop.height() - taskbar_h - self.height() - 15)
        self.move(x, y)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)


class Taskbar(QFrame):
    def __init__(self, parent_os):
        super().__init__(parent_os.desktop)
        self.parent_os = parent_os
        self.setObjectName("HiPETaskbar")
        self.setFixedHeight(55)
        self.setStyleSheet(
            "#HiPETaskbar { background-color: rgba(20, 20, 20, 240); "
            "border-top: 1px solid rgba(255, 255, 255, 20); }")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)

        # Центр панели задач (Пуск + открытые приложения)
        self.center_widget = QWidget()
        self.center_layout = QHBoxLayout(self.center_widget)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(8)

        self.start_btn = QPushButton()
        self.start_btn.setFixedSize(45, 45)
        self.start_btn.setToolTip(tr('start'))
        icon_obj, emoji = IconManager.get_icon('win')
        if icon_obj:
            self.start_btn.setIcon(icon_obj)
            self.start_btn.setIconSize(QSize(24, 24))
        else:
            self.start_btn.setText(emoji)
        self.start_btn.setStyleSheet(
            "QPushButton { background: transparent; border: none; border-radius: 6px; "
            "color: white; font-size: 18px; } "
            "QPushButton:hover { background: rgba(255, 255, 255, 30); }")
        self.start_btn.clicked.connect(self.toggle_start)
        self.center_layout.addWidget(self.start_btn)

        layout.addStretch()
        layout.addWidget(self.center_widget)
        layout.addStretch()

        # Трей (справа)
        tray_layout = QHBoxLayout()
        tray_layout.setSpacing(15)

        self.lang_btn = QLabel(tr('lang_code'))
        self.lang_btn.setStyleSheet(
            "color: white; font-size: 13px; font-weight: bold; background: transparent; border: none;")

        self.clock_btn = QLabel()
        self.clock_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock_btn.setStyleSheet(
            "color: white; font-size: 12px; background: transparent; border: none;")

        tray_layout.addWidget(self.lang_btn)
        tray_layout.addWidget(self.clock_btn)
        layout.addLayout(tray_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def toggle_start(self):
        menu = self.parent_os.start_menu
        if menu.isVisible():
            menu.hide()
        else:
            menu.show_menu()

    def update_time(self):
        self.clock_btn.setText(
            f"{QTime.currentTime().toString('HH:mm')}\n{QDate.currentDate().toString('dd.MM.yyyy')}")

    def update_taskbar_apps(self):
        # Удаляем старые кнопки (индекс 0 — кнопка «Пуск»)
        for i in reversed(range(1, self.center_layout.count())):
            item = self.center_layout.itemAt(i)
            widget = item.widget() if item else None
            if widget:
                self.center_layout.removeWidget(widget)
                widget.hide()
                widget.deleteLater()

        accent = self.parent_os.accent
        for w in self.parent_os.windows:
            btn = QPushButton()
            btn.setFixedSize(45, 45)
            btn.setToolTip(w.title_text)
            icon_obj, emoji = IconManager.get_icon(w.icon_name)
            if icon_obj:
                btn.setIcon(icon_obj)
                btn.setIconSize(QSize(24, 24))
            else:
                btn.setText(emoji)
            is_active = (w is self.parent_os.active_window and w.isVisible())
            line = accent if is_active else ("rgba(255,255,255,90)" if w.isVisible() else "transparent")
            btn.setStyleSheet(
                "QPushButton { background: rgba(255, 255, 255, 15); border: none; "
                "border-radius: 6px; border-bottom: 3px solid %s; color: white; font-size: 18px; } "
                "QPushButton:hover { background: rgba(255, 255, 255, 30); }" % line)
            # Клик по кнопке: свернуть активное окно или показать/поднять остальные
            btn.clicked.connect(lambda checked=False, win=w: self.parent_os.toggle_window(win))
            self.center_layout.addWidget(btn)


# ==============================================================================
# 7. ГЛАВНЫЙ ИНТЕРФЕЙС OS
# ==============================================================================

class HiPE_OS(QMainWindow):
    ICON_ROWS = 5  # иконок в колонке на рабочем столе

    def __init__(self):
        super().__init__()
        self.windows = []
        self.active_window = None
        self.taskbar = None
        self.start_menu = None
        self.settings = load_settings()

        self.setWindowTitle("HiPE OS 11 Pro")
        self.resize(1280, 720)
        self.setMinimumSize(800, 600)

        self.desktop = QWidget()
        self.desktop.setObjectName("HiPEDesktop")
        self.desktop.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setCentralWidget(self.desktop)
        self.apply_background()

        self.main_layout = QVBoxLayout(self.desktop)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.icons_area = QWidget()
        self.icons_grid = QGridLayout(self.icons_area)
        self.icons_grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.icons_grid.setContentsMargins(15, 15, 15, 15)
        self.icons_grid.setSpacing(10)
        self.main_layout.addWidget(self.icons_area, stretch=1)

        self.start_menu = StartMenu(self)
        self.taskbar = Taskbar(self)
        self.main_layout.addWidget(self.taskbar)

        self.build_desktop_icons()

        self.desktop.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.desktop.customContextMenuRequested.connect(self.desktop_context_menu)

        # Подъём окна по клику внутрь него и закрытие меню Пуск при клике снаружи
        app = QApplication.instance()
        app.focusChanged.connect(self.on_focus_changed)
        app.installEventFilter(self)

    # --- настройки ------------------------------------------------------------

    @property
    def accent(self):
        return ACCENTS.get(self.settings.get('accent'), ACCENTS['blue'])

    def apply_background(self):
        c1, c2 = BACKGROUNDS.get(self.settings.get('background'), BACKGROUNDS['blue'])
        # Селектор по имени. Раньше стиль "background: ..." без селектора каскадом
        # красил градиентом абсолютно все дочерние виджеты
        self.desktop.setStyleSheet(
            "#HiPEDesktop { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
            "stop:0 %s, stop:1 %s); }" % (c1, c2))

    def apply_setting(self, key, value):
        self.settings[key] = value
        save_settings(self.settings)
        if key == 'background':
            self.apply_background()
        self.refresh_taskbar()

    # --- рабочий стол ---------------------------------------------------------

    def build_desktop_icons(self):
        # (название, иконка, приложение)
        items = [
            (tr('pc'), 'pc', 'explorer'),
            (tr('notepad'), 'notepad', 'notepad'),
            (tr('calculator'), 'calculator', 'calculator'),
            (tr('terminal'), 'terminal', 'terminal'),
            (tr('taskmgr'), 'taskmgr', 'taskmgr'),
            (tr('viewer'), 'viewer', 'viewer'),
            (tr('snake'), 'snake', 'snake'),
            (tr('settings'), 'settings', 'settings'),
        ]
        for i, (title, icon_n, app_id) in enumerate(items):
            self.add_desktop_icon(title, icon_n, i % self.ICON_ROWS, i // self.ICON_ROWS, app_id)

    def clear_desktop_icons(self):
        while self.icons_grid.count():
            item = self.icons_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.hide()
                widget.deleteLater()

    def add_desktop_icon(self, title, icon_n, row, col, app_id):
        btn = QToolButton()
        btn.setFixedSize(85, 85)
        icon_obj, emoji = IconManager.get_icon(icon_n)
        if icon_obj:
            btn.setText(title)
            btn.setIcon(icon_obj)
            btn.setIconSize(QSize(36, 36))
        else:
            btn.setText(f"{emoji}\n{title}")
        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        btn.setStyleSheet(
            "QToolButton { background: transparent; color: white; border: none; "
            "border-radius: 5px; font-size: 12px; } "
            "QToolButton:hover { background: rgba(255, 255, 255, 20); }")
        btn.clicked.connect(lambda checked=False, a=app_id: self.open_app(a))
        self.icons_grid.addWidget(btn, row, col)

    def refresh_desktop(self):
        IconManager.clear()
        self.clear_desktop_icons()
        self.build_desktop_icons()
        self.refresh_taskbar()

    def desktop_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet(
            "QMenu { background-color: rgba(30, 30, 30, 240); color: white; "
            "border: 1px solid #555; border-radius: 5px; font-size: 13px; } "
            "QMenu::item { padding: 5px 20px; } "
            "QMenu::item:selected { background-color: %s; }" % self.accent)

        act_refresh = QAction(tr('ctx_refresh'), self)
        act_explorer = QAction(tr('ctx_explorer'), self)
        act_term = QAction(tr('ctx_terminal'), self)
        act_settings = QAction(tr('ctx_personalize'), self)

        act_refresh.triggered.connect(self.refresh_desktop)
        act_explorer.triggered.connect(lambda: self.open_app('explorer'))
        act_term.triggered.connect(lambda: self.open_app('terminal'))
        act_settings.triggered.connect(lambda: self.open_app('settings'))

        menu.addAction(act_refresh)
        menu.addAction(act_explorer)
        menu.addAction(act_term)
        menu.addSeparator()
        menu.addAction(act_settings)
        menu.exec(self.desktop.mapToGlobal(pos))

    # --- окна -----------------------------------------------------------------

    def open_app(self, app_id, *args):
        cls = APP_CLASSES.get(app_id)
        if cls is None:
            return None
        if app_id in SINGLE_INSTANCE:
            for w in self.windows:
                if isinstance(w, cls):
                    w.activate()
                    return w
        window = cls(self, *args)
        window.activate()
        return window

    def work_area_size(self):
        """Размер области рабочего стола без панели задач."""
        taskbar_h = self.taskbar.height() if self.taskbar else 55
        return self.desktop.width(), max(self.desktop.height() - taskbar_h, 100)

    def restack(self):
        """Панель задач и меню Пуск всегда выше окон."""
        if self.taskbar:
            self.taskbar.raise_()
        if self.start_menu and self.start_menu.isVisible():
            self.start_menu.raise_()

    def set_active(self, window):
        self.active_window = window
        self.restack()
        self.refresh_taskbar()

    def window_hidden(self, window):
        """Окно свернули или закрыли."""
        if self.active_window is window:
            self.active_window = None
        self.refresh_taskbar()

    def toggle_window(self, window):
        if window.isVisible() and window is self.active_window:
            window.minimize()
        else:
            window.activate()

    def refresh_taskbar(self):
        if self.taskbar is not None:
            self.taskbar.update_taskbar_apps()

    def on_focus_changed(self, old, new):
        widget = new
        while widget is not None:
            if isinstance(widget, HiPEWindow):
                if widget in self.windows and widget is not self.active_window:
                    widget.raise_()
                    self.set_active(widget)
                return
            widget = widget.parentWidget()

    # --- системные события ----------------------------------------------------

    def eventFilter(self, obj, event):
        try:
            if (event.type() == QEvent.Type.MouseButtonPress
                    and self.start_menu is not None and self.start_menu.isVisible()):
                target = QApplication.widgetAt(event.globalPosition().toPoint())
                inside = False
                while target is not None:
                    if target is self.start_menu or target is self.taskbar.start_btn:
                        inside = True
                        break
                    target = target.parentWidget()
                if not inside:
                    self.start_menu.hide()
        except (AttributeError, RuntimeError):
            pass
        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Макет окна обновится после этого события — подгоняем позиции чуть позже
        QTimer.singleShot(0, self.relayout_overlays)

    def relayout_overlays(self):
        if self.start_menu is not None and self.start_menu.isVisible():
            self.start_menu.reposition()
        work_w, work_h = self.work_area_size()
        for w in self.windows:
            if w.is_maximized:
                w.setGeometry(0, 0, work_w, work_h)

    def closeEvent(self, event):
        app = QApplication.instance()
        if app is not None:
            app.removeEventFilter(self)
            try:
                app.focusChanged.disconnect(self.on_focus_changed)
            except (TypeError, RuntimeError):
                pass
        save_settings(self.settings)
        super().closeEvent(event)


# ==============================================================================
# ЗАПУСК
# ==============================================================================

def run(lang='ru'):
    """Запуск оболочки. Вызывается ядром: gui.run(lang)."""
    set_language(lang)
    IconManager.clear()

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    # Явно задаём размер шрифта в пунктах: иначе при стилях с font-size в пикселях
    # Qt сыплет предупреждениями QFont::setPointSize: Point size <= 0
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)

    os_window = HiPE_OS()
    os_window.show()
    app.exec()
    return 0


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else 'ru')

