#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/7/8
"""
初始化数据库系统
"""
import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)


if __name__ == '__main__':
    from core import mysystem_init
    mysystem_init.run()
    print("初始化数据库成功...")
    print("新建数据成功...")
