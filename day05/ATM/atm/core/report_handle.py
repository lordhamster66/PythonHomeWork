#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
import os
from conf import settings
from core import data_access

# 获取报告的存储路径
report_path = settings.REPORT_PATH


def create_report(user_dict, what, **kwargs):
    """
    报告生成函数
    :param user_dict: 用户信息
    :param what: 报告内容
    :param kwargs: 拓展参数
    :return:
    """
    username = user_dict["username"]
    report_file_path = os.path.join(report_path, "%s.rp" % username)
    data_access.write_file(what, report_file_path)


def check_report(user_dict, start_time, end_time, **kwargs):
    """
    读取报告函数
    :param user_dict: 用户信息
    :param start_time: 查询的起始日期
    :param end_time: 查询的终止日期
    :param kwargs: 拓展参数
    :return:
    """
    username = user_dict["username"]
    report_file_path = os.path.join(report_path, "%s.rp" % username)
    return data_access.read_file(report_file_path, start_time, end_time)


