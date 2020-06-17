# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-28.
# Copyright (c) 2020 3KWan.
# Description :
import os

from fcore.base.util import env, command
from fcore.base.util.flog import Flog
from fcore.base.util.path import FPath


def jar2dex(src_dir: str, dst_dir: str) -> bool:
    dx_tool = FPath.DX_JAR
    if os.path.exists(src_dir):
        cmd = get_java_shell() + " -jar -Xms2048m -Xmx2048m %s --dex --multi-dex --output=%s" % (dx_tool, dst_dir)
        for jar_file in os.listdir(src_dir):
            if jar_file.endswith(".jar"):
                cmd = cmd + " " + os.path.join(src_dir, jar_file)
        return command.exec_command(cmd)
    else:
        return False


def dex2smali(src_dir: str, dst_dir: str) -> bool:
    baksmali_tool = FPath.BAKSMALI_JAR
    if not os.path.exists(src_dir):
        Flog.i("classes.dex is can not found , where : " + src_dir)
        return False
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    cmd = get_java_shell() + " -jar %s -o %s %s" % (baksmali_tool, dst_dir, src_dir)
    return command.exec_command(cmd)


def get_java_shell() -> str:
    if env.get_sys_platform_code() == 1 or env.get_sys_platform_code() == 3:
        return "java"
    else:
        return FPath.ASSETS_PATH + "/java_home/bin/./java"


def get_javac_shell() -> str:
    if env.get_sys_platform_code() == 1 or env.get_sys_platform_code() == 3:
        return "javac"
    else:
        return FPath.ASSETS_PATH + "/java_home/bin/./javac"


def get_jarsigner_shell() -> str:
    if env.get_sys_platform_code() == 1 or env.get_sys_platform_code() == 3:
        return "jarsigner"
    else:
        return FPath.ASSETS_PATH + "/java_home/bin/./jarsigner"


def get_aapt_shell() -> str:
    if env.get_sys_platform_code() == 1:
        return "aapt"
    elif env.get_sys_platform_code() == 3:
        return FPath.ASSETS_PATH + "/apktool/aapt.exe"
    else:
        return FPath.ASSETS_PATH + "/apktool/./aapt"