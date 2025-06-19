#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_authors.py – нормализация и разбор авторов
=============================================

Модуль предоставляет утилиты для работы с именами авторов из
MARC-полей #700 / #701 и произвольных списков авторов.

Функции
-------
parse_author_700_701(field_text: str) -> str
    Извлекает фамилию и инициалы из текста MARC-поля #700 / #701
    (подполя A – фамилия, B – инициалы) и возвращает строку
    «Фамилия И.О.».

normalize_author(full: str) -> str
    Приводит строку «Фамилия И.О.» к каноническому виду:
        • убирает лишние пробелы;
        • гарантирует ровно один пробел между фамилией и инициалами;
        • прибавляет «.» к инициалам, если их нет;
        • для однобуквенных инициалов типа «А. С.» убирает пробел и добавляет точки («А.С.»);
        • возвращает пустую строку, если на входе пусто.

split_authors(raw: str) -> list[str]
    Разбивает строку вида «Иванов И.И.; Петров П.П.»
    на список индивидуально нормализованных авторов
    без точных дубликатов.
"""

from __future__ import annotations
import re
from typing import Dict, List

# ─────────────────────────── helpers ────────────────────────────
_SUBFIELD_SEP = "\x1f"          # разделитель подполя в ИРБИС-экспорте
_INITIAL_RE   = re.compile(r"^[A-ZА-ЯЁ]$", re.IGNORECASE)   # однобуквенная инициала


def _parse_subfields(field_text: str) -> Dict[str, str]:
    """
    Преобразует строку MARC-поля вида
        '$AИванов$BИ.О.'  (где  = \x1f)
    в словарь {'A': 'Иванов', 'B': 'И.О.'}.

    В экспортах ИРБИС иногда вместо \x1f используют '^'.
    """
    text = field_text.replace("^", _SUBFIELD_SEP)
    parts = text.split(_SUBFIELD_SEP)
    subf: Dict[str, str] = {}
    for chunk in parts:
        chunk = chunk.strip()
        if chunk:
            subf[chunk[0]] = chunk[1:].strip()
    return subf


# ─────────────────────────── public API ─────────────────────────
def parse_author_700_701(field_text: str) -> str:
    """
    «\x1fAИванов\x1fBИ.О.»      → «Иванов И.О.»
    «^AПетров^BП.П.»            → «Петров П.П.»
    Если фамилия или инициалы отсутствуют, возвращается то, что найдено.
    """
    subf = _parse_subfields(field_text)
    last_name = subf.get("A", "").strip()
    initials  = subf.get("B", "").strip()
    if initials and not initials.endswith("."):
        # «И.О» → «И.О.»
        initials = ".".join(i.strip(".") for i in initials.split(".")) + "."
    return f"{last_name} {initials}".strip()


def normalize_author(full: str) -> str:
    """
    «Евтеев  Ю.И.»     → «Евтеев Ю.И.»
    «Чернышев А .А»    → «Чернышев А.А.»
    «Пукина А. С.»     → «Пукина А.С.»

    Правила:
      • множественные пробелы сводятся к одному;
      • между фамилией и инициалами ровно один пробел;
      • инициалы приводятся к «И.О.» (с точками);
      • пробелы между однобуквенными инициалами убираются;
      • регистр букв фамилии сохраняется как есть;
      • пустая или пробельная строка → ''.
    """
    full = full.replace("\u202f", " ")          # узкие неразрывные → обычные
    full = re.sub(r"\s+", " ", full).strip()    # множественные пробелы

    if not full:
        return ""

    parts = full.split(" ", maxsplit=1)
    if len(parts) == 1:                         # только фамилия
        return parts[0]

    last_name, rest = parts
    rest = re.sub(r"\s+", "", rest)             # убираем пробелы в инициалах
    buf = []

    i = 0
    while i < len(rest):
        ch = rest[i]
        if ch == ".":
            i += 1
            continue
        if _INITIAL_RE.match(ch):
            buf.append(ch.upper())
            i += 1
            # Если следующая буква тоже инициала, не добавляем точку пока
            if i < len(rest) and _INITIAL_RE.match(rest[i]):
                continue
            buf.append(".")
        else:
            # Неожиданный символ – возвращаем исходные инициалы без изменений
            return f"{last_name} {rest}"

    # Убедимся, что строка заканчивается точкой
    if buf and buf[-1] != ".":
        buf.append(".")
    initials = "".join(buf)
    return f"{last_name} {initials}"


def split_authors(raw: str) -> List[str]:
    """
    «Иванов И.И.;  Петров П.П.» → ['Иванов И.И.', 'Петров П.П.']

    • Точка с запятой «;» – разделитель авторов.
    • Каждый автор нормализуется normalize_author().
    • Полные дубликаты удаляются, порядок сохраняется.
    """
    if not raw:
        return []

    out: List[str] = []
    for token in raw.split(";"):
        token = normalize_author(token)
        if token and token not in out:
            out.append(token)
    return out