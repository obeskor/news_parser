"""Сохранение новостей в CSV-файл."""

from __future__ import annotations

import csv
from pathlib import Path

from .parser import NewsItem

COLUMNS = ["title", "source", "published", "url"]


def save_csv(items: list[NewsItem], path: Path) -> Path:
    """Записывает новости в CSV (UTF-8 с BOM, чтобы Excel видел кириллицу)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        for item in items:
            writer.writerow(item.as_row())
    return path
