from typing import List, Dict, Tuple
from ._api import API_exception
from .custom_status import Custom_status
from flask import request


def Successful_response(data, msg=""):
    raise API_exception(data=data, state=Custom_status.successful, msg=msg)


def Unauthorized_response():
    raise API_exception(msg="登录过期请重新登录", http_code=401)


class Error_response(object):
    state = Custom_status.error

    def __init__(self, msg="", debug_msg=None):
        raise API_exception(msg=msg, state=self.state, debug_msg=debug_msg)

    @classmethod
    def parameter_incomplete(cls, l: List):
        '''

        :param l: list
        :return:
        '''

        msg = f"参数 {' '.join(l)} 没有或为空 "
        cls.__init__(cls, msg)

    # sql
    @classmethod
    def not_find_in_sql(cls, debug_msg):
        msg = f"条件不存在"
        cls.__init__(cls, msg=msg, debug_msg=debug_msg)

    @classmethod
    def user_not_exits(cls, msg="一些错误发生了", debug_msg=None):
        msg = f"用户名不存在"
        debug_msg = debug_msg
        cls.__init__(cls, msg=msg, debug_msg=debug_msg)

    @classmethod
    def password_wrong(cls, msg="一些错误发生了", debug_msg=None):
        msg = f"密码不对"
        debug_msg = debug_msg
        cls.__init__(cls, msg=msg, debug_msg=debug_msg)

    @classmethod
    def duplicate_data(cls, duplicate_data_name=None):
        msg = f"数据库中已经存在这样的信息了"
        cls.__init__(cls, debug_msg=duplicate_data_name, msg=msg)

    @classmethod
    def you_ip_has_been_recorded(cls, msg="一些错误发生了", debug_msg=None):
        msg = f"警告:请不要恶意操作,你的ip:{request.remote_addr}已被记录 "
        debug_msg = debug_msg
        cls.__init__(cls, msg=msg, debug_msg=debug_msg)

    @classmethod
    def duplicate_file_name(cls, msg="一些错误发生了", debug_msg=None):
        msg = f"文件名/文件夹名名重复"
        debug_msg = debug_msg
        cls.__init__(cls, msg=msg, debug_msg=debug_msg)

    @classmethod
    def get_file_list_none(cls, msg="一些错误发生了", debug_msg=None):
        msg = f"获取文件列表失败"
        debug_msg = debug_msg
        cls.__init__(cls, msg=msg, debug_msg=debug_msg)
