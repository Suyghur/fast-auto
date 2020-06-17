# -*- coding: utf-8 -*-
# Author:yangtianbiao
# CreateTime:2019/5/7
#
# 此文件用于编写打包脚本的主要逻辑

import os
import os.path
import os.path
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import SubElement

from fcore.base.util.flog import Flog

androidNS = 'http://schemas.android.com/apk/res/android'


def get_super_clz_name(smali_path):
    f = open(smali_path, 'r')
    lines = f.readlines()
    f.close()

    for line in lines:

        if line.strip().startswith('.super'):
            line = line[6:].strip()
            return line[1:-1].replace('/', '.')

    return None


def find_smali_path_by_clz(decompile_dir, clz_name):
    Flog.i("findSmaliPathOfClass: " + clz_name)

    clz_name = clz_name.replace(".", "/")

    for i in range(1, 10):
        smali_path = "smali"
        if i > 1:
            smali_path = smali_path + str(i)

        path = decompile_dir + "/" + smali_path + "/" + clz_name + ".smali"

        Flog.i(path)

        if os.path.exists(path):
            return path

    return None


def find_application_clz(decompile_dir):
    manifest_file = decompile_dir + "/AndroidManifest.xml"
    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}name'

    tree = ET.parse(manifest_file)
    root = tree.getroot()

    application_node = root.find('application')
    if application_node is None:
        return None

    application_class_name = application_node.get(key)

    return application_class_name


def find_root_application_smali(decompileDir):
    application_class_name = find_application_clz(decompileDir)

    if application_class_name is None:
        return None

    return findRootApplicationRecursively(decompileDir, application_class_name)


def findRootApplicationRecursively(decompileDir, applicationClassName):
    smaliPath = find_smali_path_by_clz(decompileDir, applicationClassName)

    if smaliPath is None or not os.path.exists(smaliPath):
        return None

    superClass = get_super_clz_name(smaliPath)
    if superClass is None:
        return None

    if superClass == 'android.app.Application':
        return smaliPath
    else:
        return findRootApplicationRecursively(decompileDir, superClass)


def modifyRootApplicationExtends(decompileDir, applicationClassName):
    applicationSmali = find_root_application_smali(decompileDir)
    if applicationSmali is None:
        Flog.i("the applicationSmali get failed.")
        return

    Flog.i("modifyRootApplicationExtends: root application smali: " + applicationSmali)

    modifyApplicationExtends(applicationSmali, applicationClassName)


# 将Application改为继承指定的applicationClassName
def modifyApplicationExtends(applicationSmaliPath, applicationClassName):
    Flog.i("modify Application extends " + applicationSmaliPath + "; " + applicationClassName)

    applicationClassName = applicationClassName.replace(".", "/")

    f = open(applicationSmaliPath, 'r')
    lines = f.readlines()
    f.close()

    result = ""
    for line in lines:

        if line.strip().startswith('.super'):
            result = result + '\n' + '.super L' + applicationClassName + ';\n'
        elif line.strip().startswith('invoke-direct') and 'android/app/Application;-><init>' in line:
            result = result + '\n' + '      invoke-direct {p0}, L' + applicationClassName + ';-><init>()V'
        elif line.strip().startswith('invoke-super'):
            if 'attachBaseContext' in line:
                result = result + '\n' + '      invoke-super {p0, p1}, L' + applicationClassName + ';->attachBaseContext(Landroid/content/Context;)V'
            elif 'onConfigurationChanged' in line:
                result = result + '\n' + '      invoke-super {p0, p1}, L' + applicationClassName + ';->onConfigurationChanged(Landroid/content/res/Configuration;)V'
            elif 'onCreate' in line:
                result = result + '\n' + '      invoke-super {p0}, L' + applicationClassName + ';->onCreate()V'
            elif 'onTerminate' in line:
                result = result + '\n' + '      invoke-super {p0}, L' + applicationClassName + ';->onTerminate()V'
            else:
                result = result + line

        else:
            result = result + line

    f = open(applicationSmaliPath, 'w')
    f.write(result)
    f.close()

    return 0


# 删除AndroidManifest.xml中指定的组件，比如activity,service,provider等
# typeName:组件类型， 比如activity,service,provider,receiver
# name：组件名称， 比如com.3k.comsdk.UniLoginActivity
def removeMinifestComponentByName(decompileDir, typeName, componentName):
    manifestFile = decompileDir + "/AndroidManifest.xml"
    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}name'

    tree = ET.parse(manifestFile)
    root = tree.getroot()

    applicationNode = root.find('application')
    if applicationNode is None:
        return

    activityNodeLst = applicationNode.findall(typeName)
    if activityNodeLst is None:
        return

    for activityNode in activityNodeLst:

        name = activityNode.get(key)
        if name == componentName:
            applicationNode.remove(activityNode)
            break

    tree.write(manifestFile, 'UTF-8')
    Flog.i("remove " + componentName + " from AndroidManifest.xml")

    return componentName


# 将指定java文件中的类的package值给修改为指定的值
def replaceJavaPackage(javaFile, newPackageName):
    if not os.path.exists(javaFile):
        Flog.i("getJavaPackage failed. java file is not exists." + javaFile)
        return 1

    f = open(javaFile, 'r')
    lines = f.readlines()
    f.close()

    content = ""
    for l in lines:
        c = l.strip()
        if c.startswith('package'):
            content = content + 'package ' + newPackageName + ';\r\n'
        else:
            content = content + l

    f = open(javaFile, 'wb')
    f.write(content)
    f.close()

    return 0


# 修改或者替换meta-data  目前只是替换application节点下面的meta-data
def handle_meta_data(tree, meta_data_key, meta_data_value):
    name = "{" + androidNS + "}name"
    value = "{" + androidNS + "}value"
    root = tree.getroot()
    #
    # application_node = root.find("application")
    # if application_node is None:
    #     Logger.error("application node is not exists in AndroidManifest.xml")
    #     return

    b_found = False
    meta_datas = root.find(".//application").findall("meta-data")

    if meta_datas is not None:
        for meta_data in meta_datas:
            if meta_data.get(name) == meta_data_key:
                b_found = True
                meta_data.set(value, str(meta_data_value))
                break

    if not b_found:
        meta_node = SubElement(root.find(".//application"), "meta-data")
        meta_node.set(name, meta_data_key)
        meta_node.set(value, str(meta_data_value))
