# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-03-05.
# Copyright (c) 2020 3KWan.
# Description :
import os
import shutil
import zipfile
from os.path import isfile

from tqdm import tqdm

from fcore.base.util.flog import Flog


def unzip(res_zip_path: str, dis_path: str) -> bool:
    """
    解压zip文档
    :param res_zip_path:
    :param dis_path:
    :return: None
    """
    if zipfile.is_zipfile(res_zip_path):
        with zipfile.ZipFile(res_zip_path, "r") as zf:
            for name in tqdm(zf.namelist(), desc="Extract files", unit="files"):
                # 过滤MacOS生成的__MACOSX开头的文件
                if not name.startswith("__MACOSX"):
                    zf.extract(name, path=dis_path)
            zf.close()
        return True
    else:
        Flog.i(res_zip_path + " is not a zip file")
        return False


def insert_file_2_apk(apk_path: str, target_path: str, data: bytes) -> bool:
    try:
        with zipfile.ZipFile(apk_path, "a")as zf:
            with zf.open(target_path, "w")as f:
                f.write(data)
        return True
    except Exception as e:
        Flog.i(str(e))
        return False


def list_file(src: str, _files: list, ignore=None) -> None:
    if ignore is None:
        ignore = []
    if os.path.exists(src):
        if os.path.isfile(src) and src not in ignore:
            _files.append(src)
        elif os.path.isdir(src):
            for f in os.listdir(src):
                if src not in ignore:
                    list_file(os.path.join(src, f), _files, ignore)


def copy_files(src: str, dst: str) -> bool:
    """
    将目标文件夹的文件复制到指定目录
    :param src:
    :param dst:
    :return:
    """
    if not os.path.exists(src):
        Flog.i("the src is not exists path:" + src)
        return

    if os.path.isfile(src):
        copy_file(src, dst)
        return

    for f in os.listdir(src):
        source_file = os.path.join(src, f)
        target_file = os.path.join(dst, f)
        if os.path.isfile(source_file):
            copy_file(source_file, target_file)
        else:
            copy_files(source_file, target_file)


def copy_file(src: str, dst: str) -> None:
    """
    复制文件
    :param src:
    :param dst:
    :return:
    """
    if not os.path.exists(src):
        return

    if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src):
        dst_dir = os.path.dirname(dst)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        dst_file_stream = open(dst, 'wb')
        source_file_stream = open(src, 'rb')
        dst_file_stream.write(source_file_stream.read())
        dst_file_stream.close()
        source_file_stream.close()


def del_file_folder(src):
    if os.path.exists(src):
        if os.path.isfile(src):
            try:
                src = src.replace('\\', '/')
                os.remove(src)
            except Exception as e:
                Flog.i(str(e))
        elif os.path.isdir(src):
            for item in os.listdir(src):
                item_src = os.path.join(src, item)
                del_file_folder(item_src)

            try:
                os.rmdir(src)
            except Exception as e:
                Flog.i(str(e))


def remove_files(target: str) -> bool:
    """
    删除文件或文件夹
    :param target: 目标文件或文件夹路径
    :return: 是否成功
    """
    try:
        if isfile(target):
            os.remove(target)
            return True
        else:
            shutil.rmtree(target)
            return True
    except Exception as e:
        Flog.i(str(e))
        return False
