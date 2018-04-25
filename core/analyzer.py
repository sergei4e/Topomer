# coding: utf-8
import re
import pdb
from urllib.parse import urlparse, unquote, urljoin
from pprint import pprint
from transliterate import translit
try:
    from .text_utils import Utils
    from .rds import Rds
    from .links import Links
    from .logs import logger
except ImportError:
    from text_utils import Utils
    from rds import Rds
    from links import Links
    from logs import logger


class Analyzer(Utils):

    def __init__(self, init_data):

        self.keyword = init_data.get('key')
        self.root = init_data.get('root')
        self.keywordslug = ''
        self.rootslug = []

        # self.po_sition = init_data.get('pos')
        self.page_load_time = init_data.get('load')

        self.url = init_data.get('url')
        # self.u_rl = self.url
        self.url_root = {}
        self.url_root_slug = {}
        self.url_keyphrase = 0
        self.url_keyphrase_slug = 0
        self.url_length = 0
        self.url_level = 0
        self.url_params_count = 0
        self.url_https = 0
        self.url_ismain = 0

        self.domain = ''
        self.domain_root = {}
        self.domain_level = 0
        self.domain_country = 0
        self.domain_is_www = 0

        self.title = init_data.get('title')
        self.title_words_count = 0
        self.title_keyphrase = 0
        self.title_root = {}
        self.title_density = {}
        self.title_words_unique = 0

        self.metadescription = init_data.get('metadescription')
        self.meta_description_words_count = 0
        self.meta_description_keyphrase = 0
        self.meta_description_root = {}
        self.meta_description_density = {}
        self.meta_description_words_unique = 0

        self.metakeywords = init_data.get('metakeywords')
        self.meta_keywords_words_count = 0
        self.meta_keywords_keyphrase = 0
        self.meta_keywords_root = {}
        self.meta_keywords_density = {}
        self.meta_keywords_words_unique = 0

        self.h1 = init_data.get('h1')
        self.h1_words_count = 0
        self.h1_keyphrase = 0
        self.h1_root = {}
        self.h1_density = {}
        self.h1_words_unique = 0
        self.h1_count = 0

        self.h2 = init_data.get('h2')
        self.h2_words_count = 0
        self.h2_keyphrase = 0
        self.h2_root = {}
        self.h2_density = {}
        self.h2_words_unique = 0
        self.h2_count = 0

        self.h3 = init_data.get('h3')
        self.h3_words_count = 0
        self.h3_keyphrase = 0
        self.h3_root = {}
        self.h3_density = {}
        self.h3_words_unique = 0
        self.h3_count = 0

        self.h4 = init_data.get('h4')
        self.h4_words_count = 0
        self.h4_keyphrase = 0
        self.h4_root = {}
        self.h4_density = {}
        self.h4_words_unique = 0
        self.h4_count = 0

        self.h5 = init_data.get('h5')
        self.h5_words_count = 0
        self.h5_keyphrase = 0
        self.h5_root = {}
        self.h5_density = {}
        self.h5_words_unique = 0
        self.h5_count = 0

        self.h6 = init_data.get('h6')
        self.h6_words_count = 0
        self.h6_keyphrase = 0
        self.h6_root = {}
        self.h6_density = {}
        self.h6_words_unique = 0
        self.h6_count = 0

        self.text = init_data.get('text')
        self.text_words_count = 0
        self.text_keyphrase = 0
        self.text_root = {}
        self.text_density = {}
        self.text_sentenses = 0
        self.text_words_unique = 0

        self.b = init_data.get('b')
        self.b_words_count = 0
        self.b_keyphrase = 0
        self.b_root = {}
        self.b_density = {}
        self.b_words_unique = 0
        self.b_count = 0

        self.strong = init_data.get('strong')
        self.strong_words_count = 0
        self.strong_keyphrase = 0
        self.strong_root = {}
        self.strong_density = {}
        self.strong_words_unique = 0
        self.strong_count = 0

        self.i = init_data.get('i')
        self.i_words_count = 0
        self.i_keyphrase = 0
        self.i_root = {}
        self.i_density = {}
        self.i_words_unique = 0
        self.i_count = 0

        self.alt = init_data.get('alt')
        self.alt_words_count = 0
        self.alt_keyphrase = 0
        self.alt_root = {}
        self.alt_density = {}
        self.alt_words_unique = 0
        self.alt_count = 0

        self.anchors = init_data.get('anchors')
        self.anchors_words_count = 0
        self.anchors_keyphrase = 0
        self.anchors_root = {}
        self.anchors_density = {}
        self.anchors_words_unique = 0

        self.titles = init_data.get('titles')
        self.titles_words_count = 0
        self.titles_keyphrase = 0
        self.titles_root = {}
        self.titles_density = {}
        self.titles_words_unique = 0
        self.titles_count = 0

        self.img = init_data.get('img')
        self.img_count = 0
        self.img_keyphrase_slug = 0
        self.img_root_slug = {}
        self.img_unique = 0
        self.img_self = 0
        self.img_out = 0

        self.links = init_data.get('links')
        self.links_count = 0
        self.links_unique = 0
        self.links_keyphrase_slug = 0
        self.links_root_slug = {}
        self.links_self = 0
        self.links_out = 0
        self.links_without_href = 0

        self.html = init_data.get('html')
        self.html_size = 0
        self.html_keyphrase = 0
        self.html_root = {}
        self.html_keyphrase_slug = 0
        self.html_root_slug = {}
        self.html_clean_text_length = 0
        self.html_clean_code_length = 0
        self.html_ads_count = 0
        self.html_scripts_count = 0

        logger.debug('Init Analyzer {}'.format(self))

    def url_domain_method(self):
        self.keywordslug = translit(self.keyword.replace(' ', '-'), 'ru', reversed=True)
        self.rootslug = [translit(x.replace(' ', '-'), 'ru', reversed=True) for x in self.root]

        clean_url = unquote(self.url)
        p = urlparse(self.url)

        if p.scheme == 'https':
            self.url_https = 1

        for r in self.root:
            self.url_root[r] = clean_url.count(r)
        for rs in self.rootslug:
            self.url_root_slug[rs] = clean_url.count(rs)

        self.url_length = len(self.url)
        self.url_level = len(p.path.split('/')) - 1

        if p.query:
            self.url_params_count = len(p.query.split('&'))

        self.domain = p.netloc

        for r in self.root:
            self.domain_root = self.domain.count(r)

        self.domain_level = len(self.domain.split('.'))
        if self.domain.split('.')[-1] == 'ua':
            self.domain_country = 1
        if self.domain.split('.')[0] == 'www':
            self.domain_is_www = 1
        if self.url.endswith(self.domain + '/') or self.url.endswith(self.domain):
            self.url_ismain = 1

        logger.debug('Analyzer url_domain_method done')

    def title_meta_description_method(self):
        self.title_words_count, \
        self.title_keyphrase, \
        self.title_root, \
        self.title_density, \
        self.title_words_unique = Utils.get_count(' '.join(self.title), self.keyword, self.root)

        self.meta_description_words_count, \
        self.meta_description_keyphrase, \
        self.meta_description_root, \
        self.meta_description_density, \
        self.meta_description_words_unique = Utils.get_count(' '.join(self.metadescription), self.keyword, self.root)

        self.meta_keywords_words_count, \
        self.meta_keywords_keyphrase, \
        self.meta_keywords_root, \
        self.meta_keywords_density, \
        self.meta_keywords_words_unique = Utils.get_count(' '.join(self.metakeywords), self.keyword, self.root)

        logger.debug('Analyzer title_meta_description_method done')

    def h_method(self):
        self.h1_words_count, \
        self.h1_keyphrase, \
        self.h1_root, \
        self.h1_density, \
        self.h1_words_unique = Utils.get_count(' '.join(self.h1), self.keyword, self.root)
        self.h1_count = len(self.h1)

        self.h2_words_count, \
        self.h2_keyphrase, \
        self.h2_root, \
        self.h2_density, \
        self.h2_words_unique = Utils.get_count(' '.join(self.h2), self.keyword, self.root)
        self.h2_count = len(self.h2)

        self.h3_words_count, \
        self.h3_keyphrase, \
        self.h3_root, \
        self.h3_density, \
        self.h3_words_unique = Utils.get_count(' '.join(self.h3), self.keyword, self.root)
        self.h3_count = len(self.h3)

        self.h4_words_count, \
        self.h4_keyphrase, \
        self.h4_root, \
        self.h4_density, \
        self.h4_words_unique = Utils.get_count(' '.join(self.h4), self.keyword, self.root)
        self.h4_count = len(self.h4)

        self.h5_words_count, \
        self.h5_keyphrase, \
        self.h5_root, \
        self.h5_density, \
        self.h5_words_unique = Utils.get_count(' '.join(self.h5), self.keyword, self.root)
        self.h5_count = len(self.h5)

        self.h6_words_count, \
        self.h6_keyphrase, \
        self.h6_root, \
        self.h6_density, \
        self.h6_words_unique = Utils.get_count(' '.join(self.h6), self.keyword, self.root)
        self.h6_count = len(self.h6)

        logger.debug('Analyzer h_method done')

    def text_method(self):
        self.text_words_count, \
        self.text_keyphrase, \
        self.text_root, \
        self.text_density, \
        self.text_words_unique = Utils.get_count('. '.join(self.text), self.keyword, self.root)
        # self.text_count = len(self.text)
        # self.te_xt = Utils.text_normalizer(' '.join(self.text))

        self.b_words_count, \
        self.b_keyphrase, \
        self.b_root, \
        self.b_density, \
        self.b_words_unique = Utils.get_count(' '.join(self.b), self.keyword, self.root)
        self.b_count = len(self.b)

        self.strong_words_count, \
        self.strong_keyphrase, \
        self.strong_root, \
        self.strong_density, \
        self.strong_words_unique = Utils.get_count(' '.join(self.strong), self.keyword, self.root)
        self.strong_count = len(self.strong)

        self.i_words_count, \
        self.i_keyphrase, \
        self.i_root, \
        self.i_density, \
        self.i_words_unique = Utils.get_count(' '.join(self.i), self.keyword, self.root)
        self.i_count = len(self.i)

        self.alt_words_count, \
        self.alt_keyphrase, \
        self.alt_root, \
        self.alt_density, \
        self.alt_words_unique = Utils.get_count(' '.join(self.alt), self.keyword, self.root)
        self.alt_count = len(self.alt)

        self.anchors_words_count, \
        self.anchors_keyphrase, \
        self.anchors_root, \
        self.anchors_density, \
        self.anchors_words_unique = Utils.get_count(' '.join(self.anchors), self.keyword, self.root)
        # self.anchors_count = len(self.anchors)

        self.titles_words_count, \
        self.titles_keyphrase, \
        self.titles_root, \
        self.titles_density, \
        self.titles_words_unique = Utils.get_count(' '.join(self.titles), self.keyword, self.root)
        self.titles_count = len(self.titles)

        logger.debug('Analyzer text_method done')

    def images_method(self):

        for n, l in enumerate(self.img):
            self.img[n] = urljoin('http://{}/'.format(self.domain), l)

        self.img_count = len(self.img)
        img_txt = ' '.join(self.img)

        data = Utils.get_count(img_txt, self.keywordslug, self.rootslug)

        self.img_root_slug = data[2]
        self.img_keyphrase_slug = data[1]
        self.img_unique = len(set(self.img))
        self.img_self = img_txt.count(self.domain)
        self.img_out = len(self.img) - img_txt.count(self.domain)

        logger.debug('Analyzer images_method done')

    def links_method(self):

        self.links_without_href = self.links.count('')

        for n, l in enumerate(self.links):
            self.links[n] = urljoin('http://{}/'.format(self.domain), l)

        self.links_count = len(self.links)
        self.links_unique = len(set(self.links))
        links_txt = ' '.join(self.links)

        data = Utils.get_count(links_txt, self.keywordslug, self.rootslug)

        self.links_keyphrase_slug = data[1]
        self.links_root_slug = data[2]
        self.links_self = links_txt.count(self.domain)
        self.links_out = self.links_count - self.links_self

        logger.debug('Analyzer links_method done')

    def html_method(self):
        self.html_size = len(self.html)

        data1 = Utils.get_count(self.html, self.keyword, self.root)
        data2 = Utils.get_count(self.html, self.keywordslug, self.rootslug)

        self.html_keyphrase = data1[1]
        self.html_root = data1[2]

        self.html_keyphrase_slug = data2[1]
        self.html_root_slug = data2[2]

        htmlnoscript = str(self.html)
        for x in re.compile(r"<script.*?</script>", re.S).findall(self.html):
            htmlnoscript = htmlnoscript.replace(x, '')
        self.html_clean_text_length = len(' '.join(re.compile(r"(?<=[>]).*?(?=[<])", re.S).findall(htmlnoscript)))
        self.html_clean_code_length = len(' '.join(re.compile(r"(?<=[<]).*?(?=[>])", re.S).findall(htmlnoscript)))
        self.html_ads_count = self.html.count('googleadservices') + self.html.count('id="yandex_ad')
        self.html_scripts_count = len([x for x in re.compile(r"<script.*?</script>", re.S).findall(self.html)])

        logger.debug('Analyzer html_method done')

    def analyze(self):
        self.url_domain_method()
        self.title_meta_description_method()
        self.h_method()
        self.text_method()
        self.images_method()
        self.links_method()
        self.html_method()

        res = {}
        for i in self.__dict__:
            if '_' in i:
                if type(self.__dict__[i]) is not dict:
                    res[i] = round(self.__dict__[i], 2)
                else:
                    for j in self.__dict__[i]:
                        if j in self.root:
                            # res[i+'_'+str(self.root.index(j)+1)] = round(self.__dict__[i][j], 2)
                            res[i + '_' + str(j)] = round(self.__dict__[i][j], 2)
                        elif j in self.rootslug:
                            # res[i+'_'+str(self.rootslug.index(j)+1)] = round(self.__dict__[i][j], 2)
                            res[i + '_' + str(j)] = round(self.__dict__[i][j], 2)
                        else:
                            continue

        # logger.debug('Analyze first done')
        # logger.debug(len(res))

        # links_data = Links(self.keyword, self.root).analyze(self.url)
        # res.update(links_data)

        # logger.debug('Analyze links done')
        # logger.debug(len(res))

        # rds = Rds(self.url).analyze()
        # res['a_ge'], res['google_index'] = rds.a_ge, rds.index_count

        # logger.debug('Analyze (rds = All) done')
        # logger.debug(len(res))
        # logger.debug(res)

        return res


