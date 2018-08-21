# create by 'yang' in 2018/8/21
import asyncio, functools, inspect

__author__ = 'yang'


def get(path):
    # 定义一个get/path装饰器
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        # @get('/')函数中的参数path，放到wrapper函数的__route__属性中
        # 默认的GET请求方式放到__method__中
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper

    return decorator


def post(path):
    # 定义一个post/path装饰器
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper

    return decorator


def get_required_kw_args(fn):
    args = []
    # inspect.signature(fn)返回inspect.Signature类型的对象，值为fn这个函数的所有参数
    # 值是有序字典，key为参数名，str类型，value是inspect.Parameter类型的对象，包含参数各种信息
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        # 参数是关键词参数，并且没有默认值就append到args中
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)

