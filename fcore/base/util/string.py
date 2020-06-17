# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-27.
# Copyright (c) 2020 3KWan.
# Description :


def dict_2_str(data: dict) -> str:
    return repr(data).replace("'", '"')


def is_empty(content: str) -> bool:
    if content is None or content.strip() == "":
        return True
    else:
        return False


def get_wx_notify_msg_theme(status: bool) -> str:
    if status:
        return "任务ID <font color=\"info\">{0}</font> 状态通知，请相关同事注意\n" \
               "> 状态：<font color=\"info\">成功</font>\n" \
               "> 游戏组：<font color=\"comment\">{1}</font>\n" \
               "> 渠道：<font color=\"comment\">{2}</font>\n" \
               "> 融合SDK版本：<font color=\"comment\">{3}</font>\n" \
               "> [点击下载随机抽查子包]({4})"
    else:
        return "任务ID <font color=\"warning\">{0}</font> 状态通知，请相关同事注意\n" \
               "> 状态：<font color=\"warning\">失败</font>\n" \
               "> 游戏组：<font color=\"comment\">{1}</font>\n" \
               "> 渠道：<font color=\"comment\">{2}</font>\n" \
               "> 融合SDK版本：<font color=\"comment\">{3}</font>\n"
