#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/4
"""
执行此文件则开始运行整个程序
"""
import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from core import main

if __name__ == '__main__':
    h = main.Haproxy()
    h.start()
