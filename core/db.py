import sqlalchemy as sa
from datetime import datetime
from settings import connection


dsn = 'postgresql://{user}:{password}@{host}/{database}'.format(**connection)

metadata = sa.MetaData()

Task = sa.Table(
    'queue', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('uuid', sa.String(255)),
    sa.Column('url', sa.String(255)),
    sa.Column('query', sa.String(255)),
    sa.Column('email', sa.String(255)),
    sa.Column('root', sa.String(255)),
    sa.Column('urls', sa.Text),
    sa.Column('engine', sa.String(255)),
    sa.Column('timestamp', sa.DateTime, default=datetime.now),
    sa.Column('inprocess', sa.Boolean, default=False),
    sa.Column('iscomplete', sa.Boolean, default=False),
    sa.Column('amount', sa.Float)
)

Result = sa.Table(
    'results', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('taskid', sa.Integer),
    sa.Column('data', sa.JSON)
)


Promocode = sa.Table(
    'promocodes', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('promocode', sa.String(255), unique=True),
    sa.Column('count', sa.Integer),
    sa.Column('timestamp', sa.DateTime, default=datetime.now),
    sa.Column('expired', sa.DateTime)
)


if __name__ == '__main__':
    engine = sa.create_engine(dsn)
    metadata.drop_all(engine)
    metadata.create_all(engine)
