# -*- coding: UTF-8 -*-
__author__ = 'hunter'
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
