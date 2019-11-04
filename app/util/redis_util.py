# -*- coding: UTF-8 -*-
__author__ = 'hunter'

from traceback import format_exc

from rediscluster import RedisCluster
from redis import Redis, StrictRedis

from app.util.logger_util import logger
from config import conf


class Cache(object):
    def __init__(self):
        self.redis_nodes = conf.redis_nodes

        self.REDIS_MAX_CONNECTIONS = conf.REDIS_MAX_CONNECTIONS

        self.REDIS_PASSWD = conf.redis_password

        self.Header = conf.app_name + ':'

        try:
            if len(self.redis_nodes) == 1:
                self.redis_conn = StrictRedis(self.redis_nodes[0]['host'], self.redis_nodes[0]['port'],
                                              password=self.REDIS_PASSWD, max_connections=self.REDIS_MAX_CONNECTIONS)
                self.redis_conn.ping()
            else:
                self.redis_conn = RedisCluster(startup_nodes=self.redis_nodes,
                                               max_connections=self.REDIS_MAX_CONNECTIONS,
                                               password=self.REDIS_PASSWD)

        except Exception as e:
            print(format_exc())
            logger.Error(format_exc())
            logger.Error("connect redis error %s" % e)
            raise

    def set(self, key, value, REDIS_EXPIRETIME=3600):
        '''
        :param key:
        :param value:
        :param REDIS_EXPIRETIME: 缓存时间
        :return:
        '''
        return self.redis_conn.set(self.Header + key, value, REDIS_EXPIRETIME)

    def get(self, key):
        return self.redis_conn.get(self.Header + key)

    def keys(self, key):
        return self.redis_conn.keys(self.Header + key)

    def delete(self, key):
        return self.redis_conn.delete(self.Header + key)

    def exists(self, key):
        '''
        :param 检验key是否存在
        :return: True or False
        '''
        return self.redis_conn.exists(self.Header + key)

    def get_some(self, keys, pre='wedof_usercenter:cookie.'):
        pipe = self.redis_conn.pipeline()
        for key in keys:
            pipe.get(key)
        return pipe.execute()


cache = Cache()