if __name__ == '__main__':

    example = {
        'key': 'макароны оптом киев',
        'root': ['макарон', 'опт', 'киев'],
        'url': 'http://www.ua.all.biz/makarony-bgg1056017',
        'pos': 14,
        'load': 3.123,
        'title': ['Макароны в Украине по цене от 1 UAH. Купить макароны оптом, недорого, продажа на Allbiz Украина'],
        'meta_description': ['''Хотите купить макароны по цене от 1 UAH? На торговом портале Allbiz
        Украина есть предложения по оптовой, недорогой продаже макарон.'''],
        'meta_keywords': ['макароны, купить макароны, киев, цена'],
        'h1': ['макароны'],
        'h2': ['макароны', 'купить макароны в киеве'],
        'h3': ['макароны', 'купить макароны в киеве'],
        'h4': ['макароны', 'купить макароны в киеве'],
        'h5': ['макароны', 'купить макароны в киеве'],
        'h6': [],
        'text': ['Подробнее', 'Уточнить цену', '''У большинства семей минимум раз в неделю на столе
        присутствует всемирно популярное блюдо, именуемое у нас макаронами, но во многих странах
        называемое пастой. Многие уверены, что блюдо это итальянское, однако, для истинных почитателей
        изделий не секрет, что в Европу макароны были привезены из Китая известным путешественником Марко Поло.'''],
        'b': ['Европа', 'Америка', 'Африка'],
        'strong': ['цена', 'купить', 'подробнее'],
        'i': ['цена', 'купить', 'подробнее'],
        'alt': ['цена на макароны рожки', 'купить макароны итальянские', 'подробнее о макаронах Украины'],
        'anchors': ['цена на макароны рожки', 'купить макароны итальянские', 'подробнее о макаронах Украины'],
        'titles': ['цена на макароны рожки', 'купить макароны итальянские', 'подробнее о макаронах Украины'],
        'img': ['http://www.ua.all.biz/img/ua/catalog/middle/340158.jpeg',
                'http://www.ua.all.biz/img/ua/catalog/middle/340158.jpeg',
                'http://www.ua.all.biz/img/ua/catalog/middle/340159.jpeg',
                'http://www.s.all.biz/img/ua/catalog/middle/makarony.jpeg',
                'http://www.ua.all.biz/img/ua/catalog/middle/340161.jpeg'],
        'links': ["http://www.ua.all.biz/bassejny-kompozitnye-bgg1043688",
                  "http://www.ua.all.biz/auditorskoe-soprovozhdenie-bsg2104",
                  "http://www.ua.all.biz/posuda-bgg1003120",
                  "http://www.ua.all.biz/golubcy-bgg1066359",
                  "/shampuni-dlya-okrashennyh-volos-bgg1040539",
                  "/obuchenie-bsg9740",
                  "/voditelskie-kursy-bsg6055",
                  '/posuda-bgg1003120',
                  "http://www.ua.all.biz/zhir-svinoj-bgg1055952",
                  "http://www.ua.all.biz/formy-dlya-keksov-bgg1042545",
                  "http://kiev.all.biz/borony-bgg1000395",
                  "",
                  "#top",
                  "http://facebook.com/makarony-bgg1056017",
                  "http://www.ua.all.biz/makarony-bgg1056017"],
        'html': '''<div class="b-tabs"><p class="active b-tabs-single-title">Другие страны</p>
        <div class="tab-content">а</div></div><script type="text/javascript">
        12412948214098102948019248 142094821094821904 142904821094821904 </script>'''
    }

    a = Analyzer(init_data=example)
    res = a.analyze()

    pprint(res)
    print(len(res))
    pdb.set_trace()
