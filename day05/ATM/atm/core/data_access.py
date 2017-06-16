#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
"""
数据访问层模块，处理所有数据访问内容
"""
import json
import os
import time
from conf import settings


def get_info_file(username, dbpath = settings.DATABASE["dbpath"]):
    """
    文件访问用户信息函数
    :param username: 用户名
    :return: 返回用户账号信息
    """
    user_file = os.path.join(dbpath, "%s.json" % username)
    if os.path.isfile(user_file):
        user_dict = json.load(open(user_file, "r", encoding="utf-8"))
        return user_dict
    else:
        return


def get_info_mysql(username):
    pass  # todo


def dump_info_file(user_dict, dbpath = settings.DATABASE["dbpath"]):
    """
    文件存储用户信息函数
    :param user_dict: 用户信息
    :return: 返回完成情况
    """
    user_file = os.path.join(dbpath, "%s.json" % user_dict["username"])
    json.dump(user_dict, open(user_file, "w", encoding="utf-8"))
    return "done"


def dump_info_mysql(user_dict):
    pass  # todo


def get_file(where):
    """
    获取文件内容函数
    :param where: 文件地址
    :return: 返回文件内容
    """
    if os.path.isfile(where):
        file = json.load(open(where, "r", encoding="utf-8"))
        return file
    else:
        return


def dump_file(obj, where):
    """
    存储文件内容函数
    :param obj: 存储对象
    :param where: 存储文件地址
    :return:
    """
    json.dump(obj, open(where, "w", encoding="utf-8"))
    return "done"


def read_file(where, start_time, end_time):
    """
    读取报告相应的内容
    :param where: 报告存储路径
    :param start_time: 查询的起始日期
    :param end_time: 查询的终止日期
    :return:
    """
    tmp_list = []
    start_timestamp = time.mktime(time.strptime(start_time, "%Y-%m-%d"))  # 起始日期时间戳
    end_timestamp = time.mktime(time.strptime(end_time, "%Y-%m-%d"))  # 终止日期时间戳
    with open(where, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                return
            date, trade_type, money, interest, balance = line.split(" ")
            date_timestamp = time.mktime(time.strptime(date, "%Y-%m-%d&%H:%M:%S"))
            # 如果报告日期在所选日期范围内，则回添加到临时列表里
            if dstart_timestamp <= date_timestamp <= end_timestamp:
                tmp_list.append([])
                tmp_list[-1].extend([date.replace("&", " "), trade_type, money, interest, balance])
            else:
                continue
    return tmp_list


def write_file(what, where):
    """
    写入文件函数
    :param what: 写入的内容
    :param where: 写入的路径
    :return:
    """
    if os.path.isfile(where):
        with open(where, "a", encoding="utf-8") as f:
            f.write("%s\n" % what)
    else:
        f = open(where, "w", encoding="utf-8")
        f.close()
