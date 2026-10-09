"""Парсер заголовков новостей Дзена (Яндекс.Новости).

Пакет умеет: скачать HTML страницы новостей, извлечь заголовки
и сохранить их в CSV.
"""

from .fetcher import fetch_html, save_html
from .parser import NewsItem, looks_like_bot_stub, parse_news
from .storage import save_csv

__all__ = [
    "fetch_html",
    "save_html",
    "parse_news",
    "looks_like_bot_stub",
    "save_csv",
    "NewsItem",
]

__version__ = "1.0.0"
