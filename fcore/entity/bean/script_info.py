# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-27.
# Copyright (c) 2020 3KWan.
# Description :
from typing import Optional


class ScriptInfo:

    def __init__(self, info: dict):
        if "common_script" in info:
            self.__common_script = info["common_script"]
        else:
            self.__common_script = {}
        if "game_script" in info:
            self.__game_script = info["game_script"]
        else:
            self.__game_script = {}

    class __Script:
        def __init__(self, info: dict):
            self.__file_name = info["file_name"]
            self.__file_url = info["file_url"]
            self.__file_md5 = info["file_md5"]

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
    def common_script(self) -> Optional[__Script]:
        if self.__common_script:
            return self.__Script(self.__common_script)
        else:
            return None

    @property
    def game_script(self) -> Optional[__Script]:
        if self.__game_script:
            return self.__Script(self.__game_script)
        else:
            return None
