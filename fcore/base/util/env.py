# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-28.
# Copyright (c) 2020 3KWan.
# Description :
import sys


def is_py2():
    version = sys.version_info
    major = version.major
    return major == 2


def get_py_version():
    version = sys.version_info
    major = version.major
    minor = version.minor
    micro = version.micro

    curr_version = str(major) + "." + str(minor) + "." + str(micro)
    return curr_version


def get_sys_platform_code() -> int:
    platform = sys.platform
    if platform == "darwin":
        return 1
    elif platform == "win32":
        return 3
    else:
        return 0
