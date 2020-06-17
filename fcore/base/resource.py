# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-03-04.
# Copyright (c) 2020 3KWan.
# Description :

import os
import shutil
from typing import Tuple, Any

from fcore.base import dao, switch
from fcore.base.util import fio
from fcore.base.util.flog import Flog
from fcore.base.util.net.download import Download
from fcore.entity.result import Task
from fcore.base.util.path import FPath
from fcore.base.util.string import is_empty

try:
    import xml.etree.cElementTree as elementTree
except ImportError:
    import xml.etree.ElementTree as elementTree


# ------ 检查sdk资源 ------
def check_sdk_resource(task: Task) -> Tuple[bool, Any]:
    result, plugin_sdk_size = __check_plugin_sdk(task)
    if __check_common_sdk(task) and __check_channel_sdk(task) and result:
        return True, plugin_sdk_size
    else:
        return False, plugin_sdk_size


def __check_common_sdk(task: Task) -> Tuple[bool, int]:
    # 查表取出本地的md5
    # md5为空直接下载，非空时进行对比，不一致时以服务端返回为较新版本
    sdk_info = task.sdk_info
    md5 = dao.get_common_sdk_md5(sdk_info.common_sdk.version)
    file_size = 0
    result = False, file_size

    if not os.path.exists(FPath.COMMON_SDK_PATH):
        os.makedirs(FPath.COMMON_SDK_PATH)

    if not switch.DB_ENABLE and os.path.exists(FPath.COMMON_SDK_PATH + "/" + sdk_info.common_sdk.version):
        shutil.rmtree(FPath.COMMON_SDK_PATH + "/" + sdk_info.common_sdk.version)

    if is_empty(md5):
        file_name = Download.download_file(sdk_info.common_sdk.file_url, FPath.COMMON_SDK_PATH)
        file_size = os.path.getsize(FPath.COMMON_SDK_PATH + "/" + file_name)
        # 解压
        if fio.unzip(FPath.COMMON_SDK_PATH + "/" + file_name, FPath.COMMON_SDK_PATH):
            os.remove(FPath.COMMON_SDK_PATH + "/" + file_name)
            result = True, file_size
        else:
            return False, 0
        # 更新db
        if dao.insert_common_sdk_md5(sdk_info.common_sdk.version, sdk_info.common_sdk.file_md5, file_size):
            result = True, file_size
        else:
            return False, 0
    else:
        if sdk_info.common_sdk.file_md5 != md5 or not os.path.exists(
                FPath.COMMON_SDK_PATH + "/" + sdk_info.common_sdk.version):
            # 删除原来的文件夹
            Flog.i(FPath.COMMON_SDK_PATH + "/" + sdk_info.common_sdk.version)
            if os.path.exists(FPath.COMMON_SDK_PATH + "/" + sdk_info.common_sdk.version):
                shutil.rmtree(FPath.COMMON_SDK_PATH + "/" + sdk_info.common_sdk.version)
            # 下载
            # file_name = os.path.basename(sdk_info.common_sdk.file_url)
            file_name = Download.download_file(sdk_info.common_sdk.file_url, FPath.COMMON_SDK_PATH)
            file_size = os.path.getsize(FPath.COMMON_SDK_PATH + "/" + file_name)
            # 解压
            if fio.unzip(FPath.COMMON_SDK_PATH + "/" + file_name, FPath.COMMON_SDK_PATH):
                os.remove(FPath.COMMON_SDK_PATH + "/" + file_name)
                result = True, file_size
            else:
                return False, 0
            # 更新db
            if dao.update_common_sdk_md5(sdk_info.common_sdk.version, sdk_info.common_sdk.file_md5, file_size):
                result = True, file_size
            else:
                return False, 0
        else:
            result = True, file_size
    return result


