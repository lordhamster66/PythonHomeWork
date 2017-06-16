#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
"""
数据交互转接模块，适应各种数据库引擎
"""
from conf import settings
from core import data_access


def get_info_db():
    """
    获取用户信息转接函数
    :return: 返回对应数据访问函数
    """
    if settings.DATABASE["engine"] == "file":
        return data_access.get_info_file
    elif settings.DATABASE["engine"] == "mysql":
        return data_access.get_info_mysql


def dump_info_db():
    """
    存储用户信息转接函数
    :return: 返回对应数据访问函数
    """
    if settings.DATABASE["engine"] == "file":
        return data_access.dump_info_file
    elif settings.DATABASE["engine"] == "mysql":
        return data_access.dump_info_mysql


def get_all_db():
    """
    获取信息转接函数
    :return: 返回对应数据访问函数
    """
    if settings.DATABASE["engine"] == "file":
        return data_access.get_file
    elif settings.DATABASE["engine"] == "mysql":
        return data_access.get_mysql


def dump_all_db():
    """
    存储信息转接函数
    :return: 返回对应数据访问函数
    """
    if settings.DATABASE["engine"] == "file":
        return data_access.dump_file
    elif settings.DATABASE["engine"] == "mysql":
        return data_access.dump_mysql
