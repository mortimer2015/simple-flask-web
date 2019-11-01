# -*- coding: UTF-8 -*-
__author__ = 'hunter'
from app import create_app, conf


app = create_app()

if __name__ == '__main__':
    print("============当前环境：{}==========".format(conf.description))
    app.run(conf.host, conf.port, conf.debug)

