# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-10-21.
# Copyright (c) 2019 3KWan.
# Description :
import os
import shutil

from fcore.base.util import fprop
from fcore.base.util import fio
from fcore.base.util.flog import Flog
from fcore.base.util.path import FPath
from fcore.base.util.string import is_empty

try:
    import xml.etree.cElementTree as elementTree
except ImportError:
    import xml.etree.ElementTree as elementTree


def handle_origin_res() -> bool:
    try:
        files = []
        fio.list_file(FPath.DECOMPILE_PATH + "/res", files)
        for file in files:
            if "authsdk_" in file and os.path.exists(file):
                os.remove(file)
            if "umcsdk_" in file and os.path.exists(file):
                os.remove(file)
            if "kkk_" in file and os.path.exists(file):
                os.remove(file)

        xml_list = ["colors", "dimens", "ids", "public", "strings", "styles"]
        for f in xml_list:
            xml_path = FPath.DECOMPILE_PATH + "/res/values/" + f + ".xml"

            if os.path.exists(xml_path):
                tree = elementTree.parse(xml_path)
                root = tree.getroot()
                for node in list(root):
                    attrib_name = node.attrib.get('name')
                    if attrib_name is None:
                        continue
                    if attrib_name.lower().startswith("authsdk_"):
                        root.remove(node)
                    if attrib_name.lower().startswith("kkk_"):
                        root.remove(node)
                tree.write(xml_path, "UTF-8")

        return True
    except Exception as e:
        Flog.i("handle_origin_res() error " + str(e))
    return False


def handle_origin_assets() -> bool:
    avenger_local = "avenger_local_local.properties"
    avenger_plugins = "avenger_plugins_config.xml"
    fuse_cfg = "fuse_cfg.properties"
    try:
        if os.path.exists(FPath.DECOMPILE_PATH + "/assets/" + avenger_local):
            os.remove(FPath.DECOMPILE_PATH + "/assets/" + avenger_local)
        if os.path.exists(FPath.DECOMPILE_PATH + "/assets/" + avenger_plugins):
            os.remove(FPath.DECOMPILE_PATH + "/assets/" + avenger_plugins)

        if os.path.exists(FPath.DECOMPILE_PATH + "/assets/" + fuse_cfg):
            os.remove(FPath.DECOMPILE_PATH + "/assets/" + fuse_cfg)

        if os.path.exists(FPath.DECOMPILE_PATH + "/assets/kkk_fuse"):
            shutil.rmtree(FPath.DECOMPILE_PATH + "/assets/kkk_fuse")

        return True
    except Exception as e:
        Flog.i("handle_origin_assets() error " + str(e))
    return False


def handle_smali() -> bool:
    try:
        if os.path.exists(FPath.DECOMPILE_PATH + "/smali/com/didi"):
            shutil.rmtree(FPath.DECOMPILE_PATH + "/smali/com/didi")
        if os.path.exists(FPath.DECOMPILE_PATH + "/smali/com/tencent"):
            shutil.rmtree(FPath.DECOMPILE_PATH + "/smali/com/tencent")
        if os.path.exists(FPath.DECOMPILE_PATH + "/smali/cn/impl"):
            shutil.rmtree(FPath.DECOMPILE_PATH + "/smali/cn/impl")
        if os.path.exists(FPath.DECOMPILE_PATH + "/smali/cn/kkk"):
            shutil.rmtree(FPath.DECOMPILE_PATH + "/smali/cn/kkk")
        return True
    except Exception as e:
        Flog.i("handle_smali() error " + str(e))
    return False


def handle_v3_common_params(channel_id: str, package_id: str, new_mode: bool = False):
    if new_mode:
        fuse_prop_file = FPath.WORKSPACE_PATH + "/fuse_cfg.properties"
    else:
        fuse_prop_file = FPath.DECOMPILE_PATH + "/assets/fuse_cfg.properties"
    if not os.path.exists(fuse_prop_file):
        Flog.i("fuse_cfg.properties not exists")
        return False
    try:
        prop = fprop.parse(fuse_prop_file)
        # 写入融合渠道id
        if is_empty(channel_id):
            Flog.i("channel_id 不能为空")
            return False
        else:
            prop.put("3KWAN_Platform_ChanleId", channel_id)
        # 写入融合渠道id
        if is_empty(package_id):
            Flog.i("package_id 不能为空")
            return False
        else:
            prop.put("3KWAN_PackageID", package_id)
        prop.save()
        return True
    except Exception as e:
        Flog.i("handle_v3_common_params() error " + str(e))
        return False


def handle_v3_origin() -> bool:
    if handle_origin_assets() and handle_origin_res() and handle_smali():
        Flog.i("handle_v3_origin() success")
        return True
    else:
        Flog.i("handle_v3_origin() error")
        return False
