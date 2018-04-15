# -*- coding: utf-8 -*-

__author__ = "yangdepp"

# 创建一个连接池，每个HTTP请求都可以直接从连接中直接获取数据库连接，不必频繁打开关闭数据库连接

import asyncio
import logging
import aiomysql


async def create_pool(loop, **kw):
    logging.info('ceate database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )

# 执行select语句，用select函数执行，需要传入SQL语句和SQL参数

###
# 紧跟with后面的语句被求值后，返回对象的__enter__()方法被调用，这个方法的返回值将被赋值给as后面的变量。
# 当with后面的代码块全部被执行完之后，将调用前面返回对象的__exit__()方法。
# class Sample:
#     def __enter__(self):
#         print "In __enter__()"
#         return "Foo"

#     def __exit__(self, type, value, trace):
#         print "In __exit__()"

# def get_sample():
#     return Sample()

# with get_sample() as sample:
#     print "sample:", sample
############输出########################
# In __enter__()
# sample: Foo
# In __exit__()
#
# ###


async def select(sql, args, size=None):
    log(sql, args)
    global __pool
    async with __pool.get() as conn:
        # 创建一个结果为字典的游标
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # 执行sql语句，将sql语句中的'?'替换为'%s'
            await cur.execute(sql.replace('?', '%s'), args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows returned: %s' % len(rs))
        return rs
