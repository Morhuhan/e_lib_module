#!/usr/bin/env python3
# -*- coding: utf-8 -*-
<<<<<<< HEAD
=======
"""
Нормализация поля #210 (publication info).

Возвращает кортеж (publisher, city, year):
    publisher  –  название издательства   (None, если не найдено)
    city       –  город публикации        (None, если не найдено)
    year       –  целое число-год         (None, если не найден)

Строки из примера:
    "Юнити- Дана, М, 1999"      &rarr; ("Юнити- Дана", "Москва",          1999)
    "Новоуральск, 1999"         &rarr; (None,           "Новоуральск",     1999)
    "АО АСКОН, М. СПб, 1999"    &rarr; ("АО АСКОН",     "Санкт-Петербург", 1999)
    "Cambridge, 1999"           &rarr; (None,           "Cambridge",       1999)
"""

>>>>>>> 17a3b8170ab6bda512c448c38bb77960536aa94a
from __future__ import annotations
import re
from typing import Optional, Tuple

_RE_YEAR = re.compile(r'(\d{4})\s*$')  # год, 4 цифры в конце

# Популярные аббревиатуры / синонимы для городов
_CITY_ABBR = {
    'М': 'Москва',
    'М.': 'Москва',
    'М. ': 'Москва',
    'СПб': 'Санкт-Петербург',
    'М. СПб': 'Санкт-Петербург',
<<<<<<< HEAD
    'Л': 'Ленинград',
    'Л.': 'Ленинград',
    'Екб': 'Екатеринбург',
    'Екат': 'Екатеринбург',
    'НН': 'Нижний Новгород',
    'Новосиб': 'Новосибирск',
    'Каз': 'Казань',
    'Кр': 'Краснодар',
    'РнД': 'Ростов-на-Дону',
    'Сам': 'Самара',
    'Вл': 'Владивосток',
    'Влд': 'Волгоград',
    'Кл': 'Калининград',
    'Крс': 'Красноярск',
=======
>>>>>>> 17a3b8170ab6bda512c448c38bb77960536aa94a
}

# Признаки, по которым строка скорее всего является издательством
_PUBLISHER_HINTS = (
<<<<<<< HEAD
    'изд', 'press', 'publisher',
    'ao ', 'ооо ', 'zao ', 'акц',
=======
    'изд', 'press', 'publisher',        # рус/англ слова
    'ao ', 'ооо ', 'zao ', 'акц',       # орг-формы
>>>>>>> 17a3b8170ab6bda512c448c38bb77960536aa94a
    'gmbh', 'ltd', 'srl', 'llc',
)

def _cleanup(token: str) -> str:
    """Удаляем лишние пробелы и кавычки-ёлочки."""
<<<<<<< HEAD
    token = token.strip().strip('«»“”"')
=======
    token = token.strip().strip('&laquo;&raquo;“”"')
>>>>>>> 17a3b8170ab6bda512c448c38bb77960536aa94a
    return re.sub(r'\s+', ' ', token)

def _looks_like_city(token: str) -> bool:
    """Грубая эвристика для определения города."""
    if token in _CITY_ABBR:
        return True
<<<<<<< HEAD
    if re.fullmatch(r'[A-ZА-ЯЁ][A-Za-zА-Яа-яёЁ\-]+', token):
        return True
    if token.endswith(('ск', 'ск-на-Дону', 'бург', 'град', 'город', 'инск', 'поль', 'од')):
=======
    # одно слово, первая буква заглавная, в слове нет точек/кавычек/цифр
    if re.fullmatch(r'[A-ZА-ЯЁ][A-Za-zА-Яа-яёЁ\-]+', token):
        return True
    # заканчивается на типичные русские суффиксы городов
    if token.endswith(('ск', 'ск-на-Дону', 'бург')):
>>>>>>> 17a3b8170ab6bda512c448c38bb77960536aa94a
        return True
    return False

def _looks_like_publisher(token: str) -> bool:
    low = token.lower()
    return any(h in low for h in _PUBLISHER_HINTS)

def parse_pub_info(raw: str) -> Tuple[Optional[str], Optional[str], Optional[int]]:
    """Главная точка входа."""
    if not raw:
        return None, None, None

    txt = raw.strip()

    # 1. Год (4 цифры в самом конце)
    year = None
    m = _RE_YEAR.search(txt)
    if m:
        year = int(m.group(1))
        txt = txt[:m.start()].rstrip(' ,;')

    # 2. Разбиваем остаток по запятым/точкам-с-запятой
    tokens = [_cleanup(t) for t in re.split(r'[;,]', txt) if t.strip()]

    publisher = city = None
    for token in tokens:
        # сначала пробуем определить город, чтобы не перепутать короткие аббревиатуры
        if city is None and _looks_like_city(token):
            city = _CITY_ABBR.get(token, token)
            continue
        # затем ищем издательство
        if publisher is None and _looks_like_publisher(token):
            publisher = token
            continue
        # если до сих пор не распознано, распределяем по оставшимся пустым позициям
        if publisher is None:
            publisher = token
        elif city is None:
            city = _CITY_ABBR.get(token, token)

    return publisher or None, city or None, year