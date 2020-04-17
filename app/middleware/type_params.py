from pydantic import BaseModel
from util.response import Error_response
from typing import Dict
from collections import namedtuple
from flask import session


# 类本体

class PersonParams(BaseModel):
    name: str = None
    passwd: str = None
    new_passwd: str = None


class DiscParams(BaseModel):
    disc_id: int = None
    md5: str = None


class FileParams(DiscParams):
    file_name: str = None
    new_name: str = None
    is_dir: bool = None
    parent_path: str = None
    user_name: str = None
    size: float = None
    update_date: str = None
    file: str = None


class ShareParams(BaseModel):
    share_id: str = None
    user_name: str = None
    file_name: str = None
    file_uuid: str = None
    update_time: str = None
    file_path: str = None


class Share_Anal_Params(ShareParams):
    file_good: str = None
    file_share_count: str = None


# 辅助方法

def generate_params(c: BaseModel):
    l = list(c.__fields__.keys())  # ["name",passwd,new_
    n = namedtuple("n", l)  # class n :name ,passwd ne
    d = {i: i for i in l}  # {"name":"name",
    return n(**d)  # n(name="name",passwd="passwd")


def get_user(session: Dict) -> str:
    return session.get("name")


def get_params(request, params_class, *args, NN=False, name_string="user_name"):
    '''
    :NN nedd name
    '''

    if request.method == "POST":
        params = request.form
    elif request.method == "GET":
        params = request.args
    else:
        Error_response.you_ip_has_been_recorded()
    d = params
    c = lambda x: d.get(x)
    l = {i: c(i) for i in args if (not c(i) == None) and (not c(i) == "")}
    k = set(args).difference(set(list(l.keys())))
    if NN:
        l.update({name_string: get_user(session)})

    return params_class(**l) if len(k) == 0 else Error_response.parameter_incomplete(k)
