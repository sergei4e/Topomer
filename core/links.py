import requests
import xmltodict
from settings import siteexplorer_key

try:
    from core.text_utils import Utils
    from core.logs import logger
except ImportError:
    from text_utils import Utils
    from logs import logger
from pprint import pprint


class Links:
    def __init__(self, keyword, root):
        self.keyword = keyword
        self.root = root
        self.data = None
        self.lin_domains = 0
        self.lin_ips = 0
        self.lin_subnets = 0
        self.lin_links = 0
        self.lin_homepages = 0
        self.lin_nofollow = 0
        self.lin_textlinks = 0
        self.lin_rank = 0
        self.linanchors = []
        self.lintext = ''
        self.lin_words_count = 0
        self.lin_words_unique = 0
        self.lin_keyphrase = 0
        self.lin_root = {x: 0 for x in root}
        self.lin_density = {x: 0 for x in root}

    def get_data(self, mask='111', nxt='', query=''):
        url = 'http://siteexplorer.info/api.aspx'
        params = {'auth': siteexplorer_key,
                  'mask': mask,
                  'query': query,
                  'next': nxt}
        response = requests.get(url, params=params)
        self.data = xmltodict.parse(response.content)

    # def open_data(self):
    #     with open('data/apidata.pickle', 'rb') as f:
    #         self.data = pickle.load(f)
    #
    # def save_data(self):
    #     with open('data/apidata.pickle', 'wb') as f:
    #         pickle.dump(self.data, f)

    def metadata(self):
        self.lin_domains = float(self.data.get('API').get('meta').get('@domains').replace(',', ''))
        self.lin_ips = float(self.data.get('API').get('meta').get('@ips').replace(',', ''))
        self.lin_subnets = float(self.data.get('API').get('meta').get('@subnets').replace(',', ''))
        self.lin_links = float(self.data.get('API').get('meta').get('@links').replace(',', ''))
        self.lin_homepages = float(self.data.get('API').get('meta').get('@homepages').replace(',', ''))
        self.lin_nofollow = float(self.data.get('API').get('meta').get('@nofollow').replace(',', ''))
        self.lin_textlinks = float(self.data.get('API').get('meta').get('@textlinks').replace(',', ''))
        self.lin_rank = float(self.data.get('API').get('meta').get('@rank').replace(',', ''))

    def text_data(self):
        if not self.data.get('API').get('results'):
            self.make()
            return
        if type(self.data.get('API').get('results').get('result').get('domains').get('domain')) is list:
            for dm in self.data.get('API').get('results').get('result').get('domains').get('domain'):
                if type(dm.get('pages').get('page')) is list:
                    for li in dm.get('pages').get('page'):
                        self.linanchors.append(li.get('@anchor'))
                else:
                    self.linanchors.append(dm.get('pages').get('page').get('@anchor'))
        else:
            self.linanchors.append(self.data.get('API').get('results').get('result').get('domains').get('domain')
                                   .get('pages').get('page').get('@anchor'))
        self.make()

    def make(self):
        self.lintext = ' '.join(self.linanchors)
        self.lin_words_count, \
        self.lin_keyphrase, \
        self.lin_root, \
        self.lin_density, \
        self.lin_words_unique = Utils.get_count(self.lintext, self.keyword, self.root)

    def analyze(self, query):
        try:
            self.get_data(query=query)
            self.metadata()
            self.text_data()
            logger.debug(self.__dict__)
        except Exception as e:
            logger.exception(e)
            logger.debug(self.__dict__)

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
                        else:
                            continue
        logger.debug(res)
        return res


if __name__ == '__main__':
    res = Links('интернет гипермаркет', ('интернет', 'гипермаркет')).analyze('http://abo.ua/')
    pprint(res)
    print(len(res))

    res = Links('стиральные машины',
                ('стир', 'машин')).analyze('http://palladium.ua/stiralnye_i_sushilnye_mashiny.html')
    pprint(res)
    print(len(res))
