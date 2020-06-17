# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-10-21.
# Copyright (c) 2019 3KWan.
# Description :handle commonsdk v2 version packing
import os
from fcore.base import sdk_helper
from fcore.base.util.flog import Flog
from fcore.entity.result import Task
from fcore.base.util import fio
from fcore.base.util.path import FPath

try:
    import xml.etree.cElementTree as elementTree
except ImportError:
    import xml.etree.ElementTree as elementTree

android_ns = "http://schemas.android.com/apk/res/android"


def del_smali_code() -> bool:
    """
    delete 3k common comsdk smali code.
    :return:
    """
    try:
        del_smali_path = ["/smali/cn/kkk/commonsdk", "/smali/com/tencent/smtt", "/smali/com/tencent/tbs",
                          "/smali/cn/impl", "/smali/cn/kkk/sdk"]

        if del_smali_path is None or len(del_smali_path) <= 0:
            return True

        for deletePath in del_smali_path:
            delete_path = FPath.DECOMPILE_PATH + deletePath
            if not os.path.exists(delete_path):
                Flog.i("can't find this folder path :" + delete_path)
                continue
            fio.del_file_folder(delete_path)
        return True
    except Exception as e:
        Flog.i("del_smali_code() error " + str(e))
        return False


def delete_so_file() -> bool:
    """
    delete so file.
    :return:
    """
    try:
        so_file_path = FPath.DECOMPILE_PATH + "/lib"
        if not os.path.exists(so_file_path):
            Flog.i("can't find so path :" + so_file_path)
            return True

        so_files = []
        fio.list_file(so_file_path, so_files, [])
        if so_files is None or len(so_files) <= 0:
            return True

        for so_file in so_files:
            if 'liblbs.so' in so_file:
                fio.del_file_folder(so_file)
        return True
    except Exception as e:
        Flog.i("delete_so_file() error " + str(e))
        return False


def del_system_label(label):
    # 开始删除字段
    filelist = ["colors", "dimens", "ids", "public", "strings", "styles"]

    for f in filelist:
        fpath = FPath.DECOMPILE_PATH + "/res/values/" + f + ".xml"
        if os.path.exists(fpath):
            tree = elementTree.parse(fpath)
            root = tree.getroot()
            for node in list(root):
                attrib_name = node.attrib.get('name')
                if attrib_name is None:
                    continue

                if attrib_name.lower().startswith(label):
                    root.remove(node)
                    Flog.i("remove debug res index name:" + attrib_name + " from" + fpath)
            tree.write(fpath, "UTF-8")

    res_path = FPath.DECOMPILE_PATH + "/res"
    filelist = []
    fio.list_file(res_path, filelist, [])
    for f in filelist:
        if os.path.basename(f).lower().startswith(label):
            fio.del_file_folder(f)
            Flog.i("remove debug res file:" + f)


def del_manifest_infos(decompile_dir: str) -> bool:
    """
    delete androidManifest infos
    :param decompile_dir:
    :return:
    """
    try:
        # 删除cn.kkk.comsdk.LoginActivity
        sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'cn.kkk.comsdk.LoginActivity')
        # 删除cn.kkk.comsdk.AccountActivity
        sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'cn.kkk.comsdk.AccountActivity')
        # 删除cn.kkk.comsdk.ChargeActivity
        sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'cn.kkk.comsdk.ChargeActivity')
        # 删除cn.kkk.comsdk.KkkService
        sdk_helper.removeMinifestComponentByName(decompile_dir, 'service', 'cn.kkk.comsdk.KkkService')

        sdk_helper.removeMinifestComponentByName(decompile_dir, 'service', 'cn.kkk.sdk.ui.floatview.FlyingBallService')
        sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'cn.kkk.sdk.WebviewPageActivity')

        sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'com.unionpay.uppay.PayActivity')
        sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'com.unionpay.uppay.PayActivityEx')
        sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity', 'com.alipay.sdk.app.H5PayActivity')
        sdk_helper.removeMinifestComponentByName(decompile_dir, 'activity-alias', '.wxapi.WXPayEntryActivity')

        # 删除3KWAN_HasLogo meta-data标签
        sdk_helper.removeMinifestComponentByName(decompile_dir, 'meta-data', '3KWAN_HasLogo')
        return True
    except Exception as e:
        Flog.i("del_manifest_infos() error " + str(e))
        return False


