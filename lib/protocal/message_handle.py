# -*- coding:utf-8 -*-
# AUTHOR:   zhao
# EMAIL:   bruce.e.zhao@gmail.com
# FILE:     message_handle.py
# ROLE:     TODO (some explanation)
# CREATED:  2017-04-20 11:59:17
# MODIFIED: 2017-04-20 11:59:22
import json


class BIGIOT_USER_TYPE:
    BIGIOT_ALL = 0
    BIGIOT_USER = 1
    BIGIOT_DEVICE = 2
    BIGIOT_GUSET = 3


class BIGIOT_ALERT_TYPE:
    BIGIOT_EMAIL = 0
    BIGIOT_WEIBO = 1
    BIGIOT_QQ = 2


class Message_handle:
    def __init__(self):
        pass

    def decode(self, json_mes):
        self.__python_mes = json.loads(json_mes)
        return self.__python_mes

    def encode(self, python_mes):
        self.__json_mes = json.dumps(python_mes)
        return self.__json_mes
