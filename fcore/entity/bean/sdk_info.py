# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-26.
# Copyright (c) 2020 3KWan.
# Description :


class SdkInfo:
    def __init__(self, info: dict):
        self.__common_sdk = info["common_sdk"]
        self.__channel_sdk = info["channel_sdk"]
        self.__plugin_sdk = {}
        if info["plugin_sdk"]:
            for plugin_sdk in info["plugin_sdk"]:
                self.__plugin_sdk[plugin_sdk] = self.__Sdk(info["plugin_sdk"][plugin_sdk])

    class __Sdk:
        def __init__(self, info: dict):
            self.__version = info["version"]
            self.__file_name = info["file_name"]
            self.__file_url = info["file_url"]
            self.__file_md5 = info["file_md5"]

        @property
        def version(self) -> str:
            return self.__version

        @property
        def file_name(self) -> str:
            return self.__file_name

        @property
        def file_url(self) -> str:
            return self.__file_url

        @property
        def file_md5(self) -> str:
            return self.__file_md5

    @property
    def common_sdk(self) -> __Sdk:
        return self.__Sdk(self.__common_sdk)

    @property
    def channel_sdk(self) -> __Sdk:
        return self.__Sdk(self.__channel_sdk)

    @property
    def plugin_sdk(self) -> dict:
        return self.__plugin_sdk
