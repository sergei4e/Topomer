import json
import requests
import time
import xmltodict
import base64
from datetime import datetime
from urllib.parse import urlparse
from settings import rds_key

try:
    from core.logs import logger
except ImportError:
    from logs import logger


class Rds:

    def __init__(self, link):
        self.link = link
        self.a_ge = 0
        self.index_count = 0
        self.__headers__ = {
            'Authorization': 'Basic ' + base64.b64encode(rds_key).decode('utf-8'),
            'Content-Type': 'text/xml; charset=utf-8',
            'Host': 'recipdonor.com:977'
        }

    def get_index(self):
        domain = urlparse(self.link).netloc
        IG = '''
        <InitSession>
            <Parameters>
                <TaskVariant>IG</TaskVariant>
            </Parameters>
            <DomainNames>
                <string>{}</string>
            </DomainNames>
            <Refresh>true</Refresh>
        </InitSession>'''.format(domain)
        url_new = 'http://www.recipdonor.com:977/api/session/new'
        response1 = requests.put(url_new, headers=self.__headers__, data=IG)
        id = json.loads(response1.content.decode('utf-8')).get('Id')
        url_get = 'http://www.recipdonor.com:977/api/session/get/' + id
        response2 = requests.get(url_get, headers=self.__headers__)
        data = json.loads(response2.content.decode('utf-8'))
        while data.get('Progress') == 0:
            time.sleep(1)
            response2 = requests.get(url_get, headers=self.__headers__)
            data = json.loads(response2.content.decode('utf-8'))
        self.index_count = data['Domains'][0]['Values'][0]['Value']

    def get_age(self):
        domain = urlparse(self.link).netloc
        url = 'http://recipdonor.com:998/api/age/' + domain
        response = requests.get(url, headers=self.__headers__)
        data = xmltodict.parse(response.content.decode('utf-8'))
        # data.get('dateTime') == '2008-02-01T14:40:00'
        date_object = datetime.strptime(data.get('dateTime'), '%Y-%m-%dT%H:%M:%S')
        self.a_ge = (datetime.now() - date_object).days

    def analyze(self):
        try:
            self.get_index()
            self.get_age()
        except Exception as e:
            logger.exception(e)

        logger.debug(self.__dict__)
        return self

if __name__ == '__main__':
    rds = Rds('http://www.all.biz/')
    rds.get_index()
    rds.get_age()
    print(rds.__dict__)
