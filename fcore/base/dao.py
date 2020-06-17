# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-03-05.
# Copyright (c) 2020 3KWan.
# Description :
from fcore.base import switch
from fcore.base.util.path import FPath
from fcore.base.util.sqlite import Sqlite


def get_common_sdk_md5(version: str) -> str:
    if switch.DB_ENABLE:
        sql = Sqlite(FPath.ASSETS_PATH + "/db/info.sqlite")
        sql_line = "SELECT MD5 FROM COMMON WHERE VERSION=?;"
        md5_list = sql.query(sql_line, (version,))
        sql.close()
        if md5_list:
            return md5_list[0][0]
    return ""


def get_common_sdk_size(version: str) -> int:
    if switch.DB_ENABLE:
        sql = Sqlite(FPath.ASSETS_PATH + "/db/info.sqlite")
        sql_line = "SELECT SIZE FROM COMMON WHERE VERSION = ?;"
        size_list = sql.query(sql_line, (version,))
        sql.close()
        if size_list:
            return size_list[0][0]
    return 0


def get_channel_sdk_md5(channel_name: str, version: str) -> str:
    if switch.DB_ENABLE:
        sql = Sqlite(FPath.ASSETS_PATH + "/db/info.sqlite")
        sql_line = "SELECT MD5 FROM CHANNEL WHERE NAME=? AND VERSION=?;"
        size_list = sql.query(sql_line, (channel_name, version))
        sql.close()
        if size_list:
            return size_list[0][0]
    return ""


def get_channel_sdk_size(channel_name: str, version: str) -> int:
    if switch.DB_ENABLE:
        sql = Sqlite(FPath.ASSETS_PATH + "/db/info.sqlite")
        sql_line = "SELECT SIZE FROM CHANNEL WHERE NAME=? AND VERSION=?;"
        size_list = sql.query(sql_line, (channel_name, version))
        sql.close()
        if size_list:
            return size_list[0][0]
    return 0


def get_origin_bag_md5(game_id: str, group_id: str) -> str:
    if switch.DB_ENABLE:
        sql = Sqlite(FPath.ASSETS_PATH + "/db/info.sqlite")
        sql_line = "SELECT MD5 FROM BAG WHERE GAME_ID=? AND GROUP_ID=?;"
        md5_list = sql.query(sql_line, (game_id, group_id))
        sql.close()
        if md5_list:
            return md5_list[0][0]
    return ""


def insert_common_sdk_md5(version: str, md5: str, file_size: int) -> bool:
    if switch.DB_ENABLE:
        sql = Sqlite(FPath.ASSETS_PATH + "/db/info.sqlite")
        sql_line = "INSERT INTO COMMON (VERSION,MD5,SIZE) VALUES (?,?,?);"
        result = sql.execute(sql_line, (version, md5, file_size))
        sql.close()
        return result
    else:
        return True


def insert_channel_sdk_md5(channel_name: str, version: str, md5: str, file_size: int) -> bool:
    if switch.DB_ENABLE:
        sql = Sqlite(FPath.ASSETS_PATH + "/db/info.sqlite")
        sql_line = "INSERT INTO CHANNEL (NAME,VERSION,MD5,SIZE) VALUES (?,?,?,?);"
        result = sql.execute(sql_line, (channel_name, version, md5, file_size))
        sql.close()
        return result
    else:
        return True


def insert_origin_bag_md5(game_id: str, group_id: str, md5: str) -> bool:
    if switch.DB_ENABLE:
        sql = Sqlite(FPath.ASSETS_PATH + "/db/info.sqlite")
        sql_line = "INSERT INTO BAG (GAME_ID,GROUP_ID,MD5) VALUES (?,?,?);"
        result = sql.execute(sql_line, (game_id, group_id, md5))
        sql.close()
        return result
    return True


def update_common_sdk_md5(version: str, md5: str, file_size: int) -> bool:
    if switch.DB_ENABLE:
        sql = Sqlite(FPath.ASSETS_PATH + "/db/info.sqlite")
        sql_line = "UPDATE COMMON SET MD5= '" + md5 + "', SIZE = " + str(file_size) + " WHERE VERSION=?;"
        result = sql.execute(sql_line, (version,))
        sql.close()
        return result
    else:
        return True


def update_channel_sdk_md5(channel_name: str, version: str, md5: str, file_size: int) -> bool:
    if switch.DB_ENABLE:
        sql = Sqlite(FPath.ASSETS_PATH + "/db/info.sqlite")
        sql_line = "UPDATE CHANNEL SET MD5='" + md5 + "', SIZE = " + str(file_size) + " WHERE NAME=? AND VERSION=?;"
        result = sql.execute(sql_line, (channel_name, version))
        sql.close()
        return result
    else:
        return True


def update_origin_bag_md5(game_id: str, group_id: str, md5: str) -> bool:
    if switch.DB_ENABLE:
        sql = Sqlite(FPath.ASSETS_PATH + "/db/info.sqlite")
        sql_line = "UPDATE BAG SET MD5= '" + md5 + "' WHERE GAME_ID=? AND GROUP_ID=?;"
        result = sql.execute(sql_line, (game_id, group_id))
        sql.close()
        return result
    else:
        return True
