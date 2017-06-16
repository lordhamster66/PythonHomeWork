#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/4
"""
公共函数模块
"""
import uuid


def creat_id():
    return str(uuid.uuid1())

if __name__ == '__main__':
    print(creat_id())
