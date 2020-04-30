#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/7 4:03 PM
# @Author  : Neal
# @Site    : 
# @File    : token.py
# @Software: PyCharm
import random
import time
import requests
import datetime
# from requests import Timeout

from review_saas.utils import sha256
from review_saas.const import SERVICE_URL

# 接口超时
API_ERROR_CODE_TIMEOUT = 50001
# 接口错误
API_ERROR_CODE_EXCEPTION = 50000
# 成功
API_SUCCESS_CODE = 20000


class Token:

    def __init__(self, client_id: str, token: str):
        self.__randomstr = str(int(time.time()))[-4:]
        self.__sha256str = sha256(self.__randomstr + f"{token}{client_id}")
        self.secretOperation = self.__randomstr + self.__sha256str
        self.client_id = client_id
        self.token_data = {}

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
            access_expires = data.get("access_expires")
            access_expires_timestap = time.mktime(
                datetime.datetime.strptime(access_expires, '%Y-%m-%d %H:%M:%S').timetuple())
            data["access_expires"] = access_expires_timestap
            return_data = {"code": API_SUCCESS_CODE, "data": data}
        # except Timeout as timeout:
        #     return_data = {"code": API_ERROR_CODE_TIMEOUT, "msg": str(timeout)}
        except Exception as e:
            return_data = {"code": API_ERROR_CODE_EXCEPTION, "msg": str(e)}
        return return_data

    def get_token(self):
        """
        获取token
        :return:
        """
        if len(self.token_data) == 0 or self.token_data.get("access_expires") - time.time() <= 3 * 60:
            data = self.get_token_from_remote()
            if data.get("code") == API_SUCCESS_CODE:
                self.token_data = data.get("data")
        token = self.token_data.get("access_token")
        if not token:
            raise Exception('token 获取失败')
        return token
