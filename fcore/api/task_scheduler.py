# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-06-15.
# Copyright (c) 2020 3KWan.
# Description :
import json

from flask import Flask
from flask_apscheduler import APScheduler

from fcore.api.task_cache import cache
from fcore.base.util.flog import Flog
from fcore.entity.result import RequestTask
from fcore.impl_manager import ImplManager

scheduler = APScheduler()


def query_task(impl: ImplManager):
    last_task_id = ""

    if cache.get("cache_task_json") is not None and cache.get("cache_task_flag"):
        request_task = RequestTask(json.loads(cache.get("cache_json")))
        task = request_task.task_entry
        auto_test = request_task.auto_test
    else:
        Flog.init_flog_file_handler()
        Flog.i("------开始查询任务，上一任务ID=" + last_task_id + "------")
        task = ImplManager.get_task(last_task_id)
        auto_test = None
        Flog.i("------结束查询任务------")
    if task is None or task.task_info is None or task.task_info.task_id == "":
        Flog.i("------无打包任务，进入定时查询------")
        Flog.save_flog_format_elk(task)
    else:
        last_task_id = task.task_info.task_id
        Flog.i("------进入打包任务：" + last_task_id + "------")
        try:
            impl.execute(task, auto_test)
            # 如果当前完成的是自动构建提交的任务则清除缓存
            if task.task_info.is_auto_build == 1:
                cache.delete("cache_task_json")
                cache.set("cache_task_flag", False)
            else:
                cache.set("cache_task_flag", True)
        except BaseException as e:
            # 上报任务状态（失败）
            impl.report_task(task, 1204)
            # 企业微信机器人提醒
            impl.api_send_msg_2_wx("全局捕获：" + str(e))
            Flog.i(str(e))
        Flog.save_flog_format_elk(task)


def init_scheduler(app: Flask, impl: ImplManager) -> None:
    scheduler.init_app(app)
    scheduler.add_job(id='query_task', func=query_task, trigger='interval', seconds=30, args=[impl])
    scheduler.start()
