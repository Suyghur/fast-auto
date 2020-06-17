# _*_coding:utf-8_*_
# Created by #zgy, on 2020-03-09.
# Copyright (c) 2020 3KWan.
# Description :
import base64
import datetime
import hashlib
import hmac
import os
from multiprocessing import Pool, cpu_count

import requests
from tqdm import tqdm
from upyun import UpYunServiceException, UpYunClientException

from fcore.base.util import Flog
from fcore.base.util.net import frequest
from fcore.base.util.net.host import Host


# class UploadHook:
#
#     def __call__(self, uploaded_size, total_size, status):
#         """
#         文件上传回调
#         :param uploaded_size: 远端文件大小
#         :param total_size: 文件总大侠
#         :param status: 状态
#         :return: None
#         """
#         if not status:
#             per = 100.0 * uploaded_size / total_size
#             print("---->uploading {0:.2f}%".format(per))
#         else:
#             print(" ----> uploading finish ")
#             print("---->uploading {0:.2f}%".format(100.0))


class UploadHook(tqdm):
    # Provides `update_to(n)` which uses `tqdm.update(delta_n)`.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_block = 0

    # def __call__(self, uploaded_size, total_size, status):
    #
    #     """
    #     文件上传回调
    #     :param uploaded_size: 远端文件大小
    #     :param total_size: 文件总大侠
    #     :param status: 状态
    #     :return: None
    #     """
    #     if not status:
    #         print("uploaded_size" + str(uploaded_size / 102400))
    #         print("total_size" + str(total_size / 1024000))
    #
    #         per = 100.0 * uploaded_size / total_size
    #         self.update((total_size - uploaded_size) / 1024)
    #         # print("---->uploading {0:.2f}%".format(per))
    #     else:
    #         print(" ----> uploading finish ")
    #         print("---->uploading {0:.2f}%".format(100.0))

    def update_to(self, uploaded_size, total_size, status):
        if not status:
            # print("uploaded_size" + str(uploaded_size))
            # print("total_size" + str(total_size))

            # per = 100.0 * uploaded_size / total_size
            self.update((total_size - uploaded_size) / 100 / 0.7)
        else:
            Flog.i(self.avg_time)
            # print(self.total)
            # print(self.miniters)
            # print("---->uploading {0:.2f}%".format(per))
        # else:
        #     print(" ----> uploading finish ")
        #     print("---->uploading {0:.2f}%".format(100.0))

        # per = 100.0 * block_num * block_size / total_size
        # if total_size is not None:
        #     self.total = total_size
        # self.update((block_num - self.last_block) * block_size)
        # self.last_block = block_num
        # if per > 100 or per == 100:
        #     per = 100
        # ViewNotify.download_file_notify(Host.CODE_SUCCESS, "下载成功", per, self.mod)
    # ViewNotify.download_file_notify(Host.CODE_SUCCESS, "下载成功", per, self.mod)


class Upload:

    @staticmethod
    def upload_file(file_path: str, timestamp: str, game_id: str, version_code: str, platform_id) -> str:
        try:
            file_name = os.path.basename(file_path)
            with open(file_path, "rb") as file:
                path = "/3kfast/{0}/{1}/{2}/{3}/{4}".format(timestamp, game_id, version_code, platform_id, file_name)
                with UploadHook(unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc=file_name) as hook:
                    res = frequest.upyun_manager.put(path, file, checksum=True, need_resume=True,
                                                     store=None, reporter=hook.update_to)
                    url = Host.OSS_SERVICE_NAME + path
                    return url

        except UpYunServiceException as se:
            Flog.i("upload bag file fail")
            Flog.i("Except an UpYunServiceException ...")
            Flog.i("Request Id : " + se.request_id)
            Flog.i("HTTP Status Code : " + str(se.status))
            Flog.i("Error code : " + se.err)
            Flog.i(" ----> Error Message : " + se.msg)
            return ""
        except UpYunClientException as ce:
            Flog.i("upload bag file fail")
            Flog.i("Except an UpYunClientException ...")
            Flog.i(" Error Message : " + ce.msg)
            return ""
        except Exception as e:
            Flog.i("upload bag file fail")
            return ""


