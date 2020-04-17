from flask import Blueprint, request, session
from util.response import Successful_response
from util import get, post, filter_null_dict
from app.model.person_model import PersonModel
from app.middleware.login_check import get_passwd_update_time, set_passwd_update_time, update_passwd_time_string
from app.middleware.type_params import PersonParams, generate_params, get_params
from werkzeug.security import generate_password_hash

person = Blueprint("persons", __name__)

params: PersonParams = generate_params(PersonParams)


@person.route('/login', methods=post)
def login():
    #user  = PersonParams(name="12345790",passswd="11111")
    user: PersonParams = get_params(request, PersonParams, params.name, params.passwd)

    PersonModel.find_by_user_passwd(user.name, user.passwd)

    if n := get_passwd_update_time(user.name):
        q = n
    else:
        q = -100

    session.update({params.name: user.name, update_passwd_time_string: q})
    Successful_response("登录成功")


@person.route('/registered', methods=post)
def registered():
    user: PersonParams = get_params(request, PersonParams, params.name, params.passwd)
    user.passwd = generate_password_hash(user.passwd)
    PersonModel(**filter_null_dict(user)).add()
    Successful_response("注册成功")


@person.route("/logout", methods=post)
def logout():
    session.clear()
    Successful_response("登出成功")


@person.route("/change_passwd", methods=post)
def change_password():
    user: PersonParams = get_params(request, PersonParams, params.name, params.passwd, params.new_passwd)
    PersonModel.update_passwd(name=user.name, passwd=user.passwd, new_passwd=user.new_passwd)
    set_passwd_update_time(user.name)
    session.clear()
    Successful_response("修改密码成功")
