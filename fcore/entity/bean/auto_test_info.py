# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-06-16.
# Copyright (c) 2020 3KWan.
# Description :


class AutoTestInfo:
    def __init__(self, info: dict):
        self.__bag_url = info["bag_url"]
        self.__wx_notify = info["wx_notify"]
        self.__type = info["type"]

    class __WxNotify:
        def __init__(self, info: dict):
            self.__enable = info["enable"]
            self.__content = info["content"]
            self.__url = info["url"]

        @property
        def enable(self) -> int:
            return self.__enable

        @property
        def content(self) -> str:
            return self.__content

        @property
        def url(self) -> str:
            return self.__url

    @property
    def bag_url(self) -> dict:
        return self.__bag_url

    @property
    def wx_notify(self) -> __WxNotify:
        return self.__WxNotify(self.__wx_notify)

    @property
    def type(self) -> int:
        return self.__type
