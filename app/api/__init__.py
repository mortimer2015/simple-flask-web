# -*- coding: UTF-8 -*-
__author__ = 'hunter'
from traceback import format_exc

from flask import Blueprint, jsonify, Response

from app.util.exception_util import AuthException
from app.util.logger_util import logger

api = Blueprint('api', __name__)


@api.after_app_request
def code_handle(ret):
    if ret.status_code == 404:
        return jsonify({"code": 404, "data": {}, "message": "Not Found"})
    if ret.status_code == 500:
        return jsonify({"code": 500, "data": {}, "message": ret.message})

    output = {"code": 200, "message": 'success', "data": None}
    try:
        # ret = func(*args, **kwargs)
        if isinstance(ret, (dict, list, str, int)):
            output['data'] = ret
        elif isinstance(ret, set):
            output['data'] = list(ret)
        elif isinstance(ret, Response):
            if isinstance(ret.json, (dict, list)):
                # if ret.json.get("code") in []
                # data = ret.get_json()
                output['data'] = ret.get_json()
            else:
                output['data'] = ret.data.decode()
        else:
            pass
    except AuthException as e:
        output['code'] = -1
        output['message'] = e.message
        logger.error(format_exc())
        logger.error("Unexpect Error: {}".format(output))

    except Exception as e:
        output['code'] = -1
        output['message'] = str(e)
        # print(format_exc())
        logger.error(format_exc())
        logger.error("Unexpect Error: {}".format(output))
        # client.captureException()
    return jsonify(output)


from . import views, errors

