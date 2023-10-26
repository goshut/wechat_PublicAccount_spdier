import os
import re


def clean_str(str_):
    return re.sub(r'[0-9.,"/\'?:!;*`^<>《》]', '', str_)


def mkdir(dir_path):
    if not dir_path: return -1
    if not os.path.exists(dir_path): os.mkdir(dir_path)
    return 0


if __name__ == '__main__':
    dict1 = {'aa': 66}
    print(dict1.get('aa', 0))
    print(dict1.setdefault('aa', 0))
    print(dict1)
