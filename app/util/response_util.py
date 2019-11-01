# -*- coding: UTF-8 -*-
__author__ = 'hunter'

import traceback
from functools import wraps
from flask import jsonify
from app.util.logger_util import logger
from app.util.exception_util import FlaskException


def json_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        output = dict(code=200, message='success', data={})
        try:
            ret = func(*args, **kwargs)
            data = ret.get_json()
            output['data'] = data
        except KeyError as e:
            output['code'] = '400'
            output['message'] = "缺少参数"
            output['info'] = "缺少参数{}".format(str(e))
            print(traceback.format_exc())
            return jsonify(output)
        except FlaskException as e:
            output['code'] = e.code
            output['message'] = e.message
            output['info'] = str(e)
            print(traceback.format_exc())
            return jsonify(output)
        except Exception as e:
            output['code'] = 500
            output['message'] = '网络繁忙'
            output['info'] = traceback.format_exc()
            print(traceback.format_exc())
            logger.Error(traceback.format_exc())
            logger.Error("Unexpect Error: {}".format(str(e)))
        return jsonify(output)

    return wrapper
