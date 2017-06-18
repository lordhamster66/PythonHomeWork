#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/18
"""启动模块"""
import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from core.rpc_server import RpcServer


if __name__ == '__main__':
    MyRpcServer = RpcServer("server2")  # 输入的参数为服务器对应的RPC队列
    MyRpcServer.start()
