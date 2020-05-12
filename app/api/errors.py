# -*- coding: UTF-8 -*-
__author__ = 'hunter'
from flask import render_template
from . import api


@api.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@api.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
