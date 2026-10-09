"""Тесты разбора HTML: извлечение заголовков и распознавание заглушки."""

import unittest

from news_parser import looks_like_bot_stub, parse_news

CARD_HTML = """
<html><body>
<article class="news-site--card-news__cardNewsWrapper-2Z card-base">
  <a class="news-site--card-news__cardLink-_n" data-testid="card-link"
     href="https://dzen.ru/news/story/aaa"> </a>
  <div class="news-site--card-part-info-wrapper__infoWrapper-2f">
    <div class="news-site--author-title__text-39">
      <span class="news-site--author-title__text-39">РИА Новости</span>
    </div>
    <div class="news-site--card-meta__cardMeta-FV">
      <div class="news-site--meta__meta-33"><span>Час назад</span></div>
    </div>
    <a class="news-site--card-news__titleLink-2Q" href="https://dzen.ru/news/story/aaa">
      <div data-testid="card-title">Первый заголовок новости</div>
    </a>
    <div data-testid="card-description">Описание новости.</div>
  </div>
</article>

<article class="news-site--card-news__cardNewsWrapper-2Z card-base">
  <a class="news-site--card-news__cardLink-_n" data-testid="card-link"
     href="https://dzen.ru/news/story/bbb"> </a>
  <div class="news-site--card-part-info-wrapper__infoWrapper-2f">
    <div><span class="news-site--author-title__text-39">ТАСС</span></div>
    <div class="news-site--card-meta__cardMeta-FV">
      <div class="news-site--meta__meta-33"><span>2 часа назад</span></div>
    </div>
    <div data-testid="card-title">Второй заголовок новости</div>
  </div>
</article>
</body></html>
"""

SSO_STUB_HTML = """
<html><body><script nonce='x'>
var it = {"host":"https://sso.dzen.ru/install?uuid=1","retpath":"https://dzen.ru/news",
"dzen":"1","root":"sso.passport.yandex.ru"};
</script></body></html>
"""


class ParseNewsTest(unittest.TestCase):
    def test_extracts_all_titles(self):
        items = parse_news(CARD_HTML)
        self.assertEqual(
            [item.title for item in items],
            ["Первый заголовок новости", "Второй заголовок новости"],
        )

    def test_extracts_metadata(self):
        first = parse_news(CARD_HTML)[0]
        self.assertEqual(first.source, "РИА Новости")
        self.assertEqual(first.published, "Час назад")
        self.assertEqual(first.url, "https://dzen.ru/news/story/aaa")

    def test_deduplicates_titles(self):
        doubled = CARD_HTML.replace(
            "Второй заголовок новости", "Первый заголовок новости"
        )
        items = parse_news(doubled)
        self.assertEqual(len(items), 1)

    def test_empty_html_gives_no_items(self):
        self.assertEqual(parse_news("<html><body></body></html>"), [])


class StubDetectionTest(unittest.TestCase):
    def test_detects_sso_stub(self):
        self.assertTrue(looks_like_bot_stub(SSO_STUB_HTML))

    def test_normal_page_is_not_stub(self):
        self.assertFalse(looks_like_bot_stub(CARD_HTML))


if __name__ == "__main__":
    unittest.main()
