# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-06-16.
# Copyright (c) 2020 3KWan.
# Description :
from flask import Flask
from flask_caching import Cache

cache = Cache()


def init_cache(app: Flask) -> None:
    app.config['CACHE_TYPE'] = 'simple'
    # 默认过期时间 5分钟
    app.config['CACHE_DEFAULT_TIMEOUT'] = 60 * 60
    cache.init_app(app)
