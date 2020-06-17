# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-03-13.
# Copyright (c) 2020 3KWan.
# Description :
import os

from fcore.base.util.flog import Flog
from fcore.base.util.path import FPath

try:
    import xml.etree.cElementTree as elementTree
except ImportError:
    import xml.etree.ElementTree as elementTree

android_ns = "http://schemas.android.com/apk/res/android"


def replace_package_name(new_package_name) -> str:
    """
    替换AndroidManifest.xml中的package,补全缺省的activity、service、provider和receiver写法
    :param new_package_name:
    :return:old_package_name
    """
    manifest = FPath.DECOMPILE_PATH + "/AndroidManifest.xml"
    elementTree.register_namespace("android", android_ns)
    tree = elementTree.parse(manifest)
    root = tree.getroot()
    old_package_name = root.attrib.get("package")

    compile_sdk_version = "{" + android_ns + "}compileSdkVersion"
    compile_sdk_version_code_name = "{" + android_ns + "}compileSdkVersionCodename"
    name = "{" + android_ns + "}name"

    # 删除compileSdkVersion和compileSdkVersionCodename
    if compile_sdk_version in root.attrib:
        del root.attrib[compile_sdk_version]

    if compile_sdk_version_code_name in root.attrib:
        del root.attrib[compile_sdk_version_code_name]
    application = root.find(".//application")
    if application is not None:
        activity_list = root.find(".//application").findall("activity")
        service_list = root.find(".//application").findall("service")
        receiver_list = root.find(".//application").findall("receiver")
        provider_list = root.find(".//application").findall("provider")

        # handle activity
        if activity_list is not None and len(activity_list) > 0:
            for activity in activity_list:
                activity_name = activity.get(name)
                if activity_name[0:1] == ".":
                    activity_name = old_package_name + activity_name
                elif activity_name.find(".") == -1:
                    activity_name = old_package_name + "." + activity_name
                activity.set(name, activity_name)

                # 查找intent-filter的action是否需要替换
                intent_filters = activity.findall("intent-filter")
                if intent_filters is None or len(intent_filters) <= 0:
                    continue
                for intent_filter in intent_filters:
                    actions = intent_filter.findall("action")
                    if actions is None or len(actions) <= 0:
                        continue

                    for action in actions:
                        action_name = action.attrib[name]
                        if action_name == old_package_name:
                            action.set(name, new_package_name)
                        # 融合sdk游戏Activity的标记
                        elif action_name == old_package_name + ".MAIN":
                            action.set(name, new_package_name + ".MAIN")

        # handle service
        if service_list is not None and len(service_list) > 0:
            for service in service_list:
                service_name = service.get(name)
                if service_name[0:1] == ".":
                    service_name = old_package_name + service_name
                elif service_name.find(".") == -1:
                    service_name = old_package_name + "." + service_name
                service.set(name, service_name)

        # handle receiver
        if receiver_list is not None and len(receiver_list) > 0:
            for receiver in receiver_list:
                receiver_name = receiver.get(name)
                if receiver_name[0:1] == '.':
                    receiver_name = old_package_name + receiver_name
                elif receiver_name.find('.') == -1:
                    receiver_name = old_package_name + '.' + receiver_name
                receiver.set(name, receiver_name)

        # handle provider
        if provider_list is not None and len(provider_list) > 0:
            for provider in provider_list:
                provider_name = provider.get(name)
                if provider_name[0:1] == ".":
                    provider_name = old_package_name + provider_name
                elif provider_name.find(".") == -1:
                    provider_name = old_package_name + '.' + provider_name
                provider.set(name, provider_name)

    root.set("package", new_package_name)
    tree.write(manifest, "UTF-8")
    return old_package_name


def merge_manifest(target_manifest, sdk_manifest):
    """
    Merge comsdk SdkManifest.xml to the apk AndroidManifest.xml
    :param target_manifest:
    :param sdk_manifest:
    :return:
    """
    if not os.path.exists(target_manifest) or not os.path.exists(sdk_manifest):
        Flog.i("the manifest file is not exists.target_manifest:" + target_manifest + ";sdk_manifest:" + sdk_manifest)
        return False

    elementTree.register_namespace("android", android_ns)
    target_tree = elementTree.parse(target_manifest)
    target_root = target_tree.getroot()

    elementTree.register_namespace("android", android_ns)
    sdk_tree = elementTree.parse(sdk_manifest)
    sdk_root = sdk_tree.getroot()

    f = open(target_manifest, encoding="UTF-8", errors="ignore")
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

    target_tree.write(target_manifest, "UTF-8")
    return True


def merge_res_xml(copy_from, copy_to):
    """
    Merge all android res xml
    :param copy_from:
    :param copy_to:
    :return:
    """
    if not os.path.exists(copy_to):
        return False

    ary_xml = ['strings.xml', 'styles.xml', 'colors.xml', 'dimens.xml', 'ids.xml', 'attrs.xml',
               'integers.xml', 'arrays.xml', 'bools.xml', 'drawables.xml', 'values.xml']
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
            val = node.get('name')
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


def do_common_provider(new_package_name):
    provider_paths = FPath.DECOMPILE_PATH + "/res/xml/provider_paths.xml"
    Flog.i("doCommonResXml provider_paths : " + provider_paths)
    if os.path.exists(provider_paths):
        elementTree.register_namespace("android", android_ns)
        tree = elementTree.parse(provider_paths)
        root = tree.getroot()

        external_paths = root.findall("external-path")
        if external_paths is None or len(external_paths) <= 0:
            return

        for child in external_paths:
            name = child.get("name")
            if name == "files_root":
                child.set("path", "Android/data/" + new_package_name + "/")

        tree.write(provider_paths, "UTF-8")


def get_icon_name() -> str:
    """
    从AndroidManifest.xml中获取游戏图标的名称
    :return:
    """
    manifest_file = FPath.DECOMPILE_PATH + "/AndroidManifest.xml"
    elementTree.register_namespace('android', android_ns)
    tree = elementTree.parse(manifest_file)
    root = tree.getroot()

    application_node = root.find("application")
    if application_node is None:
        return "ic_launcher"

    key = "{" + android_ns + "}icon"
    icon_name = application_node.get(key)

    if icon_name is None:
        return "ic_launcher"

    name = ""
    if "/" in icon_name:
        results = icon_name.split("/")
        name = results[1]
    else:
        name = icon_name[10:]
    return name


# 获取是否自动修改横竖屏
def obtain_direction(sdk_dir):
    sdk_manifest = sdk_dir + "/SDKManifest.xml"
    if not os.path.exists(sdk_manifest):
        return "False"

    elementTree.register_namespace("android", android_ns)
    tree = elementTree.parse(sdk_manifest)
    root = tree.getroot()

    application_config_node = root.find("applicationConfig")
    if application_config_node is None:
        return "False"

    is_auto_change_orientation = application_config_node.attrib.get("change_orientation")
    if is_auto_change_orientation is None or is_auto_change_orientation == "":
        return "False"
    else:
        return is_auto_change_orientation
