#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/26
"""
配置模块
"""
import os
import logging

# 主路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志路径
LOG_DIR = os.path.join(BASE_DIR, "log")
ACTION_LOGPATH = os.path.join(LOG_DIR, "action_log.log")

# 设置日志显示级别
LOG_LEVEL = {
    "global_level": logging.INFO,
    "ch_level": logging.WARNING,
    "fh_level": logging.INFO
}

# 数据库信息
# "mysql+pymysql://root:dmc19930417@192.168.48.20:3306/test?charset=utf8"
DB_INFO = {
    "db_type": "mysql",
    "db_connect": "pymysql",
    "user": "root",
    "password": "dmc19930417",
    "host": "192.168.146.20",
    "port": 3306,
    "db": "test",
    "charset": "utf8"
}
