# -*- coding: UTF-8 -*-
__author__ = 'hunter'
from flask import render_template
from . import api


@api.app_errorhandler(404)
def page_not_found(e):
    return {"code": 404, "data": {}, "message": "Not Found"}


@api.app_errorhandler(500)
def internal_server_error(e):
    return {"code": 500, "data": {}, "message": "Internal Error"}
