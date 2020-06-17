# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-03-10.
# Copyright (c) 2020 3KWan.
# Description :
import os
import sys

from fcore.base.util.flog import Flog
from fcore.entity.result import Task
from fcore.base.util.path import FPath


def common(task: Task, ext: dict) -> bool:
    common_script = FPath.COMMON_SCRIPT_PATH + "/common_script.py"
    if os.path.exists(common_script):
        Flog.i("common script : " + common_script)

        sys.path.append(FPath.COMMON_SCRIPT_PATH)
        try:
            import common_script
            ret = common_script.invoke(task, FPath.DECOMPILE_PATH, task.params_info.game_params.game_package_name, ext)
            del sys.modules["common_script"]
            sys.path.remove(FPath.COMMON_SCRIPT_PATH)
            return ret
        except Exception as e:
            Flog.i(str(e))
            del sys.modules["common_script"]
            sys.path.remove(FPath.COMMON_SCRIPT_PATH)
            return False
    else:
        Flog.i("没有可执行的融合脚本")
        return True


def channel(task: Task, ext: dict) -> bool:
    sdk_script = FPath.WORKSPACE_PATH + "/channel/sdk_script.py"
    if os.path.exists(sdk_script):
        Flog.i("sdk script : " + sdk_script)
        sys.path.append(FPath.WORKSPACE_PATH + "/channel")
        try:
            import sdk_script
            ret = sdk_script.invoke(task, FPath.DECOMPILE_PATH, task.params_info.game_params.game_package_name, ext)
            del sys.modules["sdk_script"]
            sys.path.remove(FPath.WORKSPACE_PATH + "/channel")
            return ret
        except Exception as e:
            Flog.i(str(e))
            del sys.modules["sdk_script"]
            sys.path.remove(FPath.WORKSPACE_PATH + "/channel")
            return False
    else:
        Flog.i("没有可执行的渠道脚本")
        return True


def plugin(task: Task, plugin_name: str, ext: dict) -> bool:
    plugin_script = FPath.WORKSPACE_PATH + "/plugin/" + plugin_name + "/plugin_script.py"
    if os.path.exists(plugin_script):
        Flog.i("plugin script : " + plugin_script)

        sys.path.append(FPath.WORKSPACE_PATH + "/plugin/" + plugin_name)
        try:
            import plugin_script
            ret = plugin_script.invoke(task, FPath.DECOMPILE_PATH, task.params_info.game_params.game_package_name, ext)
            del sys.modules["plugin_script"]
            sys.path.remove(FPath.WORKSPACE_PATH + "/plugin/" + plugin_name)
            return ret
        except Exception as e:
            Flog.i(str(e))
            del sys.modules["plugin_script"]
            sys.path.remove(FPath.WORKSPACE_PATH + "/plugin/" + plugin_name)
            return False
    else:
        Flog.i("没有可执行的插件脚本")
        return True


def game(task: Task, ext: dict) -> bool:
    game_script = FPath.GAME_SCRIPT_PATH + "/game_script.py"
    if os.path.exists(game_script):
        Flog.i("game script : " + game_script)

        sys.path.append(FPath.GAME_SCRIPT_PATH)
        try:
            import game_script
            ret = game_script.invoke(task, FPath.DECOMPILE_PATH, task.params_info.game_params.game_package_name, ext)
            del sys.modules["game_script"]
            sys.path.remove(FPath.GAME_SCRIPT_PATH)
            return ret
        except Exception as e:
            Flog.i(str(e))
            del sys.modules["game_script"]
            sys.path.remove(FPath.GAME_SCRIPT_PATH)
            return False
    else:
        Flog.i("没有可执行的游戏脚本")
        return True