def del_3k_res() -> bool:
    """
    delete 3k res eg:kkk_
    :return:
    """
    try:
        res_path = FPath.DECOMPILE_PATH + "/res"
        if not os.path.exists(res_path):
            Flog.i("can't find this res path : " + res_path)
            return False

        res_files = []
        fio.list_file(res_path, res_files, [])
        if res_files is None or len(res_files) <= 0:
            return True

        for res in res_files:
            if "kkk_" in res:
                fio.del_file_folder(res)

        # 开始删除字段
        # decompile_dir = path_utils.get_full_path(decompile_dir)
        file_list = ["colors", "dimens", "ids", "public", "strings", "styles"]
        for f in file_list:
            fpath = FPath.DECOMPILE_PATH + "/res/values/" + f + ".xml"
            if os.path.exists(fpath):
                tree = elementTree.parse(fpath)
                root = tree.getroot()
                for node in list(root):
                    attrib_name = node.attrib.get("name")
                    if attrib_name is None:
                        continue

                    if attrib_name.lower().startswith("kkk_") or attrib_name.lower().startswith("tk_"):
                        root.remove(node)
                tree.write(fpath, "UTF-8")

        res_path = FPath.DECOMPILE_PATH + "/res"
        xml_list = []
        fio.list_file(res_path, xml_list, [])
        for xml in xml_list:
            if os.path.basename(xml).lower().startswith("kkk_") or os.path.basename(xml).lower().startswith("tk_"):
                fio.del_file_folder(xml)

        return True
    except Exception as e:
        Flog.i("del_3k_res() error " + str(e))
        return False


# def handle_v2_media_params(task: Task) -> bool:
#     if task.params_info.plugin_params is None:
#         return False
#
#     manifest_path = Router.DECOMPILE_PATH + "/AndroidManifest.xml"
#     if not os.path.exists(manifest_path):
#         Flog.i("can't find this file : " + manifest_path)
#         return False
#     try:
#         elementTree.register_namespace("android", android_ns)
#         tree = elementTree.parse(manifest_path)
#
#         for key in task.params_info.plugin_params:
#             sdk_helper.handle_meta_data(tree, key, task.params_info.plugin_params[key])
#
#         tree.write(manifest_path, "utf-8")
#         return True
#     except Exception as e:
#         Flog.i("handle_v2_media_params() error " + str(e))
#         return False


def handle_v2_common_params(task: Task, package_id: str, package_chanle_dict: dict) -> bool:
    """

    :param task:
    :param package_id:
    :param package_chanle_dict:
    :return:
    """
    manifest_path = FPath.DECOMPILE_PATH + "/AndroidManifest.xml"
    if not os.path.exists(manifest_path):
        Flog.i("AndroidManifest.xml not exists")
        return False
    try:
        # 根据渠道标识获取本地融合渠道id
        channel_id = task.params_info.common_params.channel_id
        if channel_id is None:
            channel_id = ""
        elementTree.register_namespace("android", android_ns)
        tree = elementTree.parse(manifest_path)
        root = tree.getroot()

        application = root.find("application")
        if application is None:
            return False

        name = "{" + android_ns + "}name"
        value = "{" + android_ns + "}value"
        create_package_id = True
        create_chanle_id = True
        create_platform_chanle_id = True

        meta_datas = root.find(".//application").findall("meta-data")
        if meta_datas is None:
            package_id_node = elementTree.SubElement(application, "meta-data")
            package_id_node.set(name, "3KWAN_PackageID")
            package_id_node.set(value, package_id)

            chanle_id_node = elementTree.SubElement(application, "meta-data")
            chanle_id_node.set(name, "3KWAN_ChanleId")
            chanle_id_node.set(value, package_chanle_dict[package_id])

            platform_id_node = elementTree.SubElement(application, "meta-data")
            platform_id_node.set(name, "3KWAN_Platform_ChanleId")
            platform_id_node.set(value, channel_id)
        else:
            for meta_data in meta_datas:
                meta_data_name = meta_data.get(name)
                if meta_data_name == "3KWAN_PackageID":
                    create_package_id = False
                    meta_data.set(value, package_id)

                if meta_data_name == "3KWAN_ChanleId":
                    create_chanle_id = False
                    meta_data.set(value, package_chanle_dict[package_id])

                if meta_data_name == "3KWAN_Platform_ChanleId":
                    create_platform_chanle_id = False
                    meta_data.set(value, channel_id)
            if create_package_id:
                package_id_node = elementTree.SubElement(application, "meta-data")
                package_id_node.set(name, "3KWAN_PackageID")
                package_id_node.set(value, package_id)

            if create_chanle_id:
                chanle_id_node = elementTree.SubElement(application, "meta-data")
                chanle_id_node.set(name, "3KWAN_ChanleId")
                chanle_id_node.set(value, package_chanle_dict[package_id])

            if create_platform_chanle_id:
                platform_id_node = elementTree.SubElement(application, "meta-data")
                platform_id_node.set(name, "3KWAN_Platform_ChanleId")
                platform_id_node.set(value, channel_id)

        tree.write(manifest_path, "utf-8")
        return True
    except Exception as e:
        Flog.i("handle_v2_common_params() error " + str(e))
        return False


def handle_v2_origin() -> bool:
    if del_smali_code() and delete_so_file() and del_3k_res() and del_manifest_infos(FPath.DECOMPILE_PATH):
        del_system_label('$')
        del_system_label('ic_launcher_foreground')
        del_system_label('ic_launcher_background')
        fio.del_file_folder(FPath.DECOMPILE_PATH + "/res/mipmap-anydpi-v26")
        fio.del_file_folder(FPath.DECOMPILE_PATH + "/res/drawable-v24")
        Flog.i("handle_v2_origin() success")
        return True
    else:
        Flog.i("handle_v2_origin() error")
        return False
