#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/11
"""基类模块，提供基础功能"""
import os
import pickle
import hashlib
from conf import settings


class BaseClass(object):
    """基类，提供基础功能"""
    def save(self):
        class_name = self.__class__.__name__
        class_to_dir = settings.CLASS_TO_DIR[class_name]
        obj_path = os.path.join(class_to_dir, self.id)
        pickle.dump(self, open(obj_path, "wb"))

    @classmethod
    def get_all_obj(cls):
        """
        可以返回一个类生成的所有对象
        :return:
        """
        class_name = cls.__name__
        class_to_dir = settings.CLASS_TO_DIR[class_name]
        obj_list = []
        for file_name in os.listdir(class_to_dir):
            file_path = os.path.join(class_to_dir, file_name)
            obj = pickle.load(open(file_path, "rb"))
            obj_list.append(obj)
        return obj_list

    def enroll(self, username, password, logger):
        """ 注册方法 """
        class_name = self.__class__.__name__
        if class_name in settings.CAN_ENROLL:  # 如过类名在可注册字典里则可以进行注册
            for obj in self.__class__.get_all_obj():  # 通过类名来获取该类生成的所有对象
                if username == obj.username:
                    return 650
            self.username = username
            MD5 = hashlib.md5()
            MD5.update(password.encode())
            password = MD5.hexdigest()
            self.password = password
            self.save()
            logger.info("%s-%s注册了该系统！" % (settings.CAN_ENROLL[class_name], self.username))
            print("\033[31;1m%s-%s注册成功！\033[0m" % (settings.CAN_ENROLL[class_name], self.username))
            return 651
        else:
            return 652

    @classmethod
    def login(cls, username, password, logger):
        status = 653
        obj = None
        class_name = cls.__name__
        if class_name in settings.CAN_ENROLL:  # 如果类名在可注册字典里则其可以进行登陆
            MD5 = hashlib.md5()
            MD5.update(password.encode())
            password = MD5.hexdigest()
            obj_list = cls.get_all_obj()  # 通过类名获取该类下的所有对象
            for obj in obj_list:
                if username == obj.username and password == obj.password:
                    status = 654
                    obj = obj
                    logger.info("%s-%s登陆了该系统！" % (settings.CAN_ENROLL[class_name], obj.username))
                    return {"status": status, "obj": obj}
        else:
            status = 655
            obj = None
            return {"status": status, "obj": obj}
        return {"status": status, "obj": obj}



