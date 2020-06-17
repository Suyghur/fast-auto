# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-03-04.
# Copyright (c) 2020 3KWan.
# Description :
import os
import sys

from fastapi import FastAPI


app = FastAPI()


if __name__ == "__main__":
    root_path = os.getcwd()
    sys.path.append(root_path)
    import fcore.impl_manager

    # import fcore.util.flog
    # import fcore.entity.result

    impl = fcore.impl_manager.ImplManager()
    # fcore.util.flog.Flog.init(os.getcwd() + "/config.json")
    task = impl.get_task()
    if task is not None:
        impl.execute(task)
