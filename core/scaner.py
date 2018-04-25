# coding: utf-8
import gc
import pdb
import json
import numpy as np
from time import time, sleep
from concurrent.futures import ThreadPoolExecutor

try:
    from .analyzer import Analyzer
    from .browser import ChromeBrowser, get_elements
    from .serp import SearchEngineParser
    from .mail import smail
    from .db import sa, dsn, Task, Result
except ImportError:
    from analyzer import Analyzer
    from browser import ChromeBrowser, get_elements
    from serp import SearchEngineParser
    from mail import smail
    from db import sa, dsn, Task, Result


REGULARS = {
    'title': '//title/text()',
    'metadescription': '//meta[@name="description"]/@content',
    'metakeywords': '//meta[@name="keywords"]/@content',
    'h1': '//h1//text()',
    'h2': '//h2//text()',
    'h3': '//h3//text()',
    'h4': '//h4//text()',
    'h5': '//h5//text()',
    'h6': '//h6//text()',
    'b': '//b//text()',
    'strong': '//strong//text()',
    'i': '//i//text()',
    'text': '''//body//*[not(self::script or self::a or self::h1 or self::h2 or self::h3 or self::h4 or self::h5
    or self::h6 or self::b or self::strong or self::img or self::i or self::style or self::iframe or
    self::noscript)]/text()[normalize-space()]''',
    'script': '//script//text()',
    'p': '//p//text()',
    'links': '//a/@href',
    'anchors': '//a//text()',
    'alt': '//img/@alt',
    'img': '//img/@src',
    'titles': '//@title'
}


def find_avarage(goal, data):
    fromto, avarage = {}, {}
    for k in goal:
        dig = []
        for d in data:
            if data.get(d) is not None:
                if data[d].get(k[0]) is not None:
                    dig.append(data[d][k[0]])
        try:
            bad = k[1] < min(dig) or k[1] > max(dig)
            fromto[k[0]] = (min(dig), max(dig), bool(bad))
        except Exception:
            fromto[k[0]] = (0, 0, False)
        try:
            av = round(np.mean(dig), 2)
            soso = (k[1] < av / 2) or (k[1] > av * 2)
            avarage[k[0]] = (av, bool(soso))
        except Exception:
            avarage[k[0]] = (0, False)
    return fromto, avarage


def analyze(page, data):
    data.update(page)
    a = Analyzer(init_data=data)
    res = a.analyze()
    return res


def worker(url, key, root):
    page, res = dict(), None
    with ChromeBrowser(headless=True) as br:
        t1 = time()
        page['html'] = br.get(url)
        page['load'] = time() - t1
        page['url'] = url
        page['key'] = key
        page['root'] = root
        data = get_elements(page['html'], REGULARS)
        res = analyze(page, data)
    return res


def scan(task, dbconn):
    data = dict(task)
    data['root'] = data['root'].split(';')
    data['urls'] = data['urls'].split('\n')

    goal = worker(data['url'], data['query'], data['root'])
    goal = sorted(goal.items(), key=(lambda x: x[0]))
    data['result'] = goal

    if data.get('engine'):
        se = SearchEngineParser(data['query'], data['engine']).scan()
        data['sites'] = se.sites['sites']
    else:
        data['sites'] = data['urls']

    done = dict()
    with ChromeBrowser(headless=True) as br:
        for n, s in enumerate(data['sites'], 1):
            try:
                _page, _res = dict(), None
                t1 = time()
                _page['html'] = br.get(s)
                _page['load'] = time() - t1
                _page['url'] = s
                _page['key'] = data['query']
                _page['root'] = data['root']
                _data = get_elements(_page['html'], REGULARS)
                _res = analyze(_page, _data)
                done[str(n)] = _res
            except Exception as e:
                print(type(e), e)

    data['done'] = done
    data['keys'] = sorted(done.keys(), key=lambda x: int(x))
    data['fromto'], data['avarage'] = find_avarage(goal, done)
    data['timestamp'] = data['timestamp'].isoformat()

    dbconn.execute(Result.insert().values(taskid=data['id'], data=json.dumps(data, ensure_ascii=False)))

    data['result_url'] = f"http://topomer.site/done/{data['uuid']}"
    smail(data, data['email'])
    print('Done: ', data['result_url'])


def scaner():
    """
    Main method to get data from queue. Get every 2 sec.
    :return:
    """
    engine = sa.create_engine(dsn)
    conn = engine.connect()
    executor = ThreadPoolExecutor(max_workers=4)

    while True:
        tasks = conn.execute(sa.select([Task]).where(
            sa.and_(Task.c.iscomplete == False, Task.c.inprocess == False)))
        for task in tasks:
            try:
                conn.execute(Task.update().values(inprocess=True).where(Task.c.id == task.id))
                executor.submit(scan, task, conn)
            except Exception as e:
                print(type(e), e)
            finally:
                conn.execute(Task.update().values(inprocess=False, iscomplete=True).where(Task.c.id == task.id))
            gc.collect()
        sleep(2)


if __name__ == '__main__':
    scaner()
