#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/29
"""管理员类模块"""
from core.base import BaseClass
from core.idmaker import IdMaker
from core.user import User


class Manager(BaseClass):
    """用户类"""
    def __init__(self):
        self.id = IdMaker("Manager")
        self.username = None
        self.password = None

    def __str__(self):
        return self.username

    def get_user_obj(self, username):
        """获取用户对象"""
        status = 611
        obj = None
        obj_list = User.get_all_obj()  # 通过类名获取该类下的所有对象
        for obj in obj_list:
            if username == obj.username:
                status = 654
                obj = obj
                return {"status": status, "obj": obj}
        return {"status": status, "obj": obj}
