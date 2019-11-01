# -*- coding: UTF-8 -*-
__author__ = 'hunter'
from argparse import Namespace

import flask
from gunicorn.app.wsgiapp import WSGIApplication
from gunicorn.config import Config

from app.util.logger_util import logger
from app import conf


class OsloConfigParser(object):
    def __init__(self, app_name):
        self._app_name = app_name
        # super(OsloConfigParser).__init__()

    def parse_args(self, args=None):
        name = self._app_name
        cfg = Namespace()
        cfg.args = []
        cfg.config = None
        # TODO: this is a non-empty list when set environ GUNICORN_CMD_ARGS
        #       refs: Application.load_config: env_args = parser.parse_args(...)
        if args:
            raise NotImplemented("GUNICORN_CMD_ARGS has not been implemented.")
        if args is not None:
            return cfg
        # oslo_log.log.register_options(CONF)
        # CONF(sys.argv[1:])
        # oslo_log.log.setup(CONF, name)
        # LOG.info("loading config")
        cfg.bind = "{}:{}".format(conf.host, conf.port)
        cfg.workers = getattr(conf, "workers", 4) or 4
        # cfg.worker_class = getattr(conf, "worker_class", "gevent") or "gevent"
        # for k, v in conf:
        #     setattr(cfg, k, v)
        if conf.debug:
            cfg.reload = True
            cfg.loglevel = "debug"
        return cfg


class StandaloneConfig(Config):
    def __init__(self, app_name):
        super(StandaloneConfig, self).__init__()
        self._app_name = app_name

    def parser(self):
        return OsloConfigParser(self._app_name)


class StandaloneApplication(WSGIApplication):
    def __init__(self, app_name, app_version, app_uri):
        self._app_name = app_name
        self._app_version = app_version
        self._app_uri = app_uri
        super(StandaloneApplication, self).__init__()

    def load_default_config(self):
        self.cfg = StandaloneConfig(self._app_name)

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
