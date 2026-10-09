"""Разбор HTML страницы новостей и извлечение заголовков."""

from __future__ import annotations

from dataclasses import dataclass

from bs4 import BeautifulSoup

from . import config


@dataclass
class NewsItem:
    """Одна новость: заголовок и сопутствующие поля карточки."""

    title: str
    source: str = ""
    published: str = ""
    url: str = ""

    def as_row(self) -> dict[str, str]:
        return {
            "title": self.title,
            "source": self.source,
            "published": self.published,
            "url": self.url,
        }


def looks_like_bot_stub(html: str) -> bool:
    """Похожа ли страница на заглушку (автологин/капча) вместо новостей."""
    if "var it = {" in html and "sso" in html:
        return True
    markers = ("captcha", "Подтвердите, что запросы отправляли вы")
    return any(marker in html for marker in markers)


def parse_news(html: str) -> list[NewsItem]:
    """Извлекает список новостей из HTML страницы."""
    soup = BeautifulSoup(html, "lxml")
    items: list[NewsItem] = []
    seen: set[str] = set()

    for card in soup.select(config.CARD_SELECTOR):
        title_el = card.select_one(config.TITLE_SELECTOR)
        if title_el is None:
            continue

        title = title_el.get_text(" ", strip=True)
        if not title or title in seen:
            continue
        seen.add(title)

        link_el = card.select_one(config.LINK_SELECTOR) or card.select_one("a[href]")
        source_el = card.select_one(config.SOURCE_SELECTOR)
        time_el = card.select_one(config.TIME_SELECTOR)

        items.append(
            NewsItem(
                title=title,
                source=source_el.get_text(" ", strip=True) if source_el else "",
                published=time_el.get_text(" ", strip=True) if time_el else "",
                url=link_el["href"] if link_el and link_el.has_attr("href") else "",
            )
        )

    return items