def __check_channel_sdk(task: Task) -> bool:
    # 查表取出本地的md5
    # md5为空直接下载，非空时进行对比，不一致时以服务端返回为较新版本
    channel_name = task.params_info.common_params.channel_name
    sdk_info = task.sdk_info
    md5 = dao.get_channel_sdk_md5(channel_name, sdk_info.channel_sdk.version)
    result = False

    if not os.path.exists(FPath.CHANNEL_SDK_PATH):
        os.makedirs(FPath.CHANNEL_SDK_PATH)

    if not switch.DB_ENABLE and os.path.exists(FPath.CHANNEL_SDK_PATH + "/" + channel_name):
        shutil.rmtree(FPath.CHANNEL_SDK_PATH + "/" + channel_name)

    if is_empty(md5):
        file_name = Download.download_file(sdk_info.channel_sdk.file_url, FPath.CHANNEL_SDK_PATH)
        file_size = os.path.getsize(FPath.CHANNEL_SDK_PATH + "/" + file_name)
        # 解压
        if fio.unzip(FPath.CHANNEL_SDK_PATH + "/" + file_name, FPath.CHANNEL_SDK_PATH):
            os.remove(FPath.CHANNEL_SDK_PATH + "/" + file_name)
            result = True
        # 更新db
        if dao.insert_channel_sdk_md5(channel_name, sdk_info.channel_sdk.version, sdk_info.channel_sdk.file_md5,
                                      file_size):
            result = True
    else:
        if sdk_info.channel_sdk.file_md5 != md5 or not os.path.exists(FPath.CHANNEL_SDK_PATH + "/" + channel_name):
            # 删除原来的文件夹
            if os.path.exists(FPath.CHANNEL_SDK_PATH + "/" + channel_name):
                shutil.rmtree(FPath.CHANNEL_SDK_PATH + "/" + channel_name)
            # 下载
            # file_name = os.path.basename(sdk_info.channel_sdk.file_url)
            file_name = Download.download_file(sdk_info.channel_sdk.file_url, FPath.CHANNEL_SDK_PATH)
            file_size = os.path.getsize(FPath.CHANNEL_SDK_PATH + "/" + file_name)
            # 解压
            if fio.unzip(FPath.CHANNEL_SDK_PATH + "/" + file_name, FPath.CHANNEL_SDK_PATH):
                os.remove(FPath.CHANNEL_SDK_PATH + "/" + file_name)
                result = True
            # 更新db
            if dao.update_channel_sdk_md5(channel_name, sdk_info.channel_sdk.version, sdk_info.channel_sdk.file_md5,
                                          file_size):
                result = True
        else:
            result = True
    return result


def __check_plugin_sdk(task: Task) -> Tuple[bool, int]:
    if task.task_info.has_plugin_sdk != 1 or not task.sdk_info.plugin_sdk:
        return True, 0
    else:
        result = False
        plugin_dict = task.sdk_info.plugin_sdk
        total_file_size = 0
        for plugin_name in plugin_dict:
            file_name = Download.download_file(plugin_dict[plugin_name].file_url, FPath.WORKSPACE_PATH + "/plugin")
            file_size = os.path.getsize(FPath.WORKSPACE_PATH + "/plugin/" + file_name)
            total_file_size += file_size
            if fio.unzip(FPath.WORKSPACE_PATH + "/plugin/" + file_name,
                         FPath.WORKSPACE_PATH + "/plugin/" + plugin_name):
                os.remove(FPath.WORKSPACE_PATH + "/plugin/" + file_name)
                result = True
        return result, total_file_size


# ------ 检查sdk资源 ------


# ------ 检查母包资源 ------
def check_origin_bag(task: Task) -> bool:
    Flog.i("检查母包资源")
    bag_info = task.bag_info
    md5 = dao.get_origin_bag_md5(bag_info.game_id, bag_info.group_id)
    result = False
    if not os.path.exists(FPath.ORIGIN_APK_PATH):
        os.makedirs(FPath.ORIGIN_APK_PATH)
    if is_empty(md5):
        file_name = Download.download_file(bag_info.file_url, FPath.ORIGIN_APK_PATH + "/" + bag_info.group_id)
        if dao.insert_origin_bag_md5(bag_info.game_id, bag_info.group_id, bag_info.file_md5):
            os.rename(FPath.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + file_name,
                      FPath.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + bag_info.game_id + ".apk")
            result = True
    else:
        if bag_info.file_md5 != md5 or not os.path.exists(
                FPath.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + bag_info.game_id + ".apk"):
            if os.path.exists(FPath.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + bag_info.game_id + ".apk"):
                os.remove(FPath.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + bag_info.game_id + ".apk")
            file_name = Download.download_file(bag_info.file_url, FPath.ORIGIN_APK_PATH + "/" + bag_info.group_id)
            if dao.update_origin_bag_md5(bag_info.game_id, bag_info.group_id, bag_info.file_md5):
                os.rename(FPath.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + file_name,
                          FPath.ORIGIN_APK_PATH + "/" + bag_info.group_id + "/" + bag_info.game_id + ".apk")
                result = True
        else:
            result = True
    return result


