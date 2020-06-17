# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-28.
# Copyright (c) 2020 3KWan.
# Description :
import json
import socket


class Host:
    HOST_URL = ""
    BASIC_URL_GET_TASK = ""
    BASIC_URL_REPORT_STATUS = ""
    BASIC_URL_REPORT_TASK = ""
    BASIC_URL_WX_DEVELOPER = ""
    BASIC_URL_WX_TESTER = ""
    BASIC_URL_SEND_2_AUTO_TEST = ""
    OSS_SERVICE_NAME = ""
    UPYUN_SERVICE = ""
    UPYUN_USERNAME = ""
    UPYUN_PASSWORD = ""

    ENV = ""
    HOST_NAME = ""

    @staticmethod
    def init(config_path) -> None:
        with open(config_path, "r", encoding="utf-8")as f:
            setting_json = json.load(f)
            host_json = setting_json["host"]
            mode = host_json["mode"]
        if mode == 2:
            Host.HOST_URL = host_json["dev"]
            Host.ENV = "开发"
        elif mode == 1:
            Host.HOST_URL = host_json["test"]
            Host.ENV = "测试"
        else:
            Host.HOST_URL = host_json["online"]
            Host.ENV = "正式"

        Host.HOST_NAME = socket.gethostname()
        Host.BASIC_URL_GET_TASK = Host.HOST_URL + "/?ct=AutoPackage&ac=getTaskInfo"
        Host.BASIC_URL_REPORT_STATUS = Host.HOST_URL + "/?ct=AutoPackage&ac=getStatusReport"
        Host.BASIC_URL_REPORT_TASK = Host.HOST_URL + "/?ct=AutoPackage&ac=getTaskReport"
        # Host.BASIC_URL_SEND_2_AUTO_TEST=Host.HOST_URL+"/"
        Host.BASIC_URL_SEND_2_AUTO_TEST = "http://192.168.49.98:9999/tasks/api/v1/auto/task?"
        Host.BASIC_URL_WX_DEVELOPER = host_json["wx_developer"]
        Host.BASIC_URL_WX_TESTER = host_json["wx_tester"]
        Host.OSS_SERVICE_NAME = host_json["oss_service_name"]
        Host.UPYUN_SERVICE = host_json["upyun_service"]
        Host.UPYUN_USERNAME = host_json["upyun_username"]
        Host.UPYUN_PASSWORD = host_json["upyun_password"]
