#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/4
"""
基础信息配置模块
"""
import os
import logging

# 主路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 用户路径
USER_DIR = os.path.join(BASE_DIR, "db", "user")

# 类名对应存储路径
CLASSNAME_TO_DIR = {
    "User": USER_DIR
}

# 日志路径
LOG_DIR = os.path.join(BASE_DIR, "log")
ACTION_LOGPATH = os.path.join(LOG_DIR, "action.log")

# 设置日志显示级别
LOG_LEVEL = {
    "global_level": logging.INFO,
    "ch_level": logging.WARNING,
    "fh_level": logging.INFO
}

# 私钥地址
RSA_PATH = os.path.join(BASE_DIR, "db", ".ssh", "id_rsa")

# 存储主机信息
HOST_DIR = os.path.join(BASE_DIR, "db", "host")

if __name__ == '__main__':
    print(BASE_DIR)
