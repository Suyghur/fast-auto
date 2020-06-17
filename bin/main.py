# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-25.
# Copyright (c) 2020 3KWan.
# Description :
import os
import sys
import time
import goto

from goto import with_goto

# 定时间隔

INTERVAL = 30


@with_goto
def start():
    impl = fcore.impl_manager.ImplManager()
    fcore.base.util.flog.Flog.init()
    last_task_id = ''
    # 循环标记
    label.begin
    fcore.base.util.flog.Flog.init_flog_file_handler()
    fcore.base.util.flog.Flog.i("------开始查询任务，上一任务ID=" + last_task_id + "------")
    task = fcore.impl_manager.ImplManager.get_task(last_task_id)
    fcore.base.util.flog.Flog.i("------结束查询任务------")
    if task is None or task.task_info is None or task.task_info.task_id == '':
        fcore.base.util.flog.Flog.i("------无打包任务，进入定时查询------")
        # 定时查询
        start = time.time()
        time.sleep(INTERVAL)
        end = time.time()
        fcore.base.util.flog.Flog.i("------执行时间：" + str(end - start) + "------")
        fcore.base.util.flog.Flog.save_flog_format_elk(task)
        goto.begin
    else:
        last_task_id = task.task_info.task_id
        fcore.base.util.flog.Flog.i("------进入打包任务：" + last_task_id + "------")

        try:
            impl.execute(task)
        except BaseException as e:
            # 上报任务状态（失败）
            impl.report_task(task,1204)
            # 企业微信机器人提醒
            impl.api_send_msg_2_wx("全局捕获：" + str(e))
            fcore.base.util.flog.Flog.i(str(e))
        fcore.base.util.flog.Flog.save_flog_format_elk(task)
        goto.begin
    label.end


if __name__ == "__main__":
    sys.path.append(os.getcwd())
    import fcore.impl_manager
    import fcore.base.util.flog
    import fcore.entity.result

    start()
