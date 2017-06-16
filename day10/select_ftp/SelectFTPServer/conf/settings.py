#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/11
"""
配置模块
"""
import os
import logging

# 主路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 用户对象存储路径
USER_DIR = os.path.join(BASE_DIR, "db", "user")

# 用户目录
USER_DIRECTORY_DIR = os.path.join(BASE_DIR, "home")

# 类名对应路径
CLASS_TO_DIR = {
    "User": USER_DIR
}

# 可注册角色列表
CAN_ENROLL = {"User": "用户"}

# 日志路径
LOG_DIR = os.path.join(BASE_DIR, "log")
ACTION_LOGPATH = os.path.join(LOG_DIR, "action_log.log")

# 设置日志显示级别
LOG_LEVEL = {
    "global_level": logging.INFO,
    "ch_level": logging.WARNING,
    "fh_level": logging.INFO
}

# 设置ip和端口
HOST = "localhost"
PORT = 9000
