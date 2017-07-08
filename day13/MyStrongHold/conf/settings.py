#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/7/8
"""
配置模块
"""
import os

# 主路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 表信息文件主路径
TABLES_DIR = os.path.join(BASE_DIR, "resources", "tables")

# 数据库信息
# "mysql+pymysql://root:dmc19930417@192.168.48.20:3306/test?charset=utf8"
DB_INFO = {
    "db_type": "mysql",
    "db_connect": "pymysql",
    "user": "root",
    "password": "123",
    "host": "192.168.48.20",
    "port": 3306,
    "db": "s1",
    "charset": "utf8"
}
