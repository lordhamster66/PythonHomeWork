#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/29
"""用户类模块"""
import os
from core.base import BaseClass
from core.idmaker import IdMaker
from conf import settings


class User(BaseClass):
    """用户类"""
    def __init__(self):
        self.id = IdMaker("User")
        self.username = None
        self.password = None
        self.quota = 10485760  # 磁盘配额,默认10M
        self.file_put_dict = {}  # 接收文件用

    def __str__(self):
        return self.username

    def create_directory(self):
        """创建用户目录"""
        home_dir = settings.USER_DIRECTORY_DIR
        home_path = os.path.join(home_dir, self.username)
        if os.path.isdir(home_path):
            return
        os.mkdir(home_path)
        return "done"

    @property
    def home_path(self):
        home_dir = settings.USER_DIRECTORY_DIR
        home_path = os.path.join(home_dir, self.username)
        return home_path
