#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/7
"""
公共函数模块
"""
import uuid  # 唯一ID生成库
import time


def create_id():
    """
    创建身份标识函数
    :return:返回唯一标识
    """
    return str(uuid.uuid1())


def login_decorator(status):
    """ 登陆认证装饰器 """
    def true_decorator(func):
        def wrapper(*args, **kwargs):
            if status["status"] == 1:
                return func(*args, **kwargs)
            print("\033[31;1m您没登陆！\033[0m")
            time.sleep(1)
        return wrapper
    return true_decorator


if __name__ == '__main__':
    print(create_id())
    print(create_id())
    print(create_id())

