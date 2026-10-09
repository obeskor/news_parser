"""Точка входа CLI: скачать страницу, извлечь заголовки, сохранить CSV.

Запуск:
    python main.py                 # скачать свежую страницу и сохранить CSV
    python main.py --from-html     # разобрать уже скачанный data/news_page.html
"""

from __future__ import annotations

import argparse
import sys

from news_parser import config
from news_parser.fetcher import fetch_html, save_html
from news_parser.parser import looks_like_bot_stub, parse_news
from news_parser.storage import save_csv


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Парсер заголовков новостей Дзена")
    parser.add_argument(
        "--from-html",
        action="store_true",
        help="не ходить в сеть, а разобрать уже сохранённый HTML-файл",
    )
    parser.add_argument(
        "--url",
        default=config.NEWS_URL,
        help=f"адрес страницы новостей (по умолчанию: {config.NEWS_URL})",
    )
    args = parser.parse_args(argv)

    if args.from_html:
        if not config.HTML_FILE.exists():
            print(f"Файл не найден: {config.HTML_FILE}", file=sys.stderr)
            return 1
        html = config.HTML_FILE.read_text(encoding="utf-8")
        print(f"Читаю HTML из {config.HTML_FILE}")
    else:
        print(f"Скачиваю {args.url} ...")
        html = fetch_html(args.url)
        save_html(html)
        print(f"HTML сохранён в {config.HTML_FILE}")

    if looks_like_bot_stub(html):
        print("Получена заглушка (автологин/капча) вместо новостей.", file=sys.stderr)
        return 2

    items = parse_news(html)
    if not items:
        print("Заголовки не найдены — возможно, изменилась разметка страницы.", file=sys.stderr)
        return 2

    csv_path = save_csv(items, config.CSV_FILE)
    print(f"Найдено заголовков: {len(items)}")
    print(f"CSV сохранён в {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
