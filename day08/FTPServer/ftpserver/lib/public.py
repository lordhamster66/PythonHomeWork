#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/29
"""公共函数模块"""
import uuid


def create_id():
    """
    创建身份标识函数
    :return:返回唯一标识
    """
    return str(uuid.uuid1())


if __name__ == '__main__':
    print(create_id())
    print(create_id())
    print(create_id())
