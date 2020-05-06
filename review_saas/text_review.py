#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/7 9:23 PM
# @Author  : Neal
# @Site    : 
# @File    : img_review.py
# @Software: PyCharm


from review_saas import utils
from review_saas.oauth_token import Token
import requests
from review_saas.const import SERVICE_URL


class TextReview:
    def __init__(self, client_id: str, token: str):
        self.client_id = client_id
        self.token = token
        self.token_get = Token(client_id, token)

    def review(self, text_id: int, secret_id: str, user_id: str, text: str, ):
        """
        文本审核
        :param text_id:
        :param secret_id:
        :param user_id:
        :param text:
        :return:
        """
        if not text_id:
            raise Exception(msg='video_id 值不允许为空')
        if not secret_id:
            raise Exception(msg='secret_id 值不允许为空')
        if not text:
            raise Exception(msg='text 不允许为空')
        if not user_id:
            raise Exception(msg='user_id 值不允许为空')
        text_id = str(text_id)
        playload = {"dataId": text_id, "secretId": secret_id, "text": text,
                    "userId": user_id}
        playload_querystr = utils.deal_playload(playload)
        token = self.token_get.get_token()
        query_params = utils.get_query_params(playload_querystr, token, self.client_id)
        result = requests.post(f"{SERVICE_URL}/tenant/message", json=playload, params=query_params,
                               timeout=3)
        res = result.json()
        return utils.check_api_result(res)
