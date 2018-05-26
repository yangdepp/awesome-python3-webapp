# -*- coding: utf-8 -*-

__author__ = "yangdepp"


'''
asnyc web application
'''
#logging模块用于输出运行日志,logging.basicConfig()函数实现打印日志的基础配置
import logging; logging.basicConfig(level=logging.INFO)  
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web

#该函数的作用是处理URL，之后将与具体URL绑定
###
#   agrs:aiohttp.web.request实例，包含所有浏览器发送过来的HTTP协议中的信息
#   return:aiohttp.web.response实例，功能为构造一个HTTP响应类声明。
# ###

def index(request):
    return web.Response(body=b'<h1>Awesome</h1>',content_type='text/html',charset='utf-8')


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)         #创建web服务器实例app
    app.router.add_route('GET', '/', index)       #将url注册进router
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)      #yield from返回一个创建好的，绑定ip，端口和HTTP协议监听协程
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
