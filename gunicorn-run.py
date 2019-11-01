# -*- coding: UTF-8 -*-
__author__ = 'hunter'
import flask
from gunicorn.app.wsgiapp import WSGIApplication
from gunicorn.config import Config

from app.util.logger_util import logger
from app import conf


class StandaloneApplication(WSGIApplication):
    def __init__(self, app_name, app_version, app_uri):
        self._app_name = app_name
        self._app_version = app_version
        self._app_uri = app_uri
        super(StandaloneApplication, self).__init__()

    def load_default_config(self):
        self.cfg = Config(self._app_name)

    def init(self, parser, opts, args):
        app_uri = self._app_uri
        self.cfg.set("default_proc_name", app_uri)
        self.app_uri = app_uri
        self._output_startup_msg()

    def load(self):
        app = super(StandaloneApplication, self).load()
        if conf.debug and isinstance(app, flask.Flask):
            app.config["DEBUG"] = True
            app.config["TESTING"] = True
            app.config['TEMPLATES_AUTO_RELOAD'] = True
            app.config['APP_VERSION'] = self._app_version
            app.config['APP_URI'] = self._app_uri
        return app

    def _output_startup_msg(self):
        logger.info("=========== STARTUP ===========")
        logger.info("AppName: {%s}" % self._app_name)
        logger.info("Version: {%s}" % self._app_version)
        logger.info("Uri: {%s}" % self.app_uri)
        logger.info("Gunicron:")
        logger.info("  Bind: {%s}" % "11")
        logger.info("  Worker count: {%s}" % "4")
        logger.info("  Worker class: {%s}" % "1")
        logger.info("===============================")


www = lambda: StandaloneApplication(
    "simple-flask-web",
    "0.1",
    "simple-flask-web:app"
).run()

if __name__ == '__main__':
    www()
