"""Настройки проекта: адреса, пути и CSS-селекторы."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Скачанная HTML-страница сохраняется для разбора и отладки.
HTML_FILE = DATA_DIR / "news_page.html"
# Итоговый CSV с заголовками.
CSV_FILE = OUTPUT_DIR / "news.csv"

# news.yandex.ru сейчас перенаправляет на Дзен, поэтому ходим сразу сюда.
NEWS_URL = "https://dzen.ru/news"

REQUEST_TIMEOUT = 30

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# CSS-селекторы карточек новостей.
# Классы Дзена содержат хеши (например, cardNewsWrapper-2Z), поэтому
# ищем по стабильной части имени класса и по атрибуту data-testid.
CARD_SELECTOR = "article[class*='cardNewsWrapper']"
TITLE_SELECTOR = "[data-testid='card-title']"
LINK_SELECTOR = "a[data-testid='card-link']"
SOURCE_SELECTOR = "[class*='author-title__text']"
TIME_SELECTOR = "[class*='card-meta'] [class*='meta__meta'] span"
