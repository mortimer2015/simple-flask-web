# -*- coding: UTF-8 -*-
__author__ = 'hunter'


class FlaskException(Exception):
    """
    统一异常处理
    在json_response中对异常进行统一拦截
    """
    def __init__(self, message, code=500, *args, **kwargs):
        super().__init__()
        self.message = message
        self.code = code


class ParameterException(Exception):
    def __init__(self, message, *args, **kwargs):
        super().__init__()
        self.message = message
        self.type = '缺少参数'

