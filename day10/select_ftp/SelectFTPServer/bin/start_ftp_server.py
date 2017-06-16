#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/11
"""开始模块"""
import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from core.select_ftp_server import MYSelectFTP

if __name__ == '__main__':
    select_ftp = MYSelectFTP()
    select_ftp.start()
