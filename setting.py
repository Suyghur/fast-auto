# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-06-15.
# Copyright (c) 2020 3KWan.
# Description :

import multiprocessing

debug = False
# 监听内网端口5000
bind = '0.0.0.0:5050'
workers = 1
backlog = 2048
threads = (2 * multiprocessing.cpu_count()) + 1
loglevel = 'debug'
keepalive = 10
# 超时
timeout = 60
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# 工作模式协程。使用gevent模式，还可以使用sync模式，默认的是sync模式
# worker_class = 'gevent'
# #worker_connections最大客户端并发数量，默认情况下这个值为1000。此设置将影响gevent和eventlet工作模式
worker_connections = 2000
# 值是一个整数或者0，当该值为0时，表示将对请求头大小不做限制
limit_request_field_size = 0
# HTTP请求行的最大大小，此参数用于限制HTTP请求行的允许大小，默认情况下，这个值为4094。
# 值是0~8190的数字。此参数可以防止任何DDOS攻击
limit_request_line = 0
