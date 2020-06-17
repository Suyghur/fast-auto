# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-06-15.
# Copyright (c) 2020 3KWan.
# Description :

from flask import Flask

from fcore.api import task_scheduler, task_cache
from fcore.base.util.flog import Flog
from fcore.entity.response import JSONResponse
from fcore.impl_manager import ImplManager


def create_app() -> Flask:
    app = Flask(__name__)

    app.response_class = JSONResponse
    impl = ImplManager()
    Flog.init()

    task_cache.init_cache(app)
    task_scheduler.init_scheduler(app, impl)

    return app
