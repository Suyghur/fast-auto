# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-26.
# Copyright (c) 2020 3KWan.
# Description :


class KeystoreInfo:
    def __init__(self, info: dict):
        self.__keystore_name = info["keystore_name"]
        self.__keystore_password = info["keystore_password"]
        self.__keystore_alias = info["keystore_alias"]
        self.__keystore_alias_password = info["keystore_alias_password"]
        self.__file_url = info["file_url"]
        self.__file_md5 = info["file_md5"]

    @property
    def keystore_name(self) -> str:
        return self.__keystore_name

    @property
    def keystore_password(self) -> str:
        return self.__keystore_password

    @property
    def keystore_alias(self) -> str:
        return self.__keystore_alias

    @property
    def keystore_alias_password(self) -> str:
        return self.__keystore_alias_password

    @property
    def file_url(self) -> str:
        return self.__file_url

    @property
    def file_md5(self) -> str:
        return self.__file_md5
