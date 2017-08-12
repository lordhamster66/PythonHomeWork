#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/8/12
"""
实用工具模块
"""
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def print_err(msg, quit=False):
    """打印错误信息"""
    output = "\033[31;1mError: %s\033[0m" % msg
    if quit:  # quit默认为False,如果传入参数为True，则退出整个程序
        exit(output)
    else:
        print(output)


def yaml_parser(yml_filename):
    """
    load yaml file and return
    :param yml_filename:
    :return:
    """
    # yml_filename = "%s/%s.yml" % (settings.StateFileBaseDir,yml_filename)
    try:
        yaml_file = open(yml_filename, 'r', encoding="utf-8")  # 尝试打开文件句柄
        data = yaml.load(yaml_file)  # 尝试用yaml读取文件句柄
        return data  # 返回yaml解析的结果
    except Exception as e:
        print_err(e)  # 如果出现错误则打印错误信息
