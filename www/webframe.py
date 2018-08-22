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


# 检查参数，将所有没有默认值的命名关键字参数名 作为一个tuple返回
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


# 检查参数，将函数所有的命名关键字参数名，作为一个tuple返回
def get_named_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)


# 检查是否有命名关键字参数，返回布尔值
def has_named_kw_args(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True


# 检查是否有关键字参数，返回布尔值
def has_var_kw_arg(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True


# 检查函数是否有request参数，返回布尔值。若有request参数，检查改参数是否为该函数最后一个参数，否则抛出异常
def has_request_arg(fn):
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == 'request':
            found = False
            continue
        if found and (
                param.kind != inspect.Parameter.VAR_POSITIONAL
                and param.kind != inspect.Parameter.KEYWORD_ONLY
                and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError(
                'request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found
