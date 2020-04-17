from pydantic import BaseModel
from typing import Dict

post = ["POST"]
get = ["GET"]


def filter_null_dict(d: BaseModel,  exclude={}) -> Dict:
    c = d.dict(exclude=exclude)
    n = {i: v for i, v in c.items() if v != None}
    return n


def size_pack(size):
    """
    大小包装 返回两位小数,
    :param size:
    :return:
    """
    b = ["k", "m", "g", "t"]
    for i in b:
        if (size < 1024):
            return f"{round(size, 2)}{i}"
        size = size / 1024


time_format = lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
