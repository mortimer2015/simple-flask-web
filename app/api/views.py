# -*- coding: UTF-8 -*-
__author__ = 'hunter'
from flask import render_template, session, redirect, url_for, current_app, jsonify
from .. import db
from app.models.user import User
from ..email import send_email
from . import api
from .forms import NameForm

from app.util.logger_util import logger


@api.route("/dict")
def api_dict():
    print(2333)
    logger.error("2333")
    return {}


@api.route("/jsonify")
def api_jsonify():
    print(2333)
    logger.error("2333")
    return jsonify([])


@api.route("/str")
def api_str():
    print(2333)
    logger.error("2333")
    raise Exception("参数错误11")
    return '666'
