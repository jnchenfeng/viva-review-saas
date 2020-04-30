#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/7 9:23 PM
# @Author  : Neal
# @Site    : 
# @File    : video.py
# @Software: PyCharm

from review_saas import utils
from review_saas.oauth_token import Token
import requests
from review_saas.const import SERVICE_URL


class Video:
    def __init__(self, client_id: str, token: str):
        self.client_id = client_id
        self.token = token
        self.token_get = Token(client_id, token)

    def review(self, video_id: int, video_url: str, secret_id: str, duration: int, user_id: str, cover: str = ""):
        """
        视频审核
        :param video_id:
        :param video_url:
        :param secret_id:
        :param duration:
        :param user_id:
        :param cover:
        :return: bool,str
        """
        if not video_id:
            raise Exception(msg='video_id 值不允许为空')
        if not video_url:
            raise Exception(msg='video_url 值不允许为空')
        if not secret_id:
            raise Exception(msg='secret_id 值不允许为空')
        if not duration:
            raise Exception(msg='duration 值不允许为空')
        if not user_id:
            raise Exception(msg='user_id 值不允许为空')
        playload = {"dataId": video_id, "secretId": secret_id, "duration": duration, "videoUrl": video_url,
                    "userId": user_id}
        if cover:
            playload["cover"] = cover

        playload_querystr = utils.deal_playload(playload)
        token = self.token_get.get_token()
        query_params = utils.get_query_params(playload_querystr, token, self.client_id)
        result = requests.post(f"{SERVICE_URL}/tenant/message", json=playload, params=query_params,
                               timeout=3)
        res = result.json()
        return utils.check_api_result(res)
