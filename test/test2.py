# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-06-14.
# Copyright (c) 2020 3KWan.
# Description :
import json
#
# from flask import Flask
# from flask_apscheduler import APScheduler
#
import time

import requests

from fcore.base.util.cipher import cipher

#
#
# def init_scheduler():
#     pass
#
#
# class Config:
#     JOBS = [{
#         'id': 'task1',
#         'func': '__main__:exec_task',
#         'trigger': 'interval',
#         'args': (3, 4),
#         'seconds': 1
#     }]
#     print("bbbb")
#
#
# def exec_task(a, b):
#     print("aaaaaa")
#     print(str(a) + str(b))
#
#
# scheduler = APScheduler()
# app = Flask(__name__)
#
# app.config.from_object(Config())
# # init_scheduler()
# scheduler.init_app(app)
# scheduler.start()
# app.run()
#
#
# @app.route('/test')
# def test():
#     print("sleep")
#     return 'test'
#
#
# @app.route('/')
# def index():
#     return 'index'

if __name__ == '__main__':
    # ts = '88bb522c2618e76ede9d7ac605a4eb8f'
    # p = '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'
    # url = "http://127.0.0.1:5050/?ct=AutoBuild&ac=SubmitTask&p=" + p + "&ts=" + ts
    # print(url)
    # print(p)
    # result = requests.post(url, headers={"Connection": "close"}, verify=False, timeout=5)
    # print(result)
    # aes_key = cipher.get_16low_md5(ts + ts[::-1])
    # raw = cipher.urldecode(cipher.AesCipher.decrypt(cipher.urldecode(p), aes_key))
    # request_params = json.loads(raw)
    # print(raw)
    raw = '''{"common":{},"task_entry":{"task_info":{"task_id":"9201","is_majia":0,"is_white_bag":0,"is_debug_bag":0,"has_plugin_sdk":0,"is_h5game":0,"is_auto_build":1},"bag_info":{"group_name":"我的使命","game_orientation":"1","group_id":"20","version_code":"","version_name":"5.1.5","file_name":"originApk/20200316/wdsm_release_wdsma_v515_1584338388.apk","file_url":"http://3kfastapi.3k.com/download/originApk/20200316/wdsm_release_wdsma_v515_1584338388.apk","file_md5":"42199599ed5a119b752020dad7102713","game_id":"203"},"sdk_info":{"common_sdk":{"file_name":"6.1.1_1589854668.zip","version":"6.1.1","file_md5":"73b4b741b067db0046add3e32d10fb91","file_url":"http://3kfast-center-test.3kwan.com/download/rhSdk/20200519/6.1.1_1589854668.zip"},"channel_sdk":{"file_name":"3k_1589507695.zip","version":"4.8.1","file_md5":"a0d0467518292c1420cdd5f547c2a5c2","file_url":"http://3kfast-center-test.3kwan.com/download/channelSdk/20200515/3k_1589507695.zip"},"plugin_sdk":{}},"keystore_info":{"file_md5":"040a8097e0726d991674131d8823db73","keystore_name":"android.keystore","keystore_password":"123456","keystore_alias":"android.keystore","keystore_alias_password":"123456","file_url":"http://3kfastapi.3k.com/download/signatureFile/1561717814/android.keystore"},"script_info":{"common_script":{"file_name":"common_script_1589780548.zip","file_url":"http://3kfast-center-test.3kwan.com/download/rhScript/20200518/common_script_1589780548.zip","file_md5":"712b8998eeee7a3bf7660fcb4dac2508"},"game_script":{"file_name":"game_script_1584970762.zip","file_url":"http://3kfast-center-test.3kwan.com/download/gameScript/20200323/game_script_1584970762.zip","file_md5":"196fe4b15b938aaa11993690a8fbc66c"}},"params_info":{"common_params":{"game_id":"203","package_chanle":{"29250":"29250"},"total":1,"channel_name":"3k","channel_id":"0","deploy_id":"0"},"channel_params":{"3KWAN_AppID":"391","3KWAN_Appkey":"NdwF8TzpbH7cPzFmpnY3h02vK4EXc5re","3KWAN_ChanleId":"8592","3KWAN_PackageID":"","BUGLY_APPID":"6a21a8e6db","3KWAN_DeployID":"0","3KWAN_GAMEID":"203","3KWAN_GAMENAME":"我的使命"},"plugin_params":{},"game_params":{"game_package_name":"com.wdsm.kkkwan","game_name":"我的使命","game_version_code":"515","game_version_name":"5.1.5","game_orientation":"1","game_icon_url":"https://yxfile.3k.com/2019/07/26/upload_gc3biin72w4505vx7w1xvt54w6refz2g.png","game_logo_url":"","game_splash_url":"","game_background_url":"","game_loading_url":"","game_resource_url":""}},"ext":{"xcqy_game_name":"wdsm","wpk_flag":0}},"auto_test":{"bag_url":{},"wx_notify":{"enable":0,"content":"","url":"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ea9e4616-4d92-4a38-acbb-37dfb72b37ef"},"type":1}}'''
    print(json.loads(raw))

    time_stamp = str(int(time.time()))
    raw_key = cipher.get_32low_md5(time_stamp + cipher.get_random_str())
    aes_key = cipher.get_16low_md5(raw_key + raw_key[::-1])
    # p = cipher.urlencode(cipher.AesCipher.encrypt(raw, aes_key))
    p = cipher.urlencode(cipher.AesCipher.encrypt(raw, aes_key))
    ts = raw_key
    url = "http://127.0.0.1:5050/?ct=AutoBuild&ac=SubmitTask"
    enc_url = url + "&p=" + p + "&ts=" + ts
    result = requests.post(enc_url, headers={"Connection": "close"}, verify=False, timeout=5)
    print(result)
    print("logTag " + time_stamp + " : url = " + enc_url)
    # print(raw2)
