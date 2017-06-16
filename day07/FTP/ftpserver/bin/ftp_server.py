#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/20
import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from core.ftpserver import FtpServer
from conf import settings

if __name__ == '__main__':
    server = FtpServer()
    server.start()
