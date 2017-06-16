#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/4
"""
用户类模块
"""
from core.base import Base
from lib import public


class User(Base):
    """用户类"""
    def __init__(self):
        self.id = public.creat_id()
        self.username = None
        self.password = None
