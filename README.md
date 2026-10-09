# Парсер новостей Яндекса (Дзен)

Python-приложение, которое скачивает HTML-страницу новостей, извлекает
заголовки с источниками и ссылками и сохраняет их в CSV-файл.
Используются `requests` и `BeautifulSoup`.

## Что важно знать про источник

`news.yandex.ru` сейчас **перенаправляет** на `https://dzen.ru/news`, а Дзен
сначала отдаёт короткую страницу автологина (JS-форму, а не новости).
Приложение проходит этот автологин автоматически (`news_parser/fetcher.py`),
поэтому в CSV попадают настоящие заголовки, а не заглушка.

Проверка на заглушку есть в `looks_like_bot_stub()` — если вместо новостей
придёт форма входа или капча, приложение сообщит об этом и не создаст CSV.

## Структура проекта

```
parser_news/
├── main.py                 # точка входа (CLI)
├── news_parser/            # пакет с логикой
│   ├── __init__.py
│   ├── config.py           # адрес, пути, CSS-селекторы
│   ├── fetcher.py          # скачивание HTML + обход автологина
│   ├── parser.py           # разбор HTML → список заголовков
│   └── storage.py          # запись CSV
├── tests/
│   └── test_parser.py      # тесты разбора
├── requirements.txt
└── .gitignore
```

Во время работы создаются папки:

- `data/`   — сохранённый HTML страницы (`news_page.html`);
- `output/` — итоговый CSV (`news.csv`).

## Установка

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```bat
python main.py
```

Результат:

```
Скачиваю https://dzen.ru/news ...
HTML сохранён в ...\data\news_page.html
Найдено заголовков: 27
CSV сохранён в ...\output\news.csv
```

Разобрать уже скачанный HTML (без обращения к сети):

```bat
python main.py --from-html
```

## CSV

Файл `output/news.csv` в кодировке UTF-8 с BOM (кириллица корректно
открывается в Excel) со столбцами:

| Столбец     | Значение                          |
|-------------|-----------------------------------|
| `title`     | заголовок новости                 |
| `source`    | источник (РИА Новости, ТАСС, ...) |
| `published` | время публикации                  |
| `url`       | ссылка на новость                 |

## Тесты

```bat
python -m unittest discover -s tests -v
```

## Как устроен разбор HTML

Классы Дзена содержат хеши (например, `cardNewsWrapper-2Z`), поэтому селекторы
ищут по стабильной части имени класса и по `data-testid`:

- карточка новости — `article[class*='cardNewsWrapper']`;
- заголовок — `[data-testid='card-title']`;
- ссылка — `a[data-testid='card-link']`;
- источник — `[class*='author-title__text']`;
- время — `[class*='card-meta'] [class*='meta__meta'] span`.

Все селекторы собраны в `news_parser/config.py`.
