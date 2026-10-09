"""Загрузка HTML страницы новостей и обход автологина Дзена."""

from __future__ import annotations

import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from . import config


def build_session() -> requests.Session:
    """Создаёт сессию requests с нужными заголовками."""
    session = requests.Session()
    session.headers.update(config.HEADERS)
    return session


def _needs_sso(html: str) -> bool:
    """True, если вместо новостей пришла страница автологина Дзена."""
    return "var it = {" in html and "sso" in html


def _complete_sso(
    session: requests.Session, html: str, timeout: int
) -> requests.Response:
    """Проходит JS-форму автологина: POST на адрес из переменной it.host."""
    soup = BeautifulSoup(html, "lxml")
    script = soup.find("script")
    script_text = script.string or "" if script else ""

    match = re.search(r"var it = (\{.*?\});", script_text, re.S)
    if not match:
        raise RuntimeError("Не удалось разобрать форму автологина Дзена")
    it = json.loads(match.group(1))

    form = {"retpath": it["retpath"], "dzen": it.get("dzen", "1")}
    container = re.search(
        r"name = 'container';.*?value = '([^']+)'", script_text, re.S
    )
    if container:
        form["container"] = container.group(1)

    return session.post(it["host"], data=form, timeout=timeout)


def fetch_html(url: str = config.NEWS_URL, timeout: int = config.REQUEST_TIMEOUT) -> str:
    """Скачивает страницу новостей и возвращает её HTML-текст."""
    session = build_session()

    response = session.get(url, timeout=timeout)
    response.raise_for_status()

    if _needs_sso(response.text):
        _complete_sso(session, response.text, timeout)
        response = session.get(url, timeout=timeout)
        response.raise_for_status()

    response.encoding = response.apparent_encoding or response.encoding
    return response.text


def save_html(html: str, path: Path = config.HTML_FILE) -> Path:
    """Сохраняет HTML страницы в файл."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return path
