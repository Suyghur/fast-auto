# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-28.
# Copyright (c) 2020 3KWan.
# Description :local router
import json


class FPath:
    ROOT_PATH = ""
    LOG_PATH = ""
    ASSETS_PATH = ""
    WORKSPACE_PATH = ""

    COMMON_SDK_PATH = ""
    CHANNEL_SDK_PATH = ""
    ORIGIN_APK_PATH = ""

    COMPILE_PATH = ""
    DECOMPILE_PATH = ""
    APKTOOL231 = ""
    APKTOOL232 = ""
    DX_JAR = ""
    BAKSMALI_JAR = ""

    ORIGIN_APK = ""
    OUTPUT_APK = ""

    COMMON_SCRIPT_PATH = ""
    GAME_SCRIPT_PATH = ""

    RESOURCE_PATH = ""

    @staticmethod
    def init(config_path: str) -> None:
        with open(config_path, "r", encoding="utf-8")as f:
            config = json.load(f)
            router_json = config["router"]
            FPath.ROOT_PATH = router_json["root_path"]
            FPath.LOG_PATH = router_json["log_path"]
            FPath.ASSETS_PATH = FPath.ROOT_PATH + router_json["assets_path"]
            FPath.WORKSPACE_PATH = FPath.ROOT_PATH + router_json["workspace_path"]

            FPath.COMMON_SDK_PATH = FPath.ASSETS_PATH + "/common"
            FPath.CHANNEL_SDK_PATH = FPath.ASSETS_PATH + "/channel"
            FPath.PLUGIN_SDK_PATH = FPath.ASSETS_PATH + "/plugin"
            FPath.ORIGIN_APK_PATH = FPath.ASSETS_PATH + "/origin"

            FPath.ORIGIN_APK = FPath.WORKSPACE_PATH + "/origin.apk"
            FPath.OUTPUT_APK = FPath.WORKSPACE_PATH + "/output.apk"
            FPath.COMMON_SCRIPT_PATH = FPath.WORKSPACE_PATH + "/script/common"
            FPath.GAME_SCRIPT_PATH = FPath.WORKSPACE_PATH + "/script/game"
            FPath.RESOURCE_PATH = FPath.WORKSPACE_PATH + "/resource"

            FPath.COMPILE_PATH = FPath.WORKSPACE_PATH + "/decompile"
            FPath.DECOMPILE_PATH = FPath.WORKSPACE_PATH + "/decompile"

            FPath.APKTOOL231 = FPath.ASSETS_PATH + "/apktool/apktool231.jar"
            FPath.APKTOOL232 = FPath.ASSETS_PATH + "/apktool/apktool232.jar"
            FPath.DX_JAR = FPath.ASSETS_PATH + "/apktool/dx.jar"
            FPath.BAKSMALI_JAR = FPath.ASSETS_PATH + "/apktool/baksmali.jar"
