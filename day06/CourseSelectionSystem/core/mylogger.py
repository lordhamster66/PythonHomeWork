#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/7

"""
日志处理模块，所有日志处理均调用该模块
"""
import os
from conf import settings
import logging


def mylogger(log_type):
    """ 日志处理类 """
    # 创建一个log对象
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL["global_level"])

    # 创建一个屏幕输出handler
    ch = logging.StreamHandler()
    ch.setLevel(settings.LOG_LEVEL["ch_level"])

    # 创建一个文件输出handler
    log_file_path = os.path.join(settings.BASE_DIR, "log", settings.LOG_TYPE[log_type])
    fh = logging.FileHandler(log_file_path, encoding="utf-8")
    fh.setLevel(settings.LOG_LEVEL["fh_level"])

    # 设置输出格式
    ch_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                                     , datefmt='%m/%d/%Y %I:%M:%S %p')
    fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(lineno)d:  %(message)s')

    # 绑定输出格式
    ch.setFormatter(ch_formatter)
    fh.setFormatter(fh_formatter)

    # 绑定handler
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