class UploadApi:

    @staticmethod
    def __gmt_date():
        utc_str = datetime.datetime.utcnow()
        return utc_str.strftime('%a, %d %b %Y %H:%M:%S GMT')

    @staticmethod
    def __sign_str(opename, opepass, method, uri, gmtdate, policy):
        hmd5 = hashlib.md5()
        hmd5.update(opepass.encode(encoding='utf-8'))
        key = hmd5.hexdigest()
        if policy is None:
            msg = method + "&" + uri + "&" + gmtdate
        else:
            msg = method + "&" + uri + "&" + gmtdate + "&" + policy
        h = hmac.new(bytes(key, 'utf-8'), bytes(msg, 'utf-8'), digestmod='sha1')
        return "UPYUN " + opename + ":" + str(base64.b64encode(h.digest()), 'utf-8')

    @staticmethod
    def rest_upload(file_path: str, timestamp: str, game_id: str, version_code: str, platform_id) -> str:
        try:
            file_name = os.path.basename(file_path)
            path = "/3kfast_auto/{0}/{1}/{2}/{3}/{4}".format(game_id, platform_id, version_code, timestamp, file_name)
            gmtdate = UploadApi.__gmt_date()
            auth = UploadApi.__sign_str(Host.UPYUN_USERNAME, Host.UPYUN_PASSWORD, "PUT",
                                        "/" + Host.UPYUN_SERVICE + path, UploadApi.__gmt_date(), policy=None)
            Flog.i(auth)
            headers = {'Date': gmtdate,
                       'Authorization': auth}
            with open(file_path, 'rb') as f:
                Flog.i('http://v0.api.upyun.com' + "/" + Host.UPYUN_SERVICE + path)
                r = requests.put('http://v0.api.upyun.com/yxupload' + path, data=f, headers=headers)
                return Host.OSS_SERVICE_NAME + path
        except UpYunServiceException as se:
            Flog.i("upload bag file fail")
            Flog.i("Except an UpYunServiceException ...")
            Flog.i("Request Id : " + se.request_id)
            Flog.i("HTTP Status Code : " + str(se.status))
            Flog.i("Error code : " + se.err)
            Flog.i(" ----> Error Message : " + se.msg)
            return ""
        except UpYunClientException as ce:
            Flog.i("upload bag file fail")
            Flog.i("Except an UpYunClientException ...")
            Flog.i(" Error Message : " + ce.msg)
            return ""
        except Exception as e:
            Flog.i("upload bag file fail : " + str(e))
            return ""


class MultiUpload:

    def __init__(self, file_path: str, timestamp: str, game_id: str, version_code: str, platform_id):
        self.__unit = 5 * 1024 * 1024
        self.__pool = Pool(cpu_count())
        self.__local_file = file_path
        self.__file_name = os.path.basename(file_path)
        self.__header = {"X-Upyun-Multi-Type": "application/vnd.android"}
        self.__remote_file = "/3kfast_auto/{0}/{1}/{2}/{3}/{4}".format(game_id, platform_id, version_code, timestamp,
                                                                       self.__file_name)
        self.__uploader = frequest.upyun_manager.init_multi_uploader(self.__remote_file, part_size=self.__unit,
                                                                     headers=self.__header)

    def __file_iterator(self):
        with open(self.__local_file, "rb") as f:
            while True:
                chunk_data = f.read(self.__unit)
                if chunk_data == b"":
                    break
                yield chunk_data

    def __upload_task(self, num, part_size):
        print('Run task %s (%s)...' % (num, os.getpid()))
        self.__uploader.upload(num, part_size)

    def __upload(self):
        i = 0
        for chunk_data in self.__file_iterator():
            # uploader.upload(i, chunk_data)
            print("upload chunk : " + str(i))
            self.__pool.apply_async(self.__upload_task, args=(i, chunk_data,))
            i += 1

    def invoke_multi_upload(self) -> str:
        Flog.i("rest_multi_upload...")
        # file_name = os.path.basename(file_path)
        # remote_file = "/3kfast_auto/{0}/{1}/{2}/{3}/{4}".format(game_id, platform_id, version_code, timestamp,
        #                                                         file_name)

        try:
            # for chunk_data in MultiUpload.__file_iterator(local_file, unit):
            #     print("upload chunk : " + str(i))
            #     uploader.upload(i, chunk_data)
            #     i += 1
            # else:
            #     uploader.complete()
            #     Flog.i("upload complete")
            # pool = multiprocessing.Pool(multiprocessing.cpu_count())
            self.__upload()
            self.__pool.close()
            self.__pool.join()
            res = self.__uploader.complete()
            print(res)
            return Host.OSS_SERVICE_NAME + self.__remote_file
        except Exception as e:
            Flog.i(str(e))
            return ""
