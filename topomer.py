# coding: utf-8
import json
import base64
import asyncio
import jinja2
import aiohttp_jinja2
from aiohttp import web
from threading import Thread
from datetime import datetime
from aiopg.sa import create_engine as create_engine_async

from core.scaner import scaner
from core import functions
from core.liqpay import LiqPay
from core.db import sa, connection, Promocode, Task, Result
from settings import liqpay_public_key, liqpay_private_key


async def go(db_client, sql):
    async with db_client.acquire() as conn:
        ret = []
        async for row in conn.execute(sql):
            ret.append(row)
        return ret[0] if len(ret) == 1 else ret


async def main(request):
    response = aiohttp_jinja2.render_template('index.html', request, {})
    return response


async def send(request):
    data = await request.post()
    if not await functions.validate(data):
        return aiohttp_jinja2.render_template('index.html', request, {'message': True})
    task = functions.convert(data)

    promo = data.get('promocode')
    if promo:
        promodb = await go(request.app['db'], sa.select([Promocode]).where(Promocode.c.promocode == promo))
        if not promodb:
            return web.Response(text='Unknown promocode')
        if promodb.count > 0 and promodb.expired > datetime.now():
            async with request.app['db'].acquire() as conn:
                await conn.execute(Promocode.update().values(count=promodb.count-1).where(
                    Promocode.c.id == promodb.id))
                await conn.execute(Task.insert().values(**task))
            return web.HTTPFound(f"/done/{task['uuid']}")
        else:
            return web.Response(text='Promocode Expired')
    else:
        pay = LiqPay(liqpay_public_key, liqpay_private_key)
        if data.get('top'):
            task['amount'] = 2
            return web.HTTPFound(pay.make_link(task))
        elif data.get('one'):
            if task['urls']:
                task['amount'] = len(task['urls'].split('\n')) * 0.2
                return web.HTTPFound(pay.make_link(task))
            else:
                async with request.app['db'].acquire() as conn:
                    await conn.execute(Task.insert().values(**task))
        return web.HTTPFound(f"/done/{task['uuid']}")


async def result(request):
    uuid = request.match_info['uuid']
    task = await go(request.app['db'], sa.select([Task]).where(Task.c.uuid == uuid))
    if not task:
        return web.Response(text=f'Task Not Found Error', status=404)
    result = await go(request.app['db'], sa.select([Result]).where(Result.c.taskid == task.id))
    if not result:
        return aiohttp_jinja2.render_template('wait.html', request, {'paymants': True})
    res = json.loads(result.data)
    names = functions.get_names(res)
    context = {'task': task, 'res': res, 'names': names}
    return aiohttp_jinja2.render_template('result.html', request, context)


async def frompay(request):
    try:
        post = await request.post()
        pay = base64.b64decode(post.get('data'))
        pay = json.loads(pay.decode())
        task = json.loads(base64.b64decode(pay['dae']).decode())
        if pay.get('status') == 'success' or pay.get('status') == 'sandbox':
            async with request.app['db'].acquire() as conn:
                await conn.execute(Task.insert().values(**task))
        return web.Response(text='All is OK', content_type='plain/text', status=200)
    except Exception as e:
        return web.Response(text=f'Error {e}', content_type='plain/text', status=404)


async def _start(app):
    app['db'] = await create_engine_async(minsize=2, maxsize=10, **connection)
    app['scater'] = Thread(target=scaner, args=(), daemon=True)
    app['scater'].start()


loop = asyncio.get_event_loop()
app = web.Application(loop=loop)

app.on_startup.append(_start)
# app.on_cleanup.append(_clean)

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.router.add_static('/static', 'static', name='static')

app.router.add_route('GET', '/', main)
app.router.add_route('POST', '/', send)
app.router.add_route('GET', '/done/{uuid}', result)
app.router.add_route('POST', '/asjdhakjdh', frompay)

web.run_app(app, host='localhost', port=8044)
