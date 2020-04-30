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
from typing import List
from review_saas.const import SERVICE_URL

import json


class ImgReview:
    def __init__(self, client_id: str, token: str):
        self.client_id = client_id
        self.token = token
        self.token_get = Token(client_id, token)

    def review(self, video_id: int, secret_id: str, user_id: str, img_list: List, video_url: str = '', ):
        """
        图片审核
        :param video_id:
        :param video_url:
        :param secret_id:
        :param user_id:
        :param img_list:
        :return:
        """
        if not video_id:
            raise Exception(msg='video_id 值不允许为空')
        if not secret_id:
            raise Exception(msg='secret_id 值不允许为空')
        if not img_list:
            raise Exception(msg='img_list 不允许为空')
        if not user_id:
            raise Exception(msg='user_id 值不允许为空')
        video_id = str(video_id)
        playload = {"dataId": video_id, "secretId": secret_id, "imgs": img_list,
                    "userId": user_id}
        if video_url:
            playload["videoUrl"] = video_url
        playload_querystr = utils.deal_playload(playload)
        token = self.token_get.get_token()
        query_params = utils.get_query_params(playload_querystr, token, self.client_id)
        result = requests.post(f"{SERVICE_URL}/tenant/message", json=playload, params=query_params,
                               timeout=3)
        res = result.json()
        return utils.check_api_result(res)


if __name__ == '__main__':
    ss = ImgReview('Ep4I64pF', '1b764f3b-50a5-514f-8d39-b033a90792b0')
    img_list = ["http://qa-img.vd4v.com/20200415/4/730154803201519631332.jpg",
                "https://vid-video-in-qa.s3.ap-south-1.amazonaws.com/video-compose/20200415/1586952922698-1586952923698562538-1586952923767710753.jpg",
                "https://vid-video-in-qa.s3.ap-south-1.amazonaws.com/video-compose/20200415/1586952922698-1586952923698562538-1586952923767710754.jpg",
                "https://vid-video-in-qa.s3.ap-south-1.amazonaws.com/video-compose/20200415/1586952922698-1586952923698562538-1586952923767710755.jpg",
                "https://vid-video-in-qa.s3.ap-south-1.amazonaws.com/video-compose/20200415/1586952922698-1586952923698562538-1586952923767710756.jpg",
                "https://vid-video-in-qa.s3.ap-south-1.amazonaws.com/video-compose/20200415/1586952922698-1586952923698562538-1586952923767710757.jpg",
                "https://vid-video-in-qa.s3.ap-south-1.amazonaws.com/video-compose/20200415/1586952922698-1586952923698562538-1586952923767710758.jpg",
                "https://vid-video-in-qa.s3.ap-south-1.amazonaws.com/video-compose/20200415/1586952922698-1586952923698562538-1586952923767710759.jpg",
                "https://vid-video-in-qa.s3.ap-south-1.amazonaws.com/video-compose/20200415/1586952922698-1586952923698562538-1586952923767710760.jpg",
                "https://vid-video-in-qa.s3.ap-south-1.amazonaws.com/video-compose/20200415/1586952922698-1586952923698562538-1586952923767710761.jpg",
                "https://vid-video-in-qa.s3.ap-south-1.amazonaws.com/video-compose/20200415/1586952922698-1586952923698562538-1586952923767710762.jpg"]
    ss.review(730154803, '565b36ce-7f15-11ea-9e87-0221860e9b7e', '28224847', img_list,
              'https://vid-video-in-qa.s3.ap-south-1.amazonaws.com/20200415/3/730154803201519633579.mp4')
