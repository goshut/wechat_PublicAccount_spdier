import functools
import random
from time_code import *


def cache_by_members(*members):
    # 自定义一个缓存装饰器，根据成员的值来判断是否命中缓存
    def decorator(func):
        # 创建一个字典来存储缓存
        cache = {}

        @functools.wraps(func)
        def wrapper(self):
            # 获取成员的值，构造一个缓存的键
            key = tuple(getattr(self, member) for member in members)
            # 如果键在缓存中，直接返回缓存的值
            if key in cache:
                return cache[key]
            # 否则，调用原函数，计算结果，并更新缓存
            else:
                result = func(self)
                cache[key] = result
                return result

        return wrapper

    return decorator


class WxGzhSpider:
    project_dir = "/home/user/project"

    def __init__(self):
        self.dir_name = ""
        self.output_dir = f"{WxGzhSpider.project_dir}/output"

    # 调换一下装饰器的顺序，先执行 @property ，再执行 @cache_by_members
    @property
    @cache_by_members("dir_name", "output_dir")
    def save_dir(self):
        # 使用自定义的缓存装饰器，根据 dir_name 和 output_dir 的值来缓存结果
        res = f"{self.output_dir}/{self.dir_name}"
        return res


class Test:
    def __init__(self):
        self.a = 1
        self.b = 2

    @functools.cache
    def get_add(self, a, b):
        return a * b


@functools.cache
def t0(n):
    res = 1
    for i in range(1, n):
        res *= i
    return res


def t(n):
    res = 1
    for i in range(1, n):
        res *= i
    return res


if __name__ == '__main__':
    # a = WxGzhSpider()
    # 去掉 a.save_dir 后面的括号，访问这个属性，而不是调用这个属性
    # print(a.save_dir)
    # a.dir_name = "545"
    # print(a.save_dir)
    # 被@property修饰后取值方式变了
    # print(a.save_dir.__closure__[0].cell_contents)
    # print(a.__getattribute__('save_dir').__closure__)
    # print(functools.cache_info(a.save_dir))
    pass
    with CodeTimer("make list"):
        test_list = [random.randint(1, 10) for i in range(100)]
    with CodeTimer("t0"):
        for i in test_list:
            t0(i)
    with CodeTimer("t"):
        for i in test_list:
            t(i)
