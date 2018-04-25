import base64
import hashlib
import json


class LiqPay(object):
    def __init__(self, public_key, private_key):
        self._public_key = public_key
        self._private_key = private_key
        self._host = 'https://www.liqpay.com/api/3/checkout'

    def _make_signature(self, *args):
        joined_fields = ''.join(x for x in args)
        return base64.b64encode(hashlib.sha1(joined_fields.encode('utf-8')).digest())

    def _make_data(self, task):
        dae = base64.b64encode(json.dumps(task).encode('utf-8'))
        data = {
            "version": 3,
            "language": "ru",
            "public_key": self._public_key,
            "action": "pay",
            "amount": task['amount'],
            "currency": "USD",
            "description": "Оплата за анализ web страницы",
            "order_id": task['uuid'],
            "result_url": f"http://topomer.site/done/{task['uuid']}",
            "server_url": f"http://topomer.site/asjdhakjdh",
            "dae": dae.decode('utf-8'),
            # "sandbox": 1
        }
        return json.dumps(data).encode('utf-8')

    def make_link(self, task):
        data = base64.b64encode(self._make_data(task)).decode('utf-8')
        signature = self._make_signature(self._private_key, data, self._private_key).decode('utf-8')
        link = "{}?data={}&signature={}".format(self._host, data, signature)
        return link
