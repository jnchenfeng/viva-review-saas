#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/8 10:21 AM
# @Author  : Neal
# @Site    : 
# @File    : utils.py
# @Software: PyCharm

import time
import hashlib
from typing import Dict, List


def sha256(text: str) -> str:
    """
    获取sha256
    :param text:
    :return:
    """
    return hashlib.sha256(text.encode()).hexdigest()


def deal_playload(playload: Dict) -> str:
    """
    处理参数，对参数名进行排序以及转小写再生成 url query 字符串
    :param playload:
    :return:
    """
    sort_keys = sorted(list(playload.keys()))
    new_playload = {}
    for k, v in playload.items():
        if isinstance(v, List):
            new_playload[k] = ','.join([str(d) for d in v])
        else:
            new_playload[k] = v
    param_list = ['='.join([str(key).lower(), str(new_playload.get(key))]) for key in sort_keys]
    query_str = '&'.join(param_list)
    return query_str


def get_query_params(playload_raw: str, token: str, client_id: str) -> Dict:
    """
    获取query中的参数
    :param playload_raw:
    :param token:
    :param client_id:
    :return:
    """
    ret = {"token": token, "openid": client_id, "nonce_str": str(int(time.time()))[-4:],
           "timestamp": int(time.time()) * 1000, "playload": playload_raw}
    ret_raw = deal_playload(ret)
    ret["sign"] = hashlib.md5(ret_raw.encode()).hexdigest()
    ret['clientid'] = client_id
    del ret["openid"]
    del ret["playload"]
    return ret


def check_api_result(data: Dict):
    """
    校验api请求结果
    :param data:
    :return:
    """
    if data.get("code") == 20000:
        return True, data.get("message")
    else:
        return False, data.get("message")
