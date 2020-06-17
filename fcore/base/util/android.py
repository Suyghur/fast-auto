# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-28.
# Copyright (c) 2020 3KWan.
# Description :
import os

from fcore.base import switch
from fcore.base.util.flog import Flog
from fcore.entity.result import Task
from fcore.base.util import fio, java, command
from fcore.base.util.path import FPath


def use_apktool232(task: Task) -> bool:
    if task.ext and "apktool232" in task.ext:
        if task.ext["apktool232"] == "1":
            return True
    if task.bag_info.group_id in switch.APKTOOL232:
        return True

    return False


def decompile_apk(task: Task) -> bool:
    if use_apktool232(task):
        apktool = FPath.APKTOOL232
    else:
        apktool = FPath.APKTOOL231
    cmd = "%s -jar -Xms2048m -Xmx2048m %s -v d -b -f %s -o %s" % (
        java.get_java_shell(), apktool, FPath.ORIGIN_APK, FPath.DECOMPILE_PATH)
    return command.exec_command(cmd)


def compile_apk(task: Task) -> bool:
    if use_apktool232(task):
        apktool = FPath.APKTOOL232
    else:
        apktool = FPath.APKTOOL231
    if os.path.exists(FPath.COMPILE_PATH):
        cmd = "%s -jar -Xms2048m -Xmx2048m %s -v b -f %s -o %s" % (
            java.get_java_shell(), apktool, FPath.COMPILE_PATH, FPath.OUTPUT_APK)
        return command.exec_command(cmd)
    else:
        return False


def split_dex():
    """
    如果函数上限超过限制，自动拆分smali，以便生成多个dex文件
    """
    smali_path = FPath.DECOMPILE_PATH + "/smali"
    ##interaction multidex in mother apk
    for k in range(2, 20):
        temp_path = FPath.DECOMPILE_PATH + "/smali_classes" + str(k)
        if os.path.exists(temp_path):
            fio.copy_files(temp_path, smali_path)
            fio.del_file_folder(temp_path)
    # if os.path.exists(smali_path + "/android/support/multidex/multiDex.smali"):
    #     multidex_file_path = smali_path + "/android/support/multidex/multiDex.smali"
    # else:
    #     multidex_file_path = smali_path + "/cn/kkk/tools/multidex/multiDex.smali"

    # 将smali的所有文件转移到smali_temp文件夹进行备份
    smali_temp = os.path.join(FPath.DECOMPILE_PATH, "smali_temp")
    if os.path.exists(smali_temp):
        fio.del_file_folder(smali_temp)

    os.makedirs(smali_temp)
    fio.copy_files(smali_path, smali_temp)

    # 然后清空原有的smaliPath
    fio.del_file_folder(smali_path)
    # 创建全新的smaliPath
    if not os.path.exists(smali_path):
        os.makedirs(smali_path)

    # 遍历出smali_temp的所有文件
    all_files = []
    fio.list_file(smali_temp, all_files, [])

    max_func_num = 64000
    total_fuc_num = 0
    curr_dex_index = 1
    all_refs = dict()

    # 优先将带有Application 和 3k融合代码移到smali
    for f in all_files:
        f = f.replace("\\", "/")
        if not f.endswith(".smali"):
            continue

        if "Application" in f or "/cn/kkk/commonsdk" in f or "/cn/impl/common" in f or "/cn/impl/control" in f or "/android/support/multidex" in f \
                or "com/console/game/common/channels" in f or "com/console/game/common/comsdk" in f or "com/consolegame" in f:
            this_fuc_num = get_smali_method_count(f, all_refs)
            total_fuc_num = total_fuc_num + this_fuc_num
            # 将文件移到smali
            target_path = f[0:len(FPath.DECOMPILE_PATH)] + "/smali" + f[len(smali_temp):]
            fio.copy_file(f, target_path)
            # 删除smali_temp文件夹内的对应文件
            fio.del_file_folder(f)

    # # 查询渠道SDK是否有mainlistdex文件,有的话则第二步将此文件内填充的路径添加到主dex(前提是不能超过maxFuncNum)
    # temp_channel_id = task.common_params_obj.common_channel_majia_id
    # if task.common_params_obj.common_channel_majia_id is None or task.common_params_obj.common_channel_majia_id is "":
    #     temp_channel_id = task.common_params_obj.common_channel_id
    # main_listdex_path = os.path.join(workDir, "sdk/" + str(temp_channel_id) + "/mainlistdex.txt")
    # if os.path.exists(main_listdex_path):
    #     f = open(main_listdex_path, "r")
    #     lines = f.readlines()
    #     f.close()
    #
    #     if lines is not None and len(lines) > 0:
    #         for line in lines:
    #             line_path = os.path.join(decompile_dir, "smali_temp", line)
    #             line_path = line_path.replace("\n", "").strip()
    #             if os.path.exists(line_path):
    #                 path_list = []
    #                 file_utils.list_file(line_path, path_list, [])
    #                 for file in path_list:
    #                     if file.endswith(".smali"):  # 当前是smali文件
    #                         smaliFuncNum = smali_utils.get_smali_method_count(file, all_refs)
    #                         if total_fuc_num + smaliFuncNum < max_func_num:
    #                             target_path = line_path[0:len(decompile_dir)] + "/smali" + file[len(smali_temp):]
    #                             file_utils.copy_file(file, target_path)
    #                             # 删除smali_temp文件夹内的对应文件
    #                             file_utils.del_file_folder(file)
    #                             total_fuc_num = total_fuc_num + smaliFuncNum
    #                         else:
    #                             Logger.info(line + "func num add main dex func num has over main dex func num ")
    #                             break

    # 把剩余的smali文件进行划分
    for f in all_files:
        f = f.replace("\\", "/")
        if not f.endswith(".smali"):
            continue

        # 如果之前application和3k common的smali func num 已经超过maxFuncNum
        target_path = None
        this_fuc_num = get_smali_method_count(f, all_refs)
        if total_fuc_num >= max_func_num or (total_fuc_num + this_fuc_num) >= max_func_num:
            # 刷新当前smali_class开始的方法数
            total_fuc_num = this_fuc_num
            # 则应该新建一个smali_class(num)进行存放smali
            curr_dex_index = curr_dex_index + 1
            new_dex_path = os.path.join(FPath.DECOMPILE_PATH, "smali_classes" + str(curr_dex_index))

            if os.path.exists(new_dex_path):
                fio.del_file_folder(new_dex_path)
            os.makedirs(new_dex_path)

            target_path = f[0:len(FPath.DECOMPILE_PATH)] + "/smali_classes" + str(curr_dex_index) + f[len(smali_temp):]
        else:
            total_fuc_num = total_fuc_num + this_fuc_num
            if curr_dex_index > 1:
                target_path = f[0:len(FPath.DECOMPILE_PATH)] + "/smali_classes" + str(curr_dex_index) + f[len(
                    smali_temp):]
            else:
                target_path = f[0:len(FPath.DECOMPILE_PATH)] + "/smali" + f[len(smali_temp):]

        fio.copy_file(f, target_path)
        fio.del_file_folder(f)

    # # 删除smali_temp
    fio.del_file_folder(smali_temp)

    # # 如果渠道sdk存在classes.dex
    # if os.path.exists(ext_smali_dir):
    #     all_files = []
    #     io.list_file(ext_smali_dir, all_files, [])
    #     for f in all_files:
    #         f = f.replace("\\", "/")
    #         if not f.endswith(".smali"):
    #             continue
    #
    #         # 如果之前application和3k common的smali func num 已经超过maxFuncNum
    #         target_path = None
    #         this_fuc_num = get_smali_method_count(f, all_refs)
    #         if total_fuc_num >= max_func_num or (total_fuc_num + this_fuc_num) >= max_func_num:
    #             # 刷新当前smali_class开始的方法数
    #             total_fuc_num = this_fuc_num
    #             # 则应该新建一个smali_class(num)进行存放smali
    #             curr_dex_index = curr_dex_index + 1
    #             new_dex_path = os.path.join(Router.DECOMPILE_PATH, "smali_classes" + str(curr_dex_index))
    #
    #             if os.path.exists(new_dex_path):
    #                 io.del_file_folder(new_dex_path)
    #             os.makedirs(new_dex_path)
    #
    #             target_path = f[0:len(Router.DECOMPILE_PATH)] + "/smali_classes" + str(curr_dex_index) + f[len(ext_smali_dir):]
    #         else:
    #             total_fuc_num = total_fuc_num + this_fuc_num
    #             if curr_dex_index > 1:
    #                 target_path = f[0:len(Router.DECOMPILE_PATH)] + "/smali_classes" + str(curr_dex_index) + f[len(
    #                     ext_smali_dir):]
    #             else:
    #                 target_path = f[0:len(Router.DECOMPILE_PATH)] + "/smali" + f[len(ext_smali_dir):]
    #
    #         io.copy_file(f, target_path)
    #         io.del_file_folder(f)
    #
    #     io.del_file_folder(ext_smali_dir)


