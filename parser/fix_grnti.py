#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_grnti.py — утилита для нормализации кодов ГРНТИ.

Алгоритм:
1) raw-код приводится к виду X.Y.Z:
      • если одна точка  &rarr; добавляем ".00"
      • если вообще нет точек &rarr; добавляем ".00.00"
2) полученный ключ ищем в справочнике public.grnti.
"""

from typing import Dict, List, Tuple
import sys
import psycopg2


# ────────────────────────────────────────────────────────
# 1. Загрузка справочника
# ────────────────────────────────────────────────────────
def load_grnti_map(cur) -> Dict[str, int]:
    """Возвращает словарь {grnti_code: id} из public.grnti."""
    cur.execute("SELECT id, grnti_code FROM public.grnti;")
    return {code.strip(): _id for _id, code in cur.fetchall()}


# ────────────────────────────────────────────────────────
# 2. Нормализация кода + фильтрация
# ────────────────────────────────────────────────────────
def _normalize_code(code: str) -> str:
    """Расширяет код до формата XX.YY.ZZ (добавляет недостающие '.00')."""
    code = code.strip()
    dot_cnt = code.count(".")

    if dot_cnt == 0:
        return f"{code}.00.00"
    elif dot_cnt == 1:
        return f"{code}.00"
    else:
        return code


def filter_links(
    pairs: List[Tuple[int, str]], grnti_map: Dict[str, int]
) -> Tuple[List[Tuple[int, int]], int]:
    """
    • pairs       — список (book_id, raw_code) из book_grnti_raw
    • grnti_map   — результат load_grnti_map

    Возвращает:
        links   — валидные пары (book_id, grnti_id) для вставки
        skipped — кол-во пропущенных строк (код не найден)
    """
    links, skipped = [], 0
    for book_id, raw_code in pairs:
        norm_code = _normalize_code(raw_code)
        grnti_id = grnti_map.get(norm_code)
        if grnti_id:
            links.append((book_id, grnti_id))
        else:
            skipped += 1
    return links, skipped


# ────────────────────────────────────────────────────────
# 3. CLI-режим (статистика)
# ────────────────────────────────────────────────────────
def _cli(dsn: str) -> None:
    with psycopg2.connect(dsn) as conn, conn.cursor() as cur:
        grnti_map = load_grnti_map(cur)

        cur.execute("SELECT book_id, grnti_code FROM public.book_grnti_raw;")
        raw_pairs = cur.fetchall()

        links, skipped = filter_links(raw_pairs, grnti_map)

        print(f"Всего пар RAW : {len(raw_pairs)}")
        print(f"Совпали       : {len(links)}")
        print(f"Пропущены     : {skipped}")


# ────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Использование: python fix_grnti.py \"<строка-DSN>\"")
    _cli(sys.argv[1])