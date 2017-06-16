#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/29
"""id类，唯一识别对象"""
import os
import pickle
from conf import settings
from lib.public import create_id


class IdMaker(object):
    """id类"""
    def __init__(self, class_name):
        self.id = create_id()
        self.class_name = class_name

    def __str__(self):
        return self.id

    def get_obj_by_id(self):
        """通过id获取对象"""
        class_to_dir = settings.CLASS_TO_DIR[self.class_name]
        obj_path = os.path.join(class_to_dir, str(self.id))
        obj = pickle.load(open(obj_path, "rb"))
        return obj
