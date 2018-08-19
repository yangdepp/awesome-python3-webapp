import asyncio, logging

import aiomysql


def log(sql, args=()):
    logging.info('SQL: %s'.format(sql))


# 创建一个全局的连接池，每个HTTP请求都可以从连接池中直接获取数据库连接
# 使用连接池的好处是：不用频繁的打开和关闭数据库连接，能复用就复用


async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost')

    )
