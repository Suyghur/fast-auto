# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-26.
# Copyright (c) 2020 3KWan.
# Description :
import json
import ssl
import time

import requests
from upyun import upyun

from fcore.base.util.flog import Flog
from fcore.entity.result import ResultInfo
from fcore.base.util.cipher import cipher

ssl._create_default_https_context = ssl._create_unverified_context

# upyun_manager = upyun.UpYun(Host.UPYUN_SERVICE, username=Host.UPYUN_USERNAME, password=Host.UPYUN_PASSWORD)


upyun_manager = upyun.UpYun("yxupload", "sdk3k", "sdk3k123", chunksize=8192)


class NetWorkManager:
    @staticmethod
    def post(url: str, raw: str, upload: bool = False, file_link: str = "") -> ResultInfo:
        """
        加密流程：
        1）当前时间戳+10位长度Digits(0-9)随机数进行32位小写的md5加密得到原始秘钥raw_key
        2）把原始秘钥raw_key正序和倒序拼接成64位长度字符串进行16位小写的md5加密得到AES秘钥aes_key
        3）使用AES秘钥aes_key对数据进行AES/CBC/PKCS5Padding加密得到数据密文p
        """
        Flog.i("请求参数 : " + raw)
        time_stamp = str(int(time.time()))
        raw_key = cipher.get_32low_md5(time_stamp + cipher.get_random_str())
        aes_key = cipher.get_16low_md5(raw_key + raw_key[::-1])
        # p = cipher.urlencode(cipher.AesCipher.encrypt(raw, aes_key))
        p = cipher.urlencode(cipher.AesCipher.encrypt(raw, aes_key))
        ts = raw_key
        enc_url = url + "&p=" + p + "&ts=" + ts
        Flog.i("logTag " + time_stamp + " : url = " + enc_url)
        try:
            if upload:
                Flog.i("post upload")
                with open(file_link, encoding="utf-8") as f:
                    result = requests.post(enc_url, files={"log_file": f})
            else:
                result = requests.post(enc_url, headers={"Connection": "close"}, verify=False, timeout=5)
            Flog.i("返回内容 : " + result.text)
            return ResultInfo(result.text)
        except Exception as e:
            info = {
                "status": -1,
                "msg": str(e),
                "result": {}
            }
            Flog.i("请求异常 : " + str(e))
            return ResultInfo(json.dumps(info))

    @staticmethod
    def send_msg_2_wx(url: str, data: dict) -> str:
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        try:
            result = requests.post(url, json.dumps(data), headers=headers)
            Flog.i(result.text)
            return result.text
        except Exception as e:
            Flog.i("请求异常 : " + str(e))
            return str(e)
