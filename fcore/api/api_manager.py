# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-27.
# Copyright (c) 2020 3KWan.
# Description :
from typing import Optional, Any, Tuple

from fcore import CLIENT_VERSION, SERVER_VERSION
from fcore.base import switch
from fcore.entity.bean.auto_test_info import AutoTestInfo
from fcore.entity.result import Task, ResultInfo
from fcore.base.util.net.frequest import NetWorkManager
from fcore.base.util.net.host import Host
from fcore.base.util.string import dict_2_str

COMMON = {
    "class_type": 1,
    "server_version": SERVER_VERSION,
    "client_version": CLIENT_VERSION
}

URL = ""


def api_get_task(data: dict) -> Optional[Task]:
    """
    :param data:
    :return
    """
    data["common"] = COMMON
    result = NetWorkManager.post(Host.BASIC_URL_GET_TASK, dict_2_str(data))
    if result.status == 0 and result.result:
        raw_result = ResultInfo.handle_result(result.result)
        if raw_result:
            return Task(raw_result)
        else:
            return None

    else:
        if result.status != 0:
            msg = "{0}-{1}（获取任务接口请求异常：{2}）".format(Host.HOST_NAME, Host.ENV, result.msg)
            api_notify_wx_dev_group(msg)
        return None


def api_report_status(data: dict, upload: bool = False, file_link: str = "") -> Tuple[bool, Any]:
    data["common"] = COMMON
    if upload:
        result_info = NetWorkManager.post(Host.BASIC_URL_REPORT_STATUS, dict_2_str(data), upload, file_link)
    else:
        result_info = NetWorkManager.post(Host.BASIC_URL_REPORT_STATUS, dict_2_str(data))
    result = ResultInfo.handle_result(result_info.result)
    if result_info.status == 0 and result and "is_stop" in result:
        # 请求成功
        if result["is_stop"] == 1:
            return True, None  # 任务中断
        else:
            return False, None  # 任务继续
    else:
        # 请求失败，返回任务中断
        return True, "上报打包状态接口请求异常：" + result_info.msg


def api_report_task(data: dict) -> Tuple[bool, Any]:
    data["common"] = COMMON
    result_info = NetWorkManager.post(Host.BASIC_URL_REPORT_TASK, dict_2_str(data))
    if result_info.status == 0:
        return True, None
    elif result_info.status == -1:
        return False, "上报任务状态接口请求异常：" + result_info.msg
    else:
        return False, "上报任务状态接口失败，msg=" + result_info.msg


def api_polling_status():
    pass


def api_notify_wx_dev_group(msg: str) -> str:
    if switch.WX_DEV_ENABLE:
        data = {
            "msgtype": "text",
            "text": {
                "content": msg,
            }
        }
        return NetWorkManager.send_msg_2_wx(Host.BASIC_URL_WX_DEVELOPER, data)
    else:
        return ""


def api_notify_wx_test_group(msg: str) -> str:
    if switch.WX_TEST_ENABLE:
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": msg,
            }
        }
        return NetWorkManager.send_msg_2_wx(Host.BASIC_URL_WX_TESTER, data)
    else:
        return ""


def api_send_2_auto_test(task: Task, random_package_id: str, random_link: str, auto_test: AutoTestInfo):
    data = {
        "common": COMMON,
        "task_entry": task.task_info_str,
        "auto_test": {
            "bag_url": {random_package_id: random_link},
            "wx_notify": {
                "enable": auto_test.wx_notify.enable,
                "content": auto_test.wx_notify.content,
                "url": auto_test.wx_notify.url
            },
            "type": auto_test.type
        }

    }
    NetWorkManager.post(Host.BASIC_URL_SEND_2_AUTO_TEST, dict_2_str(data))
