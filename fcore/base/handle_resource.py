# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-03-10.
# Copyright (c) 2020 3KWan.
# Description :


# ------ 处理资源 ------
import os

from fcore.base.util import fio
from fcore.base.util import Flog
from fcore.base.util.path import FPath

try:
    import xml.etree.cElementTree as elementTree
except ImportError:
    import xml.etree.ElementTree as elementTree


def handle_res(sdk_dir: str) -> bool:
    try:
        # merge manifest
        merge_manifest(sdk_dir)
        copy_res(sdk_dir)
        copy_assets(sdk_dir)
        copy_libs(sdk_dir + "/libs", FPath.DECOMPILE_PATH + "/lib")
        return True
    except Exception as e:
        Flog.i(str(e))
        return False


def copy_res(sdk_dir: str) -> None:
    """
    copyRes
    :param sdk_dir:
    :return:
    """
    res_from = sdk_dir + "/res"
    res_to = FPath.DECOMPILE_PATH + "/res"

    if os.path.exists(res_from):
        copy_resource(res_from, res_to)


def copy_assets(sdk_dir: str) -> None:
    assets_from = sdk_dir + "/assets"
    assets_to = FPath.DECOMPILE_PATH + "/assets"

    if os.path.exists(assets_from):
        copy_resource(assets_from, assets_to)


def merge_manifest(sdk_dir: str) -> None:
    """
    merge manifest
    :param sdk_dir:
    :return:
    """
    target_manifest_path = FPath.DECOMPILE_PATH + "/AndroidManifest.xml"
    sdk_manifest_path = sdk_dir + "/SDKManifest.xml"
    if not os.path.exists(target_manifest_path) or not os.path.exists(sdk_manifest_path):
        Flog.i(
            "the manifest file is not exists.target_manifest:" + target_manifest_path + ";sdk_manifest:" + sdk_manifest_path)
        return
    android_ns = "http://schemas.android.com/apk/res/android"
    elementTree.register_namespace("android", android_ns)
    target_tree = elementTree.parse(target_manifest_path)
    target_root = target_tree.getroot()

    elementTree.register_namespace("android", android_ns)
    sdk_tree = elementTree.parse(sdk_manifest_path)
    sdk_root = sdk_tree.getroot()

    f = open(target_manifest_path, encoding="UTF-8", errors="ignore")
    target_content = f.read()
    f.close()

    permission_config_node = sdk_root.find("permissionConfig")
    if permission_config_node is not None and len(permission_config_node) > 0:
        for child in list(permission_config_node):
            key = "{" + android_ns + "}name"
            val = child.get(key)
            if val is not None and len(val) > 0:
                attr_index = target_content.find(val)
                if -1 == attr_index:
                    target_root.append(child)

    # 不需要对application进行处理
    app_config_node = sdk_root.find("applicationConfig")
    app_node = target_root.find("application")
    if app_config_node is not None:
        for child in list(app_config_node):
            app_node.append(child)

    target_tree.write(target_manifest_path, "UTF-8")


def merge_res_xml(copy_from, copy_to) -> bool:
    """
    Merge all android res xml
    :param copy_from:
    :param copy_to:
    :return:
    """
    if not os.path.exists(copy_to):
        return False

    ary_xml = ["strings.xml", "styles.xml", "colors.xml", "dimens.xml", "ids.xml", "attrs.xml",
               "integers.xml", "arrays.xml", "bools.xml", "drawables.xml", "values.xml"]
    basename = os.path.basename(copy_from)

    if basename in ary_xml:
        f = open(copy_to, "r", encoding="UTF-8")
        target_content = f.read()
        f.close()
        from_tree = elementTree.parse(copy_from)
        from_root = from_tree.getroot()
        to_tree = elementTree.parse(copy_to)
        to_root = to_tree.getroot()
        for node in list(from_root):
            val = node.get("name")
            if val is not None and len(val) > 0:
                val_matched = '"' + val + '"'
                attr_index = target_content.find(val_matched)
                if -1 == attr_index:
                    to_root.append(node)
                else:
                    Flog.i("The node " + val + " is already exists in " + basename)

        to_tree.write(copy_to, 'UTF-8')
        return True
    return False


def copy_resource(copy_from: str, copy_to: str):
    """
    copy resource
    :param copy_from:
    :param copy_to:
    :return:
    """
    if not os.path.exists(copy_to):
        os.makedirs(copy_to)

    if os.path.isfile(copy_from) and not merge_res_xml(copy_from, copy_to):
        fio.copy_files(copy_from, copy_to)
        return

    for f in os.listdir(copy_from):
        source_file = os.path.join(copy_from, f)
        target_file = os.path.join(copy_to, f)

        if os.path.isfile(source_file):
            if not os.path.exists(copy_to):
                os.makedirs(copy_to)

            if merge_res_xml(source_file, target_file):
                continue

            if os.path.exists(target_file):
                fio.del_file_folder(target_file)

            dst_file_stream = open(target_file, "wb")
            source_file_stream = open(source_file, "rb")
            dst_file_stream.write(source_file_stream.read())
            dst_file_stream.close()
            source_file_stream.close()

        if os.path.isdir(source_file):
            copy_resource(source_file, target_file)


def copy_libs(src: str, dst: str):
    """
    copy shared libraries
    :param src:
    :param dst:
    :return:
    """
    if not os.path.exists(src):
        return

    if not os.path.exists(dst):
        os.makedirs(dst)

    for f in os.listdir(src):
        source_file = os.path.join(src, f)
        target_file = os.path.join(dst, f)

        if source_file.endswith(".jar"):
            continue

        if os.path.isfile(source_file):
            if not os.path.exists(target_file) or os.path.getsize(target_file) != os.path.getsize(source_file):
                dst_file_stream = open(target_file, "wb")
                source_file_stream = open(source_file, "rb")
                dst_file_stream.write(source_file_stream.read())
                dst_file_stream.close()
                source_file_stream.close()

        if os.path.isdir(source_file):
            copy_libs(source_file, target_file)
# ------ 拷贝资源 ------
