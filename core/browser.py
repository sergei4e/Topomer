import os
import gc
import psutil
from lxml import html
from selenium import webdriver


def get_elements(code, regulars):
        tree = html.fromstring(code)
        result = dict()
        for element in regulars:
            result[element] = tree.xpath(regulars[element])
        return result


class ChromeBrowser:
    all_processes = []
    all_children = []

    def __init__(self, socks5_proxy=None, headless=False, debug=False):
        self.debug = debug
        _driver = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver')
        _options = webdriver.chrome.options.Options()
        if headless:
            _options.add_argument("--headless")
            _options.add_argument("--no-sandbox")
            _options.add_argument("--disable-notifications")
        if socks5_proxy:
            _options.add_argument('--proxy-server=socks5://{}'.format(socks5_proxy))
        self.browser = webdriver.Chrome(options=_options, executable_path=_driver)
        self.browser.set_page_load_timeout(60)
        self.browser.set_window_size(1366, 768)
        self._process = psutil.Process(pid=self.browser.service.process.pid)
        self._children = tuple([p for p in self._process.children(recursive=True)])
        ChromeBrowser.all_processes.append(self._process)
        ChromeBrowser.all_children.append(self._children)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.kill()

    def get(self, url):
        try:
            self.browser.get(url)
            code = self.browser.page_source
        except Exception as e:
            print(type(e), e)
            code = ''
        return code

    def kill(self):
        try:
            self._process.kill()
        except Exception as e:
            if self.debug:
                print('Process', type(e), e)
        for p in self._children:
            try:
                p.kill()
            except Exception as e:
                if self.debug:
                    print('Child', type(e), e)
        ChromeBrowser.all_processes.remove(self._process)
        ChromeBrowser.all_children.remove(self._children)
        gc.collect()


if __name__ == '__main__':
    import pdb

    browser = ChromeBrowser(debug=1, headless=1)
    code = browser.get('http://proxyjudge.us/azenv.php')
    print(code)

    browser.kill()

    pdb.set_trace()

    for i in range(3):
        browser = ChromeBrowser(debug=1, headless=1)
        code = browser.get('http://proxyjudge.us/azenv.php')
        print(code)

        browser = ChromeBrowser(debug=1, headless=1)
        code = browser.get('http://proxyjudge.us/azenv.php')
        print(code)

        del(browser)

    # pdb.set_trace()

    ChromeBrowser.killall()

    pdb.set_trace()
