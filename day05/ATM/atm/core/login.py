#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
"""
登陆认证模块
"""

from core import db_handler
from core.mylogger import Mylogger  # 自定义日志模块
import time

action_logger = Mylogger("action")  # 行为日志


def islogin(func):
    """
    用户认证装饰器
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        if args[0].get("islogin"):
            return func(*args, **kwargs)
        else:
            exit("\033[31;1m请重新登陆!\033[0m")
    return wrapper


def login_check(*args):
    """
    登陆验证函数
    :return: 验证成功，返回用户账号信息
    """
    count = 0
    while count < 3:
        username = input("请输入您的用户名：").strip()
        passwd = input("请输入您的密码:").strip()
        get_user_info = db_handler.get_info_db()  # 执行获取用户信息转换函数，用来适应多种数据源
        if len(args) == 1:
            user_dict = get_user_info(username)
        else:
            user_dict = get_user_info(username, args[1])
        if user_dict is None:
            print("\033[31;1m用户名不存在!请检查后再输入!\033[0m")
            count += 1
            continue
        if user_dict["status"] == 1:
            print("\033[31;1m该账户已被冻结！\033[0m")
            args[0].warning("冻结用户%s尝试登陆ATM!" % user_dict["username"])
            return
        elif passwd == user_dict["password"]:
            expire_date_timestamp = time.mktime(time.strptime(user_dict["expire_date"], "%Y-%m-%d"))
            if time.time() > expire_date_timestamp:
                print("\033[31;1m账户%s已经过期，请重新办理！\033[0m" % user_dict["username"])
                time.sleep(1)
                exit()
            else:
                print("\033[32;1m登陆成功\033[0m")
                args[0].info("%s用户登陆了ATM!" % user_dict["username"])
                return user_dict
        else:
            print("\033[31;1m密码错误！\033[0m")
            count += 1
            continue
    else:
        print("\033[31;1m您已输错三次，请下次重试！谢谢！\033[0m")


def atm_login(func):
    """
    atm认证装饰器
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        ret = login_check(action_logger)
        if ret:
            user_info = args[0]
            username = user_info["user_dict"]["username"]
            atm_username = ret["username"]
            if username == atm_username:
                return func(*args, **kwargs)
            else:
                print("\033[31;1m不能用他人信用卡进行结账！\033[0m")
                time.sleep(2)
    return wrapper
