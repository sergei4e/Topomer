from uuid import uuid4
from datetime import datetime, timedelta
from db import sa, dsn, Promocode


engine = sa.create_engine(dsn)
conn = engine.connect()


def generate(num):
    for i in range(num):
        promo = str(uuid4())
        timestamp = datetime.now()
        expired = timestamp + timedelta(days=30)
        data = {'promocode': promo, 'timestamp': timestamp, 'expired': expired, 'count': 10}
        conn.execute(Promocode.insert().values(**data))
        print(promo)


if __name__ == '__main__':
    import sys
    num = int(sys.argv[1])
    generate(num)
