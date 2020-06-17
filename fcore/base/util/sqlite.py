# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-03-05.
# Copyright (c) 2020 3KWan.
# Description :
import sqlite3

from fcore.base.util.flog import Flog


class Sqlite:

    def __init__(self, path: str):
        self.__conn = sqlite3.connect(path)
        self.__cur = self.__conn.cursor()

    def close(self):
        """
        关闭数据库
        """
        self.__cur.close()
        self.__conn.close()

    def execute(self, sql: str, param=None) -> bool:
        """
        执行数据库的增、删、改
        @param sql：sql语句
        @param param：数据，可以是list或tuple，亦可是None
        @return 成功返回True
        """
        try:
            if param is None:
                self.__cur.execute(sql)
            else:
                if type(param) is list:
                    self.__cur.executemany(sql, param)
                else:
                    self.__cur.execute(sql, param)
            count = self.__conn.total_changes
            self.__conn.commit()
        except Exception as e:
            Flog.i(str(e))
            return False
        if count > 0:
            return True
        else:
            return False

    def query(self, sql, param=None):
        """
        查询语句
        @param sql：sql语句
        @param param：参数,可为None
        @return：成功返回True
        """
        if param is None:
            self.__cur.execute(sql)
        else:
            self.__cur.execute(sql, param)
        return self.__cur.fetchall()
