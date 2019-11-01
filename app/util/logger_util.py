# -*- coding: UTF-8 -*-
__author__ = 'hunter'
import fcntl
import logging
import os
import sys
import time
from logging.handlers import TimedRotatingFileHandler

from config import conf


class MultiCompatibleTimedRotatingFileHandler(TimedRotatingFileHandler):
    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        # 兼容多进程并发 LOG_ROTATE
        if not os.path.exists(dfn):
            f = open(self.baseFilename, 'a')
            fcntl.lockf(f.fileno(), fcntl.LOCK_EX)
            if os.path.exists(self.baseFilename):
                os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


class Logger(object):
    def __init__(self, level=conf.DEBUG):
        if level:
            level = logging.DEBUG
        else:
            level = logging.INFO
        # 创建log目录
        if not os.path.exists(conf.log_dir):
            os.makedirs(conf.log_dir)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(message)s')
        # info warn debug
        self.logger = logging.getLogger('simple_example')
        self.logger.setLevel(level)
        self.log = MultiCompatibleTimedRotatingFileHandler(conf.log_dir + conf.log_file, when='D',
                                                           encoding="utf-8", interval=1, backupCount=30)
        self.error_log = MultiCompatibleTimedRotatingFileHandler(conf.log_dir + conf.error_log_file, when='D',
                                                                 encoding="utf-8", interval=1, backupCount=30)
        self.log.setLevel(level)
        self.log.setFormatter(self.formatter)
        self.logger.addHandler(self.log)

    def info(self, msg):
        msg = "%s:%s %s] %s" % ("/".join(sys._getframe().f_back.f_code.co_filename.split('/')[-3:]),
                                sys._getframe().f_back.f_lineno, sys._getframe().f_back.f_code.co_name, msg)
        self.logger.info(msg)

    def debug(self, msg):
        msg = "%s:%s %s] %s" % ("/".join(sys._getframe().f_back.f_code.co_filename.split('/')[-3:]),
                                sys._getframe().f_back.f_lineno, sys._getframe().f_back.f_code.co_name, msg)
        self.logger.debug(msg)

    def warning(self, msg):
        msg = "%s:%s %s] %s" % ("/".join(sys._getframe().f_back.f_code.co_filename.split('/')[-3:]),
                                sys._getframe().f_back.f_lineno, sys._getframe().f_back.f_code.co_name, msg)
        self.logger.warning(msg)

    def error(self, msg):
        msg = "%s:%s %s] %s" % ("/".join(sys._getframe().f_back.f_code.co_filename.split('/')[-3:]),
                                sys._getframe().f_back.f_lineno, sys._getframe().f_back.f_code.co_name, msg)
        error_logger = logging.getLogger('simple_example')
        error_logger.setLevel(logging.ERROR)

        self.error_log.setLevel(logging.ERROR)
        self.error_log.setFormatter(self.formatter)
        error_logger.addHandler(self.error_log)
        error_logger.error(msg)


logger = Logger()


if __name__ == '__main__':
    logger = Logger(logging.DEBUG)
    logger.info('info message')
    logger.debug('debug message')
    logger.warning('warn message')
    logger.error('error message')
