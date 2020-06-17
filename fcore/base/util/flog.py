# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-03-16.
# Copyright (c) 2020 3KWan.
# Description :
import json
import logging
import os
import time

from fcore.base import switch
from fcore.base.util.net.host import Host
from fcore.base.util.path import FPath


class Flog:
    __log = None
    __handler_console = False
    __handler_write = False

    @staticmethod
    def init():
        config_path = FPath.ROOT_PATH + "/config.json"
        if not os.path.exists(FPath.LOG_PATH):
            os.makedirs(FPath.LOG_PATH)
        with open(config_path, "r", encoding="utf-8")as f:
            config = json.load(f)
            switch.LOG_ENABLE = config["log_cfg"]["enable"]
        if switch.LOG_ENABLE:
            Flog.__log = logging.getLogger()
            Flog.__log.setLevel(logging.INFO)
            __handler_console = logging.StreamHandler()
            __handler_console.setLevel(logging.INFO)
            Flog.__log.addHandler(__handler_console)
            __handler_write = logging.FileHandler(FPath.ROOT_PATH + "/.temp.log", encoding="utf-8")
            __handler_write.setLevel(logging.INFO)
            if Flog.__log is not None:
                Flog.__log.addHandler(__handler_write)
            # Flog.init_flog_file_handler()

    @staticmethod
    def init_flog_file_handler():
        if switch.LOG_ENABLE:
            if os.path.exists(FPath.ROOT_PATH + "/.temp.log"):
                with open(FPath.ROOT_PATH + "/.temp.log", "w", encoding="utf-8") as f:
                    f.write("")
                # os.remove(Router.ROOT_PATH + "/.temp.log")

    @staticmethod
    def remove_flog_handler():
        if switch.LOG_ENABLE:
            if Flog.__handler_write is not None:
                Flog.__log.removeHandler(Flog.__handler_write)

    @staticmethod
    def save_flog_format_elk(task):
        if task is None or task.task_info is None or task.task_info.task_id == "":
            task_id = ""
        else:
            task_id = task.task_info.task_id
        temp_log = FPath.ROOT_PATH + "/.temp.log"
        json_log = FPath.LOG_PATH + "/" + str(time.strftime("fast_auto_%Y%m%d", time.localtime())) + ".log"
        timestamp = str(int(time.time()))
        if task_id == "":
            trace_id = "@" + timestamp
        else:
            trace_id = task_id + "@" + timestamp
        if not switch.LOG_ENABLE:
            return
        with open(temp_log, "r", encoding="utf-8") as f:
            temp_content = f.read()
        json_content = ""
        if os.path.exists(json_log):
            with open(json_log, "r", encoding="utf-8") as f:
                json_content = f.read()
        with open(json_log, "w", encoding="utf-8")as f:
            content = {
                "trace_id": trace_id,
                "local_time": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                "host_name": Host.HOST_NAME,
                "timestamp": timestamp,
                "content": temp_content
            }
            # content = repr(content).replace("'", '"')
            content = json.dumps(content)
            if json_content == "":
                f.write(content)
            else:
                f.write(json_content + "\n" + content)

    @staticmethod
    def i(msg: str) -> None:
        if Flog.__log is None:
            print(msg)
        else:
            Flog.__log.info("flog >> " + msg)

    @staticmethod
    def e(msg: str) -> None:
        pass
