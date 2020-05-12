# -*- coding: UTF-8 -*-
__author__ = 'hunter'
from flask import request, abort

not_need_login = ["/api/str"]


def auth_check():
    user_name = request.cookies.get("user_name")
    if user_name:
        return True
    else:
        return False


def login():
    if request.path in not_need_login or auth_check():
        pass
    else:
        return abort(401)

