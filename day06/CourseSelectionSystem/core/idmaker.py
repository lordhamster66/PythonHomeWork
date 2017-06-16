#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/7
"""
此模块用来创建唯一ID对象
"""
from lib import public  # 导入公共函数模块
from conf import settings           # 导入配置文件
import os
import pickle


class MakeId(object):
    """ 创建身份标识类 """
    def __init__(self, db_path):
        self.id = public.create_id()
        self.db_path = db_path

    def __str__(self):
        return self.id

    def get_obj_by_id(self):
        """
        用ID来获取对象信息
        :return: 返回对象信息
        """
        base_name = os.path.basename(self.db_path)
        file_dir = settings.MATCH_DIR[base_name]
        file_path = os.path.join(file_dir, self.id)
        obj = pickle.load(open(file_path, "rb"))
        return obj

