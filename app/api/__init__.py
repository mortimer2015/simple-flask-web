# -*- coding: UTF-8 -*-
__author__ = 'hunter'
from flask import Blueprint

from app.util.response_util import code_handle
from app.util.login_util import login

api = Blueprint('api', __name__)


api.after_app_request(code_handle)
api.before_app_request(login)


from . import views, errors

