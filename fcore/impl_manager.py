# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-25.
# Copyright (c) 2020 3KWan.
# Description :
import json
import multiprocessing
import os
import shutil
import sys
import time
import random
from typing import Optional, Tuple, Any

from fcore.api import api_manager
from fcore.base import resource, invoke_script, switch, handle_xml, apk_utils, pack_core
from fcore.base.dao import get_common_sdk_size, get_channel_sdk_size
from fcore.base.util.flog import Flog
from fcore.entity.bean.auto_test_info import AutoTestInfo
from fcore.entity.result import Task
from fcore.base.util import java, env, android, string
from fcore.base.util.net import multi_processing_upload
from fcore.base.util.net.host import Host
from fcore.base.util.path import FPath


class ImplManager:

    def __init__(self):
        if env.get_sys_platform_code() != 3:
            multiprocessing.set_start_method("forkserver")
        else:
            # win平台只支持这种进程启动方式
            multiprocessing.set_start_method("spawn")
        config_path = os.getcwd() + "/config.json"
        with open(config_path, "r", encoding="utf-8")as f:
            config = json.load(f)
            switch.DB_ENABLE = config["db_cfg"]["enable"]
            switch.WX_DEV_ENABLE = config["notify_wx_cfg"]["dev_group_enable"]
            switch.WX_TEST_ENABLE = config["notify_wx_cfg"]["test_group_enable"]

        FPath.init(config_path)
        Host.init(config_path)
        Flog.i("Curr Python Version : " + env.get_py_version())
        Flog.i("Curr System Platform : " + sys.platform)
        Flog.i("Working directory : " + os.getcwd())

        self.__package_count = 0
        self.__current_index = 0
        self.__wx_err_msg = "打包内部"
        self.__data = {
            "task_id": "0",
            "package_id": "0",
            "status_code": 0,
            "bag_url": "",
            "common_sdk_version": "0",
            "channel_sdk_version": "0",
            "package_size": 0,
            "ext": {
                "package_size": 0,
                "rh_sdk_size": 0,
                "channel_sdk_size": 0,
                "plugin_size": 0,
                "rh_time": 0,
                "from_time": 0,
                "upload_time": 0
            }
        }
        self.__random_link_list = []
        self.__package_id_list = []

    @staticmethod
    def get_task(task_id: str = "") -> Optional[Task]:
        """
        :param task_id
        :return Task对象
        """
        data = {
            "task_id": task_id,
            "ext": {}
        }
        return api_manager.api_get_task(data)

    def __report_status(self, data: dict, file_link: str = "") -> Tuple[bool, Any]:
        """

        :param data: 请求参数
        :param file_link: log文件地址
        :return: 第一个返回值：是否继续执行，第二个返回值：该接口请求是否成功，为None成功，非None异常信息
        """
        if "" != file_link:
            return api_manager.api_report_status(data, True, file_link)
        else:
            return api_manager.api_report_status(data)

    def report_task(self, task: Task, status_code: int = 1210, random_package_id: str = "", random_link: str = "",
                    auto_test: AutoTestInfo = None) -> Tuple[bool, Any]:
        """
        上报任务状态
        :param auto_test:
        :param task:
        :param status_code 请求参数
        :param random_package_id:
        :param random_link:
        :return
        """
        task_data = {
            "task_id": self.__data["task_id"],
            "status_code": status_code
        }
        wx_msg = ""
        if status_code == 1210:
            wx_msg = string.get_wx_notify_msg_theme(True).format(task.task_info.task_id, task.bag_info.group_name,
                                                                 task.params_info.common_params.channel_name,
                                                                 task.sdk_info.common_sdk.version,
                                                                 random_link)
            if task.task_info.is_auto_test == 1 and auto_test is not None:
                api_manager.api_send_2_auto_test(task, random_package_id, random_link, auto_test)
        else:
            wx_msg = string.get_wx_notify_msg_theme(False).format(task.task_info.task_id, task.bag_info.group_name,
                                                                  task.params_info.common_params.channel_name,
                                                                  task.sdk_info.common_sdk.version)
        api_manager.api_notify_wx_test_group(wx_msg)

        return api_manager.api_report_task(task_data)

    def api_send_msg_2_wx(self, err_msg: str):
        msg = "{0}-{1}（打包失败，任务ID={2}，分包ID={3}，原因：{4}）".format(Host.HOST_NAME, Host.ENV,
                                                              self.__data["task_id"], self.__data["package_id"],
                                                              err_msg)
        api_manager.api_notify_wx_dev_group(msg)

    def execute(self, task: Task, auto_test: AutoTestInfo = None) -> bool:
        """
        :param task task对象
        :param auto_test: 自动化测试对象
        :return 是否执行成功
        """
        config_path = os.getcwd() + "/config.json"
        with open(config_path, "r", encoding="utf-8")as f:
            config = json.load(f)
            switch.APKTOOL232 = config["apktool232_cfg"]["group_id"]

        task_id = task.task_info.task_id
        common_sdk_version = task.sdk_info.common_sdk.version
        channel_sdk_version = task.sdk_info.channel_sdk.version
        if len(task.params_info.common_params.package_chanle.keys()) > 0:
            package_id = list(task.params_info.common_params.package_chanle.keys())[0]
            is_param_err = False
        else:
            package_id = 0
            is_param_err = True
        self.__package_count = task.params_info.common_params.total
        self.__current_index = 0
        self.__wx_err_msg = "打包内部"
        self.__data = {
            "task_id": task_id,
            "package_id": package_id,
            "status_code": 0,
            "bag_url": '',
            "common_sdk_version": common_sdk_version,
            "channel_sdk_version": channel_sdk_version,
            "package_size": 0,
            "ext": {
                "package_size": 0,
                "rh_sdk_size": 0,
                "channel_sdk_size": 0,
                "plugin_size": 0,
                "rh_time": 0,
                "from_time": 0,
                "upload_time": 0
            }
        }
        self.__random_link_list = []
        self.__package_id_list = []

        if is_param_err:
            raise Exception("任务参数异常，分包ID为空")

        if not self.__init_workspace(task) or not self.__pack(task, auto_test):
            # 上报打包失败和日志
            Flog.i("上报打包失败和日志")
            self.__data["status_code"] = 1204
            self.__data["package_size"] = 0
            self.__report_status(self.__data)

            # 上报任务状态（失败）
            Flog.i("上报任务状态（失败）")
            self.report_task(task, 1204)

            # 企业微信机器人提醒

            self.api_send_msg_2_wx(self.__wx_err_msg)
            return False

    def __init_workspace(self, task: Task) -> bool:
        """
        初始化工作空间
        :param task:
        :return:
        """
        signal = 0
        try:
            signal = 0
            # 清空现有工作空间
            Flog.i("清空现有工作空间")
            if os.path.exists(FPath.WORKSPACE_PATH):
                shutil.rmtree(FPath.WORKSPACE_PATH)

            if os.path.exists(FPath.ROOT_PATH + "/output"):
                shutil.rmtree(FPath.ROOT_PATH + "/output")
            os.mkdir(FPath.ROOT_PATH + "/output")

            os.mkdir(FPath.WORKSPACE_PATH)
            os.mkdir(FPath.WORKSPACE_PATH + "/script")

            result, plugin_sdk_size = resource.check_sdk_resource(task)
            if result:
                # 拷贝处理打包资源
                Flog.i("拷贝处理打包资源")
                common_sdk_path = FPath.COMMON_SDK_PATH + "/" + task.sdk_info.common_sdk.version
                shutil.copytree(common_sdk_path, FPath.WORKSPACE_PATH + "/common")
                channel_sdk_path = FPath.CHANNEL_SDK_PATH + "/" + task.params_info.common_params.channel_name
                shutil.copytree(channel_sdk_path, FPath.WORKSPACE_PATH + "/channel")
                signal = signal + 1

            # 读取融合、渠道、插件大小
            Flog.i("读取融合、渠道、插件大小")
            self.__data["ext"]["rh_sdk_size"] = get_common_sdk_size(task.sdk_info.common_sdk.version)
            self.__data["ext"]["channel_sdk_size"] = get_channel_sdk_size(task.params_info.common_params.channel_name,
                                                                          task.sdk_info.channel_sdk.version)
            self.__data["ext"]["plugin_size"] = plugin_sdk_size

            if resource.check_origin_bag(task):
                self.__data["ext"]["package_size"] = os.path.getsize(
                    FPath.ORIGIN_APK_PATH + "/" + task.bag_info.group_id + "/" + task.bag_info.game_id + ".apk")
                shutil.copy(
                    FPath.ORIGIN_APK_PATH + "/" + task.bag_info.group_id + "/" + task.bag_info.game_id + ".apk",
                    FPath.WORKSPACE_PATH + "/origin.apk")
                signal = signal + 1

            if resource.check_keystore(task):
                signal = signal + 1

            if resource.check_common_script(task):
                signal = signal + 1

            if resource.check_game_script(task):
                signal = signal + 1

            if resource.check_game_resource(task):
                signal = signal + 1

            if signal == 6:
                return True
        except Exception as e:
            self.__wx_err_msg = str(e)
            Flog.i(str(e))
        return False

    @staticmethod
    def __decompile(task: Task):
        """
        反编译母包
        :param task:
        :return:
        """
        Flog.i("反编译母包")
        if android.decompile_apk(task):
            return True
        else:
            return False

    def __pack(self, task: Task, auto_test: AutoTestInfo = None) -> bool:
        start_time = int(time.time())  # 融合处理的起始时间

        if not self.__decompile(task):
            self.__wx_err_msg = "反编译失败"
            return False

        # 处理母包中的融合代码、融合资源
        Flog.i("处理母包中的融合代码和融合资源")
        if not pack_core.handle_origin():
            self.__wx_err_msg = "处理母包中的融合代码、融合资源失败"
            return False
        old_package_name = handle_xml.replace_package_name(task.params_info.game_params.game_package_name)
        ext = {
            "old_package_name": old_package_name,
            "gen_path": FPath.ROOT_PATH
        }
        # 处理融合sdk代码和资源
        Flog.i("处理融合sdk代码和资源")
        if os.path.exists(FPath.COMMON_SDK_PATH + "/" + task.sdk_info.common_sdk.version):
            # 转换sdk代码
            if not java.jar2dex(FPath.WORKSPACE_PATH + "/common", FPath.WORKSPACE_PATH + "/common"):
                self.__wx_err_msg = "处理融合sdk代码和资源，jar2dex失败"
                return False
            if not java.dex2smali(FPath.WORKSPACE_PATH + "/common/classes.dex", FPath.DECOMPILE_PATH + "/smali"):
                self.__wx_err_msg = "处理融合sdk代码和资源，dex2smali失败"
                return False
        else:
            self.__wx_err_msg = "融合sdk代码和资源不存在"
            return False
        # 处理渠道sdk代码和资源
        Flog.i("处理渠道sdk代码和资源")
        if os.path.exists(FPath.CHANNEL_SDK_PATH + "/" + task.params_info.common_params.channel_name):
            # 转换sdk代码
            if not java.jar2dex(FPath.WORKSPACE_PATH + "/channel/libs", FPath.WORKSPACE_PATH + "/channel/libs"):
                self.__wx_err_msg = "处理渠道sdk代码和资源，jar2dex失败"
                return False
            if not java.dex2smali(FPath.WORKSPACE_PATH + "/channel/libs/classes.dex",
                                  FPath.DECOMPILE_PATH + "/smali"):
                self.__wx_err_msg = "处理渠道sdk代码和资源，dex2smali失败"
                return False
        else:
            self.__wx_err_msg = "渠道sdk代码和资源不存在"
            return False

        if not pack_core.pack(task):
            self.__wx_err_msg = "pack_core.pack失败"
            return False

        # 处理插件sdk代码和资源（如果需要）
        if task.task_info.has_plugin_sdk > 0:
            Flog.i("处理插件sdk代码和资源")
            for plugin_sdk in task.sdk_info.plugin_sdk:
                Flog.i("正在处理插件sdk : " + plugin_sdk)
                plugin_sdk_path = FPath.WORKSPACE_PATH + "/plugin/" + plugin_sdk
                # 转换sdk代码
                if not java.jar2dex(plugin_sdk_path, plugin_sdk_path):
                    self.__wx_err_msg = "处理插件sdk代码和资源，jar2dex失败"
                    return False
                if not java.dex2smali(plugin_sdk_path + "/classes.dex", FPath.DECOMPILE_PATH + "/smali"):
                    self.__wx_err_msg = "处理插件sdk代码和资源，dex2smali失败"
                    return False

        # 执行融合脚本
        Flog.i("执行融合脚本")
        if not invoke_script.common(task, ext):
            self.__wx_err_msg = "执行融合脚本失败"
            return False
        # 执行渠道脚本
        Flog.i("执行渠道脚本")
        if not invoke_script.channel(task, ext):
            self.__wx_err_msg = "执行渠道脚本失败"
            return False
        # 执行插件脚本（如果需要）
        if task.task_info.has_plugin_sdk > 0:
            Flog.i("执行插件脚本")
            for plugin_name in task.sdk_info.plugin_sdk:
                if not invoke_script.plugin(task, plugin_name, ext):
                    self.__wx_err_msg = "执行插件{0}脚本失败".format(plugin_name)
                    return False
        # 执行游戏脚本（非坦克前线）
        if task.bag_info.group_id != "5":
            Flog.i("执行游戏脚本（非坦克前线）")
            if not invoke_script.game(task, ext):
                self.__wx_err_msg = "执行游戏脚本（非坦克前线）失败"
                return False

        # generate new R.java
        if apk_utils.generate_r_file(task.params_info.game_params.game_package_name):
            Flog.i("generate new R.java success")
        else:

            self.__wx_err_msg = "generate new R.java failure失败"
            Flog.i("generate new R.java failure")
            return False
        android.split_dex()

        # 融合处理时间
        self.__data["ext"]["rh_time"] = int(time.time()) - start_time

        # 处理融合sdk参数
        if not pack_core.is_v3_mode() or task.bag_info.group_id == "5":
            if not self.old_mode_generate_subpackage(task, ext, auto_test):
                return False
        else:
            if not self.generate_subpackage(task, auto_test):
                return False
        return True

    @staticmethod
    def __compile(task: Task) -> bool:
        return android.compile_apk(task)

    @staticmethod
    def __sign(task: Task, package_id, new_mode: bool = False) -> Tuple[bool, str]:
        if apk_utils.sign(task, new_mode):
            if not os.path.exists(FPath.ROOT_PATH + "/output/" + task.params_info.common_params.game_id):
                os.makedirs(FPath.ROOT_PATH + "/output/" + task.params_info.common_params.game_id)
            new_apk = FPath.ROOT_PATH + "/output/" + task.params_info.common_params.game_id + "/" + apk_utils.format_output_name(
                task, package_id)
            if new_mode:
                shutil.copy(FPath.WORKSPACE_PATH + "/new_mode_output.apk", new_apk)
                os.remove(FPath.WORKSPACE_PATH + "/new_mode_output.apk")
            else:
                shutil.copy(FPath.WORKSPACE_PATH + "/output.apk", new_apk)
            return True, new_apk
        else:
            return False, ""

    def __upload(self, task: Task, file_path: str) -> str:
        timestamp = str(int(time.time()))  # 当前时间
        game_id = task.params_info.common_params.game_id
        version_code = task.params_info.game_params.game_version_code
        platform_id = task.params_info.common_params.channel_id
        cnt = 0
        while cnt <= 3:
            start = time.time()
            # url = UploadApi.rest_upload(file_path, timestamp, game_id, version_code, platform_id)
            url = multi_processing_upload.invoke_multi_upload(file_path, timestamp, game_id, version_code, platform_id)
            # multi_uploader = MultiUpload(file_path, timestamp, game_id, version_code, platform_id)
            # url = multi_uploader.invoke_multi_upload()
            end = time.time()
            upload_time = int(end - start)
            self.__data["ext"]["upload_time"] = upload_time
            Flog.i("multi processing upload " + file_path + " time: " + str(upload_time))
            if url == "":
                cnt += 1
                Flog.i("上传失败，重试第 " + str(cnt) + " 次")
                continue
            return url

    def old_mode_generate_subpackage(self, task: Task, ext, auto_test: AutoTestInfo = None) -> bool:
        channel_id = task.params_info.common_params.channel_id
        for package_id in task.params_info.common_params.package_chanle:
            start_time = int(time.time())  # 统计处理分包起始时间

            Flog.i("正在打第{0}/{1}个分包，分包ID={2}".format(self.__current_index + 1, self.__package_count, package_id))
            if task.bag_info.group_id == "5":
                if not invoke_script.game(task, ext):
                    self.__wx_err_msg = "打分包执行游戏脚本失败"
                    return False
            if not pack_core.handle_common_params(task, channel_id, package_id):
                self.__wx_err_msg = "打分包执行handle_v3_common_params失败"
                return False
            if not self.__compile(task):
                self.__wx_err_msg = "打分包回编译失败"
                return False
            signed, new_apk = self.__sign(task, package_id)

            if not signed:
                self.__wx_err_msg = "打分包重签名失败"
                return False

            if not self.__upload_bag(task, new_apk, package_id, start_time, auto_test):
                return False
        return True

    def generate_subpackage(self, task: Task, auto_test: AutoTestInfo = None):
        """
        v3除坦克外新分发模式
        :return:
        """
        # 拷贝assets下的配置文件
        shutil.copy(FPath.DECOMPILE_PATH + "/assets/fuse_cfg.properties", FPath.WORKSPACE_PATH)
        # 删除原有的配置文件
        if os.path.exists(FPath.DECOMPILE_PATH + "/assets/fuse_cfg.properties"):
            os.remove(FPath.DECOMPILE_PATH + "/assets/fuse_cfg.properties")

        # 回编译
        compile_start_time = int(time.time())  # 统计处理分包起始时间
        if not self.__compile(task):
            return False
        compile_time = int(time.time()) - compile_start_time

        for package_id in task.params_info.common_params.package_chanle:
            start_time = int(time.time())  # 统计处理分包起始时间
            Flog.i("正在打第{0}/{1}个分包，分包ID={2}".format(self.__current_index + 1, self.__package_count, package_id))
            if not pack_core.new_mode_handle_common_params(task.params_info.common_params.channel_id, package_id):
                return False
            if not pack_core.implant_fuse_profile():
                return False

            signed, new_apk = self.__sign(task, package_id, True)

            if not signed:
                self.__wx_err_msg = "打分包重签名失败"
                return False
            if not self.__upload_bag(task, new_apk, package_id, start_time, compile_time, auto_test):
                return False

        return True

    def __upload_bag(self, task: Task, new_apk: str, package_id: str, start_time: int, compile_time: int = 0,
                     auto_test: AutoTestInfo = None) -> bool:
        # 上传包
        bag_url = self.__upload(task, new_apk)
        if bag_url is None and bag_url == '':
            self.__wx_err_msg = "打分包上传包体失败"
            return False

        if os.path.exists(new_apk):
            # 分包大小
            self.__data["package_size"] = os.path.getsize(new_apk)
            # 删除新包
            os.remove(new_apk)

        # 上报打包状态
        self.__data["package_id"] = package_id
        self.__data["status_code"] = 1210
        self.__data["bag_url"] = bag_url
        if self.__current_index + 1 == 1:
            self.__data["ext"]["from_time"] = int(time.time()) - start_time + compile_time  # 分包处理时间
        else:
            self.__data["ext"]["from_time"] = int(time.time()) - start_time  # 分包处理时间
        self.__random_link_list.append(bag_url)
        self.__package_id_list.append(package_id)
        is_stop, msg = self.__report_status(self.__data)
        if not msg:
            # 上报打包状态接口正常
            # 是否中止执行
            if is_stop:
                Flog.i("中断任务")
                return True
            # 判断是否最后一个子包
            self.__current_index += 1
            if self.__current_index == self.__package_count:
                # 上报任务状态（成功）
                random_link = random.choice(self.__random_link_list)
                random_package_id = self.__package_id_list[self.__random_link_list.index(random_link)]
                result, err_msg = self.report_task(task, 1210, random_package_id, random_link, auto_test)
                if err_msg:
                    self.__wx_err_msg = err_msg
                return result
            return True
        else:
            # 上报打包状态接口异常
            Flog.i("上报打包成功接口异常")
            self.__wx_err_msg = msg
            return False
