#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/4
"""
基础类模块,一些用户或者管理员类需要继承该类
"""
import pickle
import os
import hashlib
from conf import settings


class Base(object):
    """基础功能类"""
    def save(self):
        """存储对象功能"""
        classname = self.__class__.__name__
        obj_dir = settings.CLASSNAME_TO_DIR[classname]
        obj_path = os.path.join(obj_dir, self.id)
        pickle.dump(self, open(obj_path, "wb"))

    @classmethod
    def get_all_obj(cls):
        """获取所有对象功能"""
        classname = cls.__name__
        obj_dir = settings.CLASSNAME_TO_DIR[classname]
        obj_list = []
        for obj_name in os.listdir(obj_dir):
            obj_path = os.path.join(obj_dir, obj_name)
            obj = pickle.load(open(obj_path, "rb"))
            obj_list.append(obj)
        return obj_list

    def enroll(self, logger):
        """注册功能"""
        obj_list = self.get_all_obj()  # 获取该类的所有对象
        obj_username_list = []  # 对象用户名列表
        for obj in obj_list:
            obj_username_list.append(obj.username)
        while True:
            md5 = hashlib.md5()  # 一个md5对象
            username = input("请输入用户名:").strip()
            password = input("请输入密码:").strip()
            if len(username) == 0 or len(password) == 0:
                continue
            md5.update(password.encode())
            password = md5.hexdigest()
            if username in obj_username_list:
                print("\033[31;1m用户名已存在\033[0m")
                continue
            self.username = username
            self.password = password
            break
        self.save()
        logger.info("%s注册了该系统！" % username)

    @classmethod
    def login(cls, logger):
        """登陆功能"""
        obj_list = cls.get_all_obj()
        count = 0
        while count < 3:
            md5 = hashlib.md5()  # 一个md5对象
            username = input("用户名:").strip()
            password = input("密码:").strip()
            if len(username) == 0 or len(password) == 0:
                continue
            md5.update(password.encode())
            password = md5.hexdigest()
            for obj in obj_list:
                if username == obj.username and password == obj.password:
                    print("\033[32;1m登陆成功！\033[0m")
                    logger.info("%s登陆了该系统！" % username)
                    status = "done"
                    login_obj = obj
                    return {"status": status, "obj": login_obj}
            print("\033[31;1m用户名或密码错误！\033[0m")
            count += 1
        else:
            print("\033[31;1m您已尝试太多次了，请下次再试！\033[0m")
            exit()
