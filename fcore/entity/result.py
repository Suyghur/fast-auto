# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-26.
# Copyright (c) 2020 3KWan.
# Description :
import json

from fcore.base.util.flog import Flog
from fcore.entity.bean.bag_info import BagInfo
from fcore.entity.bean.keystore_info import KeystoreInfo
from fcore.entity.bean.params_info import ParamsInfo
from fcore.entity.bean.script_info import ScriptInfo
from fcore.entity.bean.sdk_info import SdkInfo
from fcore.entity.bean.task_info import TaskInfo
from fcore.base.util.cipher import cipher
from fcore.base.util.string import dict_2_str


class ResultInfo:

    def __init__(self, json_str: str):
        json_obj = json.loads(json_str)
        self.__status = json_obj["status"]
        self.__msg = json_obj["msg"]
        self.__result = json_obj["result"]

    @property
    def status(self) -> int:
        return self.__status

    @property
    def msg(self) -> str:
        return self.__msg

    @property
    def result(self) -> dict:
        return self.__result

    @staticmethod
    def handle_result(result) -> dict:
        p = ""
        ts = ""
        if result:
            if "p" in result:
                p = result["p"]
            if "ts" in result:
                ts = result["ts"]
            aes_key = cipher.get_16low_md5(ts + ts[::-1])
            raw = cipher.urldecode(cipher.AesCipher.decrypt(cipher.urldecode(p), aes_key))
            result = json.loads(raw)
            Flog.i("解析数据 : " + dict_2_str(result))
            return result


class Task:
    def __init__(self, result: dict):
        self.__task_info = result["task_info"]
        self.__bag_info = result["bag_info"]
        self.__sdk_info = result["sdk_info"]
        self.__keystore_info = result["keystore_info"]
        self.__script_info = result["script_info"]
        self.__params_info = result["params_info"]
        self.__ext = result["ext"]
        self.__task_info_str = result

    @property
    def task_info(self) -> TaskInfo:
        return TaskInfo(self.__task_info)

    @property
    def bag_info(self) -> BagInfo:
        return BagInfo(self.__bag_info)

    @property
    def keystore_info(self) -> KeystoreInfo:
        return KeystoreInfo(self.__keystore_info)

    @property
    def script_info(self) -> ScriptInfo:
        return ScriptInfo(self.__script_info)

    @property
    def sdk_info(self) -> SdkInfo:
        return SdkInfo(self.__sdk_info)

    @property
    def params_info(self) -> ParamsInfo:
        return ParamsInfo(self.__params_info)

    @property
    def ext(self) -> dict:
        return self.__ext

    @property
    def task_info_str(self) -> dict:
        return self.__task_info_str


class RequestTask:
    def __init__(self, result: dict):
        self.__common = result["common"]
        self.__task_entry = result["task_entry"]
        self.__auto_test = result["auto_task"]

    @property
    def common(self) -> dict:
        return self.__common

    @property
    def task_entry(self) -> Task:
        return Task(self.__task_entry)

    @property
    def auto_test(self):
        return self.__auto_test
