#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/7/8
"""
启动堡垒机
"""
import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)


if __name__ == '__main__':
    from core import interactive
    interactive.run()

