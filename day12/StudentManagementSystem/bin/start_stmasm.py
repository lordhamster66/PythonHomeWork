#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/26
"""
学员管理系统启动模块
"""
import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from core.view import main_view

if __name__ == '__main__':
    main_view.main_show()