def get_smali_method_count(smaliFile, allMethods):
    """
    get smali methods count
    :param smaliFile:
    :param allMethods:
    :return:
    """
    if not os.path.exists(smaliFile):
        return 0

    f = open(smaliFile, encoding='UTF-8', errors='ignore')
    lines = f.readlines()
    f.close()

    if lines is None or len(lines) <= 0:
        return 0

    class_line = lines[0]
    class_line = class_line.strip()
    if not class_line.startswith(".class"):
        Flog.i(smaliFile + " not startswith .class")
        return 0
    class_name = parse_class(class_line)

    count = 0
    for line in lines:
        line = line.strip()

        method = None
        temp_class_name = class_name
        if line.startswith(".method"):
            method = parse_method_default(line)
        elif line.startswith("invoke-"):
            temp_class_name, method = parse_method_invoke(line)

        if method is None:
            continue

        if temp_class_name not in allMethods:
            allMethods[temp_class_name] = list()

        if method not in allMethods[temp_class_name]:
            count = count + 1
            allMethods[temp_class_name].append(method)
        else:
            pass

    return count


def parse_class(line):
    """
    parse class line
    :param line:
    :return:
    """
    if not line.startswith(".class"):
        Flog.i("line parse error. not startswith .class : " + line)
        return None

    blocks = line.split()
    return blocks[len(blocks) - 1]


def parse_method_default(line):
    """
    parse default method
    :param line:
    :return:
    """
    if not line.startswith(".method"):
        Flog.i("the line parse error in parse_method_default:" + line)
        return None

    blocks = line.split()
    return blocks[len(blocks) - 1]


def parse_method_invoke(line):
    if not line.startswith("invoke-"):
        Flog.i("the line parse error in parse_method_invoke:" + line)

    blocks = line.split("->")
    method = blocks[len(blocks) - 1]

    pre_blocks = blocks[0].split(",")
    class_name = pre_blocks[len(pre_blocks) - 1]
    class_name = class_name.strip()

    return class_name, method
