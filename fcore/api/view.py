# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-06-16.
# Copyright (c) 2020 3KWan.
# Description :
import json
import os

from flask import request, send_from_directory, Flask

from fcore.api.task_cache import cache
from fcore.api.task_scheduler import scheduler
from fcore.base.util.cipher import cipher
from fcore.base.util.path import FPath
from fcore.entity.response import handle_request_params, fast_response


def create_view(app: Flask):
    @app.route("/", methods=["post", "get"])
    def index():
        ct = request.args.get("ct")
        ac = request.args.get("ac")
        if ct == "AutoBuild" and ac == "SubmitTask":
            return submit_task()
        else:
            return {"status": 0, 'msg': "Welcome 3KFast-Auto API.", "result": {}}

    @app.route("/favicon.ico")
    def favicon():
        print(FPath.ASSETS_PATH)
        return send_from_directory(os.path.join(FPath.ASSETS_PATH, "static/image"), "favicon.ico",
                                   mimetype="image/vnd.microsoft.icon")

    @app.route("/test")
    def get_cache():
        # if cache.get("cache_task_flag"):
        #     print("aaaaaa")
        # else:
        #     print("bbbbbb")
        return "Welcome 3KFast-Auto API : "


def submit_task():
    p = request.args.get("p")
    ts = request.args.get("ts")
    if handle_request_params(p, ts):
        response = {"status": 0, "msg": "success", "result": {}}
        aes_key = cipher.get_16low_md5(ts + ts[::-1])
        raw = cipher.urldecode(cipher.AesCipher.decrypt(cipher.urldecode(p), aes_key))
        cache.set("cache_json", raw)
        request_params = json.loads(raw)
        print(request_params)
        # 暂停轮询
        # scheduler.pause_job(id="query_task")
    else:
        response = {'status': 400, 'msg': 'p或ts参数异常', 'result': {}}

    return fast_response(response)
