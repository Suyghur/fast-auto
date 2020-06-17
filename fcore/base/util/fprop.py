import os
import re
import tempfile

from fcore.base.util import fio
from fcore.base.util.flog import Flog


class Properties:
    def __init__(self, file_name):
        if os.path.exists(file_name):
            self.properties = dict()
            self.file_name = file_name
            self.append_on_not_exists = True
            try:
                f = open(self.file_name, "r", encoding="utf-8")
                for line in f:
                    line = line.strip()
                    if line.find("=") > 0 and not line.startswith("#"):
                        # print("当前行数内容可用: " + line)
                        strs = line.split("=")
                        # print(strs)
                        self.properties[strs[0].strip()] = strs[1].strip()
                    else:
                        pass
                        # print("当前行数内容不可用:" + line)

            except Exception as e:
                print("parse properties file error-> " + str(e))
            else:
                f.close()
        else:
            print("file %s not found: " % file_name)

    def has_prop_key(self, key: str) -> bool:
        return key in self.properties

    def get(self, key: str, default_value="") -> str:
        if self.has_prop_key(key):
            return self.properties[key]
        return default_value

    def put(self, key: str, value: str, append_on_not_exists=True, auto_save=False):
        """
        新增或者修改

        :param key: key
        :param value: value
        :param append_on_not_exists: 不存在时是否自动添加,默认为true
        :param auto_save: 是否自动保存当前修改,默认为false;如果是,则每次put都会实时写入文件,如果需要频繁操作,不建议设置该值,而应该在调用
        该方法后调用save()来保存
        """
        self.properties[key] = value
        self.append_on_not_exists = append_on_not_exists
        if auto_save:
            self._replace(self.file_name, key, value)

    def delete(self, key: str):
        """
        删除对应key的内容

        :param key:
        """
        if self.has_prop_key(key):
            del self.properties[key]

            tfile = tempfile.TemporaryFile(mode="w+")
            file_name = self.file_name
            if os.path.exists(file_name):
                r_open = open(file_name, 'r', encoding='utf-8')
                from_regex = key + ".*=.*"
                pattern = re.compile(r'' + from_regex)
                print("表达式")
                print(pattern)
                found = None
                for line in r_open:
                    if pattern.search(line) and not line.strip().startswith('#'):
                        found = True
                        print("找到需要替换的内容 " + line)
                        line = ""
                        print("替换内容为空")
                    tfile.writelines(line)

                r_open.close()
                tfile.seek(0)
                content = tfile.read()

                if os.path.exists(file_name):
                    fio.remove_files(file_name)

                w_open = open(file_name, 'w', encoding="utf-8")
                w_open.writelines(content)
                w_open.close()

                tfile.close()

        else:
            Flog.i("delete failed,key %s not found" % key)

    def save(self):
        """
        保存修改至文件
        如果调用put()方法时,auto_save参数传的是true,则无需调用该方法
        """
        # tempfile默认模式是w+b,写入的是byte,需要改成w+ 才能写入字符串
        # 或者也可以不改这个模式,在写入时候转成byte,取出时再传string
        tfile = tempfile.TemporaryFile(mode="w+")
        file_name = self.file_name
        if os.path.exists(file_name):
            r_open = open(file_name, 'r', encoding="utf-8")
            for key in self.properties.keys():
                value = self.properties[key]
                from_regex = key + ".*=.*"
                pattern = re.compile(r'' + from_regex)
                found = None
                for line in r_open:
                    if pattern.search(line) and not line.strip().startswith('#'):
                        found = True
                        save_value = key + "=" + value
                        line = re.sub(from_regex, save_value, line)
                        tfile.writelines(line)
                        break
                    tfile.writelines(line)
                if not found and self.append_on_not_exists:
                    kav = "\n" + key + "=" + str(value)
                    tfile.writelines(kav)

            r_open.close()
            tfile.seek(0)
            content = tfile.read()

            if os.path.exists(file_name):
                fio.remove_files(file_name)

            w_open = open(file_name, 'w', encoding="utf-8")
            w_open.writelines(content)
            w_open.close()

            tfile.close()

        else:
            Flog.i("file %s not found" % file_name)

    def _replace(self, file_name, key: str, value: str):
        # tempfile默认模式是w+b,写入的是byte,需要改成w+ 才能写入字符串
        # 或者也可以不改这个模式,在写入时候转成byte,取出时再传string
        tfile = tempfile.TemporaryFile(mode="w+")
        from_regex = key + ".*=.*"
        if os.path.exists(file_name):
            r_open = open(file_name, 'r', encoding="utf-8")
            pattern = re.compile(r'' + from_regex)
            found = None
            for line in r_open:
                if pattern.search(line) and not line.strip().startswith('#'):
                    found = True
                    save_value = key + "=" + value
                    line = re.sub(from_regex, save_value, line)
                tfile.writelines(line)
            if not found and self.append_on_not_exists:
                kav = "\n" + key + "=" + str(value)
                tfile.writelines(kav)
            r_open.close()
            tfile.seek(0)
            content = tfile.read()

            if os.path.exists(file_name):
                fio.remove_files(file_name)

            w_open = open(file_name, 'w', encoding="utf-8")
            w_open.writelines(content)
            w_open.close()

            tfile.close()

        else:
            Flog.i("file %s not found" % file_name)


def parse(file_name: str):
    return Properties(file_name)
