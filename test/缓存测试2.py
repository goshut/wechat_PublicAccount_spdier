from functools import cache, lru_cache, cached_property
import random
from time_code import *


def t(n):
    res = 1
    for i in range(1, n):
        res *= i
    return res


# 在 3.9 版本加入.
@cache
def t0(n):
    res = 1
    for i in range(1, n):
        res *= i
    return res


@lru_cache(300)
def t1(n):
    res = 1
    for i in range(1, n):
        res *= i
    return res


if __name__ == '__main__':
    pass
    with CodeTimer("make list"):
        test_list = [random.randint(1, 300) for i in range(100000)]
    with CodeTimer("t"):
        for i in test_list:
            t(i)
    with CodeTimer("t0"):
        for i in test_list:
            t0(i)
    with CodeTimer("t1"):
        for i in test_list:
            t1(i)
