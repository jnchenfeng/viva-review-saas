#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/7 4:03 PM
# @Author  : Neal
# @Site    : 
# @File    : token.py
# @Software: PyCharm

import time
import requests
import datetime
import uuid

from review_saas.utils import sha256
from review_saas.const import SERVICE_URL
from typing import Dict
import redis
import hashlib

# 接口超时
API_ERROR_CODE_TIMEOUT = 50001
# 接口错误
API_ERROR_CODE_EXCEPTION = 50000
# 成功
API_SUCCESS_CODE = 20000


class Token:

    def __init__(self, client_id: str, token: str, redis_conf: Dict, token_redis_key: str = ''):
        self.__randomstr = str(int(time.time()))[-4:]
        self.__sha256str = sha256(self.__randomstr + f"{token}{client_id}")
        self.secretOperation = self.__randomstr + self.__sha256str
        self.client_id = client_id
        self.__redis_object = redis.StrictRedis(host=redis_conf.get("host"), port=redis_conf.get("port"),
                                                password=redis_conf.get("password"),
                                                db=redis_conf.get("db") or 0)
        self.token_redis_key = token_redis_key or 'viva_review_saas_token_qdf56hbf'
        self.release_force()

    def get_token_from_remote(self):
        """
        通过api获取token
        :return:
        """
        try:
            res = requests.post(f"{SERVICE_URL}/client/token/", json={
                "grant_type": "client_credentials",
                "authorization": f'{self.client_id}:{self.secretOperation}'
            }, timeout=2)
            data = res.json().get("data")
            print(res.content)
            access_expires = data.get("access_expires")
            access_expires_timestap = time.mktime(
                datetime.datetime.strptime(access_expires, '%Y-%m-%d %H:%M:%S').timetuple())
            data["access_expires"] = access_expires_timestap
            return_data = {"code": API_SUCCESS_CODE, "data": data}
        except Exception as e:
            return_data = {"code": API_ERROR_CODE_EXCEPTION, "msg": str(e)}
        return return_data

    def acquire_lock(self, lock_name, acquire_time=10, time_out=10):
        """获取一个分布式锁"""
        identifier = str(uuid.uuid4())
        end = time.time() + acquire_time
        lock = "string:lock:" + lock_name
        while time.time() < end:
            if self.__redis_object.setnx(lock, identifier):
                # 给锁设置超时时间, 防止进程崩溃导致其他进程无法获取锁
                self.__redis_object.expire(lock, time_out)
                return identifier
            elif not self.__redis_object.ttl(lock):
                self.__redis_object.expire(lock, time_out)
            time.sleep(0.001)
        return False

    def release_lock(self, lock_name, identifier):
        """通用的锁释放函数"""
        lock = "string:lock:" + lock_name
        pip = self.__redis_object.pipeline(True)
        while True:
            try:
                pip.watch(lock)
                lock_value = self.__redis_object.get(lock)
                if not lock_value:
                    return True

                if lock_value.decode() == identifier:
                    pip.multi()
                    pip.delete(lock)
                    pip.execute()
                    return True
                pip.unwatch()
                break
            except redis.WatchError:
                pass
        return False

    def release_force(self):
        lock_name = hashlib.md5('viva_review_saas_token_getlock_efgt4f'.encode()).hexdigest()
        self.__redis_object.delete(lock_name)

    def get_token(self):
        """
        获取token
        :return:
        """
        redis_key = hashlib.md5(self.token_redis_key.encode()).hexdigest()
        access_token = self.__redis_object.get(redis_key)
        if not access_token:
            lock_name = hashlib.md5('viva_review_saas_token_getlock_efgt4f'.encode()).hexdigest()
            identifier = self.acquire_lock(lock_name)
            if identifier:
                data = self.get_token_from_remote()
                if data.get("code") == API_SUCCESS_CODE:
                    access_token = data.get("data").get("access_token")
                    redis_key_timeout = int(data.get("data").get("access_expires")) - int(time.time()) - 60
                    self.__redis_object.setex(redis_key, redis_key_timeout, access_token)
                self.release_lock(lock_name, identifier)
        if not access_token:
            raise Exception('token 获取失败')
        if access_token and isinstance(access_token, bytes):
            access_token = access_token.decode()
        return access_token

    def refresh_access_token(self):
        redis_key = hashlib.md5(self.token_redis_key.encode()).hexdigest()
        lock_name = hashlib.md5('viva_review_saas_token_getlock_efgt4f'.encode()).hexdigest()
        identifier = self.acquire_lock(lock_name)
        access_token = ''
        if identifier:
            data = self.get_token_from_remote()
            if data.get("code") == API_SUCCESS_CODE:
                access_token = data.get("data").get("access_token")
                redis_key_timeout = int(data.get("data").get("access_expires")) - int(time.time()) - 60
                self.__redis_object.setex(redis_key, redis_key_timeout, access_token)
            self.release_lock(lock_name, identifier)
        if not access_token:
            raise Exception('token 获取失败')
        return access_token
