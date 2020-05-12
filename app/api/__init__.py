# -*- coding: UTF-8 -*-
__author__ = 'hunter'
from flask import Blueprint

from app.util.response_util import code_handle

api = Blueprint('api', __name__)


api.after_app_request(code_handle)


from . import views, errors

