# coding: utf-8
import nltk
from transliterate import translit
from .param_names import names
from uuid import uuid4
# from script.logs import logger


async def validate(post):
    """
    Function validates intup data.
    post:
        'url': 'https://www.farmpartsstore.com/Misc-Mower-Conditioner-Parts-Hay-Tool-Parts-s/411345.htm',
        'query': 'dentists in nyc',
        'root': 'dentist,nyc'
    """
    if 'http' not in post.get('url'):
        return False
    if '@' not in post.get('email') or '.' not in post.get('email') or ' ' in post.get('email').strip():
        return False
    if len(post.get('query')) < 4:
        return False
    return True


def get_root(phrase):
    """
    Function converts input russian string to list of words roots.
    :param phrase: string data
    :return: list with roots of words
    """
    words = phrase.split()
    an = nltk.stem.snowball.RussianStemmer()
    root = [an.stem(x) for x in words if len(x) > 2]
    return ';'.join(root)


def convert(post):
    '''
    Function converts POST input data from to dict format.
    :param post:
    :return:
    '''
    url = post.get('url').strip().lower()
    query = post.get('query').strip().lower()
    email = post.get('email').strip().lower()
    engine = post.get('search-system')
    urls = [post.get('url{}'.format(x)).strip() for x in range(10) if post.get('url{}'.format(x))]
    data = {'url': url,
            'query': query,
            'email': email,
            'root': get_root(query),
            'urls': '\n'.join(urls),
            'engine': engine,
            'uuid': str(uuid4()),
            'amount': 0
            }
    # logger.debug('Add to analyze: {}'.format(data))
    return data


def get_names(values):
    result = {}
    for k in values['result']:
        k = k[0]
        i = '_'.join(k.split('_')[:2])
        w = k.split('_')[-1:][0]
        if names.get(k):
            if 'keyphrase_slug' in k:
                result[k] = names[k].format(translit(values["query"], 'ru', reversed=True))
            elif 'keyphrase' in k:
                result[k] = names[k].format(values["query"])
            else:
                result[k] = names[k]
        else:
            if 'meta' in k or 'slug' in k:
                i = '_'.join(k.split('_')[:3])
            if 'root' in k or 'root_slug' in k:
                result[k] = names[i].format(w)
            elif 'density' in k:
                result[k] = names[i].format(w, w)
            else:
                result[k] = None

    return result
