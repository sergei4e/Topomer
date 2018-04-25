# coding: utf-8
from urllib.parse import quote

try:
    from core.browser import ChromeBrowser, get_elements
    from core.logs import logger
except ImportError:
    from browser import ChromeBrowser, get_elements
    from logs import logger


ENGINES = {
    'google.com.ua': {
        'url': 'http://www.google.com.ua/search?num=10&hl=ru&q=',
        'regulars': {'sites': '//h3[@class="r"]/a/@href'}
    },
    'google.ru': {
        'url': 'http://www.google.ru/search?num=10&hl=ru&q=',
        'regulars': {'sites': '//h3[@class="r"]/a/@href'}
    },
    'google.com': {
        'url': 'http://www.google.com/search?num=10&hl=en&q=',
        'regulars': {'sites': '//h3[@class="r"]/a/@href'}
    },
    'google.co.uk': {
        'url': 'http://www.google.co.uk/search?num=10&hl=en&q=',
        'regulars': {'sites': '//h3[@class="r"]/a/@href'}
    },
    'google.co.in': {
        'url': 'http://www.google.co.in/search?num=10&hl=en&q=',
        'regulars': {'sites': '//h3[@class="r"]/a/@href'}
    },
    'google.de': {
        'url': 'http://www.google.de/search?num=10&hl=ge&q=',
        'regulars': {'sites': '//h3[@class="r"]/a/@href'}
    },
    'google.com.au': {
        'url': 'http://www.google.com.au/search?num=10&hl=en&q=',
        'regulars': {'sites': '//h3[@class="r"]/a/@href'}
    },
    'google.pl': {
        'url': 'http://www.google.pl/search?num=10&hl=pl&q=',
        'regulars': {'sites': '//h3[@class="r"]/a/@href'}
    },
    'google.by': {
        'url': 'http://www.google.by/search?num=10&hl=ru&q=',
        'regulars': {'sites': '//h3[@class="r"]/a/@href'}
    }
}


class SearchEngineParser:
    def __init__(self, query, engine='google.com.ua'):
        self.query = query
        self.sites = []
        self.engine = ENGINES[engine]['url']
        self.regulars = ENGINES[engine]['regulars']
        logger.debug('Init SerpParser class')

    def scan(self):
        with ChromeBrowser(headless=True) as br:
            url = self.engine + quote(self.query)
            page = br.get(url)
            self.sites = get_elements(page, self.regulars)
        return self
