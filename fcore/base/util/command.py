# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-28.
# Copyright (c) 2020 3KWan.
# Description :
import importlib
import re
import subprocess
import sys

from fcore.base.util.flog import Flog


def exec_command(cmd) -> bool:
    Flog.i(cmd)
    cmd = cmd.replace('\\', '/')
    cmd = re.sub('/+', '/', cmd)
    try:
        importlib.reload(sys)
        # sys.setdefaultencoding('utf-8')

        s = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = s.communicate()

        # if platform.system() == "Windows":
        #     stdoutput = stdoutput.decode("gbk")
        #     erroutput = erroutput.decode("gbk")

        if s.returncode == 1:
            Flog.i(out.decode("utf-8"))
            Flog.i(err.decode("utf-8"))
            # Logger.error("*********ERROR********", "cmd_utils")
            # Logger.error(stdoutput)
            # Logger.error(erroutput)
            # Logger.error("*********ERROR********", "cmd_utils")
            # shell = "shell error : " + shell + " !!!exec Fail!!! "
            return False
        else:
            # Flog.i(out.decode("utf-8"))
            # Flog.i(err.decode("utf-8"))
            # cmd = cmd + " !!!exec packing!!! "
            # Logger.info(shell, "cmd_utils")
            return True
    except Exception as e:
        Flog.i(str(e))
        return False