# ------ 检查母包资源 ------


# ------ 检查签名文件资源 ------
def check_keystore(task: Task) -> bool:
    Flog.i("检查签名文件资源")
    try:
        keystore_info = task.keystore_info
        file_name = Download.download_file(keystore_info.file_url, FPath.WORKSPACE_PATH)
        if file_name != keystore_info.keystore_name:
            os.rename(FPath.WORKSPACE_PATH + "/" + file_name,
                      FPath.WORKSPACE_PATH + "/" + keystore_info.keystore_name)
        return True
    except Exception as e:
        Flog.i(str(e))
    return False


# ------ 检查签名文件资源 ------

# ------ 检查脚本资源 ------
def check_common_script(task: Task) -> bool:
    Flog.i("检查融合脚本资源")
    try:
        common_script_info = task.script_info.common_script
        if common_script_info is None:
            return True
        file_name = Download.download_file(common_script_info.file_url, FPath.COMMON_SCRIPT_PATH)
        if file_name == common_script_info.file_name:
            if fio.unzip(FPath.COMMON_SCRIPT_PATH + "/" + file_name, FPath.COMMON_SCRIPT_PATH):
                os.remove(FPath.COMMON_SCRIPT_PATH + "/" + file_name)
                return True

    except Exception as e:
        Flog.i(str(e))
    return False


def check_game_script(task: Task) -> bool:
    Flog.i("检查游戏脚本资源")
    try:
        game_script_info = task.script_info.game_script
        if game_script_info is None:
            return True
        file_name = Download.download_file(game_script_info.file_url, FPath.GAME_SCRIPT_PATH)
        if file_name == game_script_info.file_name:
            if fio.unzip(FPath.GAME_SCRIPT_PATH + "/" + file_name, FPath.GAME_SCRIPT_PATH):
                os.remove(FPath.GAME_SCRIPT_PATH + "/" + file_name)
                return True

    except Exception as e:
        Flog.i(str(e))
    return False


# ------ 检查游戏资源 ------
def check_game_resource(task: Task) -> bool:
    Flog.i("检查游戏资源")
    try:
        icon_url = task.params_info.game_params.game_icon_url
        logo_url = task.params_info.game_params.game_logo_url
        splash_url = task.params_info.game_params.game_splash_url
        background_url = task.params_info.game_params.game_background_url
        loading_url = task.params_info.game_params.game_loading_url
        resource_url = task.params_info.game_params.game_resource_url

        if not is_empty(icon_url):
            icon = Download.download_file(icon_url, FPath.RESOURCE_PATH, 1)
        if not is_empty(logo_url):
            logo = Download.download_file(logo_url, FPath.RESOURCE_PATH, 2)
        if not is_empty(splash_url):
            splash = Download.download_file(splash_url, FPath.RESOURCE_PATH, 3)
        if not is_empty(background_url):
            background = Download.download_file(background_url, FPath.RESOURCE_PATH, 4)
        if not is_empty(background_url):
            loading = Download.download_file(loading_url, FPath.RESOURCE_PATH, 5)
        if not is_empty(resource_url):
            resource = Download.download_file(resource_url, FPath.RESOURCE_PATH)
            if fio.unzip(FPath.RESOURCE_PATH + "/" + resource, FPath.RESOURCE_PATH):
                os.remove(FPath.RESOURCE_PATH + "/" + resource)

        return True

    except Exception as e:
        Flog.i(str(e))
        return False

# ------ 检查游戏资源 ------
