import time
from flask import request, session, redirect
from app import redis
from util.response import Unauthorized_response

white_list = ["/login", "/share", "/registered"]

update_passwd_time_string = "last_update_passwd_time"


def match_string_with_start(request_path):
    for i in white_list:
        if request_path.startswith(i):
            return True
    else:
        return False


def set_passwd_update_time(name):
    return redis.hset(update_passwd_time_string, name, time.time())


def get_passwd_update_time(name):
    return redis.hget(update_passwd_time_string, name)


def login_check():
    if match_string_with_start(request.path):
        return None

    user_credentials = session.get("name")
    if not user_credentials:  # 未登录
        #return None
        Unauthorized_response()
    last_update_passwd_time = get_passwd_update_time(user_credentials)
    if not last_update_passwd_time:  # 没有修改过密码 ,在会话期间
        return None
    if session[update_passwd_time_string] != last_update_passwd_time:  # 比较数值
        session.clear()
        Unauthorized_response()
