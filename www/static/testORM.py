# create by 'yang' in 2018/8/21 
__author__ = 'yang'
import asyncio
import orm
from models import User, Blog, Comment


async def test(loop):
    await orm.create_pool(user='root', host='127.0.0.1', port=3306, password='xxx1110', db='awesome', loop=loop)
    u = User(name='yang1', email='yang1@gmail.com', passwd='1234561', image='ad1')
    await u.save()
    await orm.destory_pool()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
