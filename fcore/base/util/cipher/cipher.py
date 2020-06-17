# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-25.
# Copyright (c) 2020 3KWan.
# Description :


import base64
import hashlib
import random
import string
import urllib.parse

# from Crypto.Cipher import AES

# block size
from Crypto.Cipher import AES

BS = 16


# padding算法
def pad(content: str) -> bytes:
    # 解决填充内容带有中文字符，填充前先进行urlencode
    content = urlencode(content)
    return bytes(content + (BS - len(content) % BS) * chr(BS - len(content) % BS), encoding="utf-8")


def unpad(content: bytes) -> str:
    return str(content[0:-ord(content[-1:])], encoding="utf-8")


def get_random_str() -> str:
    return "".join(random.sample(string.digits, 10))


def get_32low_md5(raw: str) -> str:
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def get_16low_md5(raw: str) -> str:
    return hashlib.md5(raw.encode("utf-8")).hexdigest()[8:-8]


def urldecode(content: str) -> str:
    return urllib.parse.unquote(content, encoding="utf-8")


def urlencode(content: str) -> str:
    return urllib.parse.quote(content, encoding="utf-8")


class AesCipher:
    """AES/CBC/PKCS5Padding"""

    @staticmethod
    def encrypt(raw: str, key: str, mode: int = AES.MODE_CBC) -> str:
        """
        加密方法
        @param key: aes秘钥
        @param raw: 明文
        @param mode: 加密模式,默认CBC
        @return: 密文
        """
        iv = key[::-1]
        cipher = AES.new(key.encode("utf-8"), mode, iv.encode("utf-8"))
        # AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题，使用base64编码
        enc = cipher.encrypt(pad(raw))
        return str(base64.b64encode(enc), encoding="utf-8")

    @staticmethod
    def decrypt(enc: str, key: str, mode: int = AES.MODE_CBC) -> str:
        """
        解密方法
        @param enc: 密文
        @param key: 秘钥
        @param mode: 加密模式,默认CBC
        @return: 明文
        """
        iv = key[::-1]
        print(enc)
        decode = base64.b64decode(bytes(enc, encoding="utf-8"))
        cipher = AES.new(key.encode("utf-8"), mode, iv.encode("utf-8"))
        raw = cipher.decrypt(decode)
        return unpad(raw)
