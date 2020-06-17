# -*- coding: utf-8 -*-
# Author:yangtianbiao
# CreateTime:2019/5/7
#
# 此文件用于编写打包脚本的主要逻辑
import os
import shutil

from fcore.base import apk_utils, handle_xml
from fcore.base.handle_v2 import handle_v2_origin, handle_v2_common_params
from fcore.base.handle_v3 import handle_v3_origin, handle_v3_common_params
from fcore.base.util import fio
from fcore.base.util.flog import Flog
from fcore.base.util.path import FPath
from fcore.entity.result import Task


def pack(task: Task) -> bool:
    # TODO 检查母包接入是否正确
    try:
        # change xml config and so on
        new_package_name = task.params_info.game_params.game_package_name

        # copy channel sdk resources.
        ret = apk_utils.copyResource(task, FPath.WORKSPACE_PATH + "/channel")
        if ret:
            Flog.i("整合渠道SDK资源失败")
            return False
        else:
            Flog.i("整合渠道SDK资源成功")

        # copy common sdk resources.
        ret = apk_utils.copyResource(task, FPath.WORKSPACE_PATH + "/common")
        if ret:
            Flog.i("整合融合SDK资源失败")
            return False

        handle_xml.do_common_provider(new_package_name)
        Flog.i("整合3k融合SDK资源成功")

        if task.task_info.has_plugin_sdk > 0:
            for plugin_sdk in task.sdk_info.plugin_sdk:
                Flog.i("正在整合插件sdk : " + plugin_sdk + " 资源")
                ret = apk_utils.copyResource(task, FPath.WORKSPACE_PATH + "/plugin/" + plugin_sdk)
                if ret:
                    Flog.i("整合插件sdk : " + plugin_sdk + " 资源失败")
                    return False
                else:
                    Flog.i("整合插件sdk : " + plugin_sdk + " 资源成功")

        # auto handle icon
        apk_utils.append_channel_icon_mark()
        Flog.i("处理icon成功")

        # copy channel special resources common, game, channel, decompile_dir
        ret = apk_utils.copyChannelSpecialResources()
        if ret:
            Flog.i("copy channel special resources failure...")
            return False

        Flog.i("整合渠道特殊资源成功")

        # generate common and channel's bagparams to apk
        is_auto_change_orientation = apk_utils.obtain_direction(FPath.WORKSPACE_PATH + "/channel")
        if apk_utils.add_channel_params(task, is_auto_change_orientation):
            Flog.i("添加渠道参数成功")
        else:
            Flog.i("添加渠道参数失败")

        # if handle_media_params(task, Router.DECOMPILE_PATH):
        #     print("处理媒体参数成功")

        # interaction cpu supports
        apk_utils.handle_cpu_support(task)

        # modify yml
        apk_utils.modify_yml(task)
        Flog.i("修改yml")

        # modify root application extends
        apk_utils.modify_application_extends(FPath.WORKSPACE_PATH + "/channel")
        Flog.i("修改application继承关系")

        # modify game name if channel specified
        apk_utils.modify_game_name(task)

        return True
    except Exception as e:
        Flog.i(str(e))
        return False


def handle_origin() -> bool:
    """
    处理母包
    :return:
    """
    if is_v3_mode():
        Flog.i("v3版本母包")
        result = handle_v3_origin()
    else:
        Flog.i("v2版本母包")
        result = handle_v2_origin()
    return result


def handle_common_params(task: Task, channel_id: str, package_id: str) -> bool:
    if is_v3_mode():
        return handle_v3_common_params(channel_id, package_id)
    else:
        return handle_v2_common_params(task, package_id, task.params_info.common_params.package_chanle)


def is_v3_mode() -> bool:
    return os.path.exists(FPath.DECOMPILE_PATH + "/assets/fuse_cfg.properties")


def new_mode_handle_common_params(channel_id, package_id: str) -> bool:
    return handle_v3_common_params(channel_id, package_id, True)


def implant_fuse_profile() -> bool:
    bcontent = b""
    apk_file = FPath.WORKSPACE_PATH + "/new_mode_output.apk"
    if os.path.exists(FPath.OUTPUT_APK):
        shutil.copy(FPath.OUTPUT_APK, apk_file)
        with open(FPath.WORKSPACE_PATH + "/fuse_cfg.properties", "rb")as pro:
            bcontent = pro.read()
        return fio.insert_file_2_apk(apk_file, "assets/fuse_cfg.properties", bcontent)
    else:
        return False
