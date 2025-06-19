#!/usr/bin/env python3
<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
fix_bbk.py — нормализация кодов ББК.
"""

from typing import Dict, List, Tuple
import sys
import re
import psycopg2

# Регулярное выражение для разделения кодов ББК по внешним разделителям
_SPLIT_CODES_RE = re.compile(r'[;,]\s*|\s{2,}')
# Регулярное выражение для разделения субполей внутри строки
_SUBFIELD_SPLIT_RE = re.compile(r'[A-Z]')
# Регулярное выражение для удаления префиксов субполей (A, B, C и т.д.)
_SUBFIELD_PREFIX_RE = re.compile(r'^[A-Z]\s*')
# Регулярное выражение для удаления однобуквенных префиксов (A, B, G и т.д.) в начале
_PREFIX_RE = re.compile(r'^[A-Z]\s*')

def load_bbk_map(cur) -> Dict[str, int]:
    cur.execute("SELECT id, bbk_abb FROM public.bbk;")
    # ключи в UPPER для регистронезависимого поиска
    return {code.upper(): _id for _id, code in cur.fetchall()}
=======
"""
fix_bbk.py
──────────
Функции для фильтрации связок (book_id, bbk_code) по уже существующим
записям справочника BBK.  Можно:
    • импортировать   (использует parse_irbis_file.py),
    • запускать отдельно: python fix_bbk.py "<DSN>"
"""

from typing import Dict, List, Tuple
import sys, psycopg2

# ────────────────────────────────────────────────────────────────────
def load_bbk_map(cur) -> Dict[str, int]:
    """Возвращает {bbk_abb: bbk_id}."""
    cur.execute("SELECT id, bbk_abb FROM public.bbk;")
    return {code: _id for _id, code in cur.fetchall()}

>>>>>>> 17a3b8170ab6bda512c448c38bb77960536aa94a

def filter_links(
    pairs: List[Tuple[int, str]], bbk_map: Dict[str, int]
) -> Tuple[List[Tuple[int, int]], int]:
<<<<<<< HEAD
    links, skipped = [], 0
    for book_id, code in pairs:
        bbk_id = bbk_map.get(code.upper())
=======
    """
    Принимает [(book_id, bbk_code), …] и сопоставление code&rarr;id.
    Возвращает (валидные_связи, количество_пропущенных).
    """
    links, skipped = [], 0
    for book_id, code in pairs:
        bbk_id = bbk_map.get(code)
>>>>>>> 17a3b8170ab6bda512c448c38bb77960536aa94a
        if bbk_id:
            links.append((book_id, bbk_id))
        else:
            skipped += 1
    return links, skipped
<<<<<<< HEAD

def collect(pairs: List[Tuple[str, str]]) -> List[str]:
    """
    Собирает и нормализует коды ББК из полей 606 и 610.
    Args:
        pairs: Список кортежей (тег, содержимое), где тег — '606' или '610'.
    Returns:
        Список нормализованных кодов ББК.
    """
    codes = []
    for tag, content in pairs:
        if tag not in ('606', '610'):
            continue
        # Разделяем содержимое на коды по внешним разделителям
        for code in _SPLIT_CODES_RE.split(content.strip()):
            code = code.strip()
            if not code:
                continue
            # Разделяем код на субполя (например, Техническая МеханикаBтеоретическая Механика)
            subfields = _SUBFIELD_SPLIT_RE.split(code)
            for subfield in subfields:
                subfield = subfield.strip()
                if not subfield:
                    continue
                # Удаляем префикс субполя (например, B)
                subfield = _SUBFIELD_PREFIX_RE.sub('', subfield).strip()
                # Удаляем однобуквенный префикс (например, A, G)
                subfield = _PREFIX_RE.sub('', subfield).strip()
                if not subfield:
                    continue
                # Удаляем скобки с содержимым, например, (ЕТГС)
                subfield = re.sub(r'\([^)]*\)', '', subfield).strip()
                # Приводим к формату Title Case
                subfield = subfield.title()
                if subfield:
                    codes.append(subfield)
    return codes

=======
# ────────────────────────────────────────────────────────────────────
>>>>>>> 17a3b8170ab6bda512c448c38bb77960536aa94a
def _cli(dsn: str) -> None:
    with psycopg2.connect(dsn) as conn, conn.cursor() as cur:
        bbk_map = load_bbk_map(cur)
        cur.execute("SELECT book_id, bbk_code FROM public.book_bbk_raw;")
        raw_pairs = cur.fetchall()

        links, skipped = filter_links(raw_pairs, bbk_map)
<<<<<<< HEAD
        print(f"Всего пар RAW : {len(raw_pairs)}")
        print(f"Совпали       : {len(links)}")
        print(f"Пропущены     : {skipped}")
=======
        print(f"Всего пар RAW: {len(raw_pairs)}")
        print(f"Совпали: {len(links)}   |   Пропущены: {skipped}")

        # Для демонстрации выведем первые 10 строк INSERT-ов.
        print("\nПример INSERT-ов:")
        for book_id, bbk_id in links[:10]:
            print(f"INSERT INTO public.book_bbk (book_id, bbk_id) "
                  f"VALUES ({book_id}, {bbk_id});")
>>>>>>> 17a3b8170ab6bda512c448c38bb77960536aa94a

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Использование: python fix_bbk.py \"<строка-DSN>\"")
    _cli(sys.argv[1])