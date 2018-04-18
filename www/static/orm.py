# -*- coding: utf-8 -*-

__author__ = "yangdepp"

# 创建一个连接池，每个HTTP请求都可以直接从连接中直接获取数据库连接，不必频繁打开关闭数据库连接

import asyncio
import logging
import aiomysql

# 定义一个log()方法
# args是一个空的tuple


def log(sql, args=()):
    logging.info('SQL: %s', sql)


# dict提供get方法，d = {'jack':1},d.get('jack',2)可以自己指定值为2
async def create_pool(loop, **kw):
    logging.info('ceate database connection pool...')
    global __pool  # 设置成全局的变量，可以在函数内部改变
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),  # 指定为localhost
        port=kw.get('port', 3306),  # 指定为3306
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),  # 缺省情况下将编码设置为utf-8
        autocommit=kw.get('autocommit', True),  # 自动提交事务
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

# 要执行INSERT、UPDATE、DELETE语句，可以定义一个通用execute()函数
# 因为这3种SQL的执行都需要相同的参数，以及返回一个整数表示影响的行数


async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?','%s'), args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected