# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-26.
# Copyright (c) 2020 3KWan.
# Description :


class BagInfo:
    def __init__(self, info: dict):
        self.__group_id = info["group_id"]
        self.__group_name = info["group_name"]
        self.__game_id = info["game_id"]
        self.__version_code = info["version_code"]
        self.__version_name = info["version_name"]
        self.__file_name = info["file_name"]
        self.__file_url = info["file_url"]
        self.__file_md5 = info["file_md5"]

    @property
    def group_id(self) -> str:
        return self.__group_id

    @property
    def group_name(self) -> str:
        return self.__group_name

    @property
    def game_id(self) -> str:
        return self.__game_id

    @property
    def version_code(self) -> str:
        return self.__version_code

    @property
    def version_name(self) -> str:
        return self.__version_name

    @property
    def file_name(self) -> str:
        return self.__file_name

    @property
    def file_url(self) -> str:
        return self.__file_url

    @property
    def file_md5(self) -> str:
        return self.__file_md5
