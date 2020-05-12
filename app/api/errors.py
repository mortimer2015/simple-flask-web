# -*- coding: UTF-8 -*-
__author__ = 'hunter'
import sys
from traceback import format_exc

from flask import Response

from app.util.logger_util import logger
from . import api


@api.app_errorhandler(404)
def page_not_found(e):
    return Response(status=404)


@api.app_errorhandler(500)
def internal_server_error(e):
    logger.error(format_exc())
    ret = Response(status=500)
    ret.message = str(sys.exc_info()[1])
    ret.error_data = format_exc()
    return ret
