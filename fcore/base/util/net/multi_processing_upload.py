# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-04-02.
# Copyright (c) 2020 3KWan.
# Description :
import multiprocessing
import os
from typing import Any

from upyun.multi import UpYunMultiUploader

from fcore.base.util.flog import Flog
from fcore.base.util.net import frequest
from fcore.base.util.net.host import Host


def invoke_multi_upload(file_path: str, timestamp: str, game_id: str, version_code: str, platform_id) -> str:
    print("invoke multi upload")
    unit = 5 * 1024 * 1024
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    local_file = file_path
    file_name = os.path.basename(file_path)
    header = {"X-Upyun-Multi-Type": "application/vnd.android"}
    remote_file = "/3kfast_auto/{0}/{1}/{2}/{3}/{4}".format(game_id, platform_id, version_code, timestamp, file_name)
    uploader = frequest.upyun_manager.init_multi_uploader(remote_file, part_size=unit, headers=header)
    try:
        __upload(pool, uploader, local_file, unit)
        pool.close()
        pool.join()
        res = uploader.complete()
        print(res)
        return Host.OSS_SERVICE_NAME + remote_file
    except Exception as e:
        Flog.i(str(e))
        return ""


def __file_iterator(local_file: str, unit: int):
    with open(local_file, "rb") as f:
        while True:
            chunk_data = f.read(unit)
            if chunk_data == b"":
                break
            yield chunk_data


def __upload_task(uploader: UpYunMultiUploader, num: int, part_size: Any):
    print('Run task %s (%s)...' % (num, os.getpid()))
    uploader.upload(num, part_size)


def __upload(pool: multiprocessing.Pool, uploader: UpYunMultiUploader, local_file: str, unit: int):
    i = 0
    for chunk_data in __file_iterator(local_file, unit):
        # uploader.upload(i, chunk_data)
        print("upload chunk : " + str(i))
        pool.apply_async(__upload_task, args=(uploader, i, chunk_data,))
        i += 1
