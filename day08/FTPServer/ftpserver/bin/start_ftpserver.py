#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/29
import os
import sys
import socketserver
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from core.ftp_server import MyTCPHandler
from conf import settings
# from core.manager import Manager

if __name__ == '__main__':
    # obj = Manager()
    # ret = obj.enroll("灵虚至尊", "123")
    # print(ret)
    server = socketserver.ThreadingTCPServer((settings.HOST, settings.PORT), MyTCPHandler)
    print("\033[32;1m服务器已启动！\033[0m")
    server.serve_forever()


