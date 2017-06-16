#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering

"""
主逻辑模块，所有业务逻辑均通过该模块处理
"""

import os
import time
import datetime
from conf import exhibition                    # 展示模板
from core.mylogger import Mylogger             # 自定义日志模块
from core.login import login_check             # 登陆模块
from core.trade import make_trade              # 交易处理模块
from core import db_handler                    # 数据库转接模块
from core.login import islogin                 # 登陆验证装饰器
from core.login import atm_login               # 其他平台登陆ATM时的认证装饰器
from conf import settings                      # 配置信息
from core import report_handle                 # 报告模块
from core import data_access

# 生成三种日志对象
action_logger = Mylogger("action")             # 行为日志
trade_logger = Mylogger("trade")               # 交易日志
manage_logger = Mylogger("manage")             # 管理日志

# 用来临时存储一些信息
user_info = {
            "user_dict": None,
            "islogin": False,
            "today": None,
            "week": None
            }

# 生成日期，星期
week_list = ("一", "二", "三", "四", "五", "六", "日")      # 星期对照表
today = time.strftime("%Y-%m-%d", time.localtime())         # 获取今天的日期
week = week_list[int(datetime.datetime.now().weekday())]   # 获取星期


def account_info(*args):
    """
    账户信息查询函数
    :param args: 接收非固定参数
    :return:
    """
    user_info = args[0]
    get_user_info = db_handler.get_info_db()
    user_info["user_dict"] = get_user_info(user_info["user_dict"]["username"])  # 获取用户最新信息
    str_status = settings.STR_STATUS
    while True:
        os.system("cls")
        print(exhibition.account_info_show.format(
                                                user=user_info["user_dict"]["username"],
                                                today=user_info["today"],
                                                week=user_info["week"],
                                                id=user_info["user_dict"]["id"],
                                                status=str_status[user_info["user_dict"]["status"]],
                                                enroll_date=user_info["user_dict"]["enroll_date"],
                                                expire_date=user_info["user_dict"]["expire_date"],
                                                credit=user_info["user_dict"]["credit"],
                                                balance=user_info["user_dict"]["balance"]
                                                ))
        user_choice = input("请输入功能选项>>").strip()
        if user_choice == "1":
            return
        elif user_choice == "2":
            exit()
        else:
            print("\033[31;1m请输入正确的功能选项！\033[0m")


@atm_login
def consume(*args):
    """
    消费接口，对外提供
    :param args:
    :return:
    """
    user_info = args[0]
    money = args[1]
    get_user_info = db_handler.get_info_db()
    user_info["user_dict"] = get_user_info(user_info["user_dict"]["username"])  # 获取用户信息
    try:
        ret = make_trade(user_info, money, "consume", trade_logger)
    except TypeError:
        print("该用户未办理信用卡！")
        return
    return ret


@islogin
def repay(*args):
    """
    还款接口
    :param args: 接收非固定参数
    :return:
    """
    while True:
        user_info = args[0]
        get_user_info = db_handler.get_info_db()
        user_info["user_dict"] = get_user_info(user_info["user_dict"]["username"])  # 获取用户最新信息
        credit = user_info["user_dict"]["credit"]
        balance = user_info["user_dict"]["balance"]
        my_repay = float(credit) - float(balance)
        os.system("cls")
        print(exhibition.repay_show.format(
                                            user = user_info["user_dict"]["username"],
                                            today = user_info["today"],
                                            week = user_info["week"],
                                            credit = user_info["user_dict"]["credit"],
                                            balance = user_info["user_dict"]["balance"],
                                            repay = my_repay
                                            ))
        user_choice = input("请输入功能选项>>").strip()
        if user_choice == "1":
            if my_repay <= 0:
                print("\033[31;1m亲，您不需要进行还款！\033[0m")
                time.sleep(1)
                continue
            while True:
                money = input("请输入您想还款的现金：").strip()
                if len(money) == 0:
                    continue
                try:
                    money = float(money)
                    if money == 0:
                        continue
                    elif money <= my_repay:
                        user_info = make_trade(user_info, money, "repay", trade_logger)
                        break
                    elif money > my_repay:
                        print("\033[31;1m亲，您不需要还这么多！\033[0m")
                except ValueError:
                    print("\033[31;1m输入不规范请重新输入！\033[0m")
        elif user_choice == "2":
            return
        elif user_choice == "3":
            exit()
        else:
            print("\033[31;1m请输入正确的功能选项！\033[0m")


@islogin
def withdraw(*args):
    '''
    提现函数
    :param args: 接收非固定参数，为以后扩展做准备
    :return:
    '''
    user_info = args[0]
    get_user_info = db_handler.get_info_db()
    user_info["user_dict"] = get_user_info(user_info["user_dict"]["username"]) #获取用户最新信息
    while True:
        os.system("cls")
        print(exhibition.withdraw_show.format(
                                            user = user_info["user_dict"]["username"],
                                            today = user_info["today"],
                                            week = user_info["week"],
                                            credit = user_info["user_dict"]["credit"],
                                            balance = user_info["user_dict"]["balance"]
                                            ))
        user_choice = input("请输入功能选项>>").strip()
        if user_choice == "1":
            while True:
                money = input("请输入您想提取的现金：").strip()
                if len(money) == 0:continue
                try:
                    money = float(money)
                    if money == 0:continue
                    make_trade(user_info,money,"withdraw",trade_logger)
                    break
                except ValueError:print("\033[31;1m输入不规范请重新输入！\033[0m")
        elif user_choice == "2":return
        elif user_choice == "3":exit()
        else:print("\033[31;1m请输入正确的功能选项！\033[0m")


@islogin
def transfer(*args):
    '''
    转账函数
    :param args: 接收非固定参数
    :return:
    '''
    user_info = args[0]
    get_user_info = db_handler.get_info_db()
    user_info["user_dict"] = get_user_info(user_info["user_dict"]["username"])  # 获取用户最新信息
    while True:
        os.system("cls")
        print(exhibition.transfer_show.format(
                                            user = user_info["user_dict"]["username"],
                                            today = user_info["today"],
                                            week = user_info["week"],
                                            credit = user_info["user_dict"]["credit"],
                                            balance = user_info["user_dict"]["balance"]
                                            ))
        user_choice = input("请输入功能选项>>").strip()
        if user_choice == "1":
            while True:
                transfer_obj = input("请输入您想转账的对象用户名：").strip()
                money = input("请输入您想转账的现金：").strip()
                if len(money) == 0: continue
                try:
                    money = float(money)
                    if money == 0: continue
                    make_trade(user_info, money, "transfer", trade_logger,other_account = transfer_obj)
                    break
                except ValueError:print("\033[31;1m输入不规范请重新输入！\033[0m")
        elif user_choice == "2":return
        elif user_choice == "3":exit()
        else:print("\033[31;1m请输入正确的功能选项！\033[0m")


@islogin
def bill_inquiry(*args):
    '''
    用户账单查询函数
    :param args: 接收非固定参数
    :return:
    '''
    user_dict = args[0]["user_dict"]
    exit_flag = False
    while not exit_flag:
        start_time = input("请输入起始日期（格式：2017-04-24）：").strip()
        end_time = input("请输入终止日期（格式：2017-04-25）：").strip()
        try:
            time.mktime(time.strptime(start_time, "%Y-%m-%d"))  # 起始日期时间戳
            time.mktime(time.strptime(end_time, "%Y-%m-%d"))  # 终止日期时间戳
        except ValueError:
            print("\033[31;1m格式错误，请重新输入！\033[0m")
            continue
        report_list = report_handle.check_report(user_dict,start_time,end_time)
        print(exhibition.report_show)
        for i in report_list:
            print("%-25s%-10s%-10s%-10s%-10s"
                  %(i[0],i[1],i[2],i[3],i[4]))
        print("==========================================================================")
        while True:
            choice = input("是否继续查询[Y/N]：").strip()
            if choice == "Y":break
            elif choice == "N":
                exit_flag = True
                break
            else:print("\033[31;1m输入有误！\033[0m")


def cancellation(*args):
    '''
    注销函数，可以让用户重新登陆
    :return:
    '''
    user_info["islogin"] = None                            #注销用户登陆状态
    user_info["user_dict"] = None                          #注销用户账号信息
    return  True


def logout(*args):
    '''
    退出函数，一经执行便退出整个程序
    :param args: 接收非固定参数
    :return: 无返回值
    '''
    exit()


def atm_show(user_info):
    '''
    ATM首界面展示函数
    :return:
    '''
    get_user_info = db_handler.get_info_db()
    user_info["user_dict"] = get_user_info(user_info["user_dict"]["username"])  # 获取用户最新信息
    exit_flag = None
    while not exit_flag:
        os.system("cls")                                       #清屏
        print(exhibition.atm_show.format(
                                        user=user_info["user_dict"]["username"],
                                        today=user_info["today"],
                                        week=user_info["week"]))            #ATM展示界面
        choice = {
                "1":account_info,
                "2":withdraw,
                "3":transfer,
                "4":repay,
                "5":bill_inquiry,
                "6":cancellation,
                "7":logout
                 }
        user_choice = input("请输入功能选项>>").strip()
        if user_choice in choice:
            exit_flag = choice[user_choice](user_info)
        else:print("\033[31;1m请输入正确的功能选项！\033[0m")


# 以下代码程序一经启动atm.py便执行
def action():
    """
    用户端执行函数
    :return:
    """
    while True:
        os.system("cls")  # 清屏
        print(exhibition.action_show.format(today=today, week=week))  # 登陆界面
        user_dict = login_check(action_logger)
        if user_dict:
            user_info["islogin"] = True
            user_info["user_dict"] = user_dict
            user_info["today"] = today
            user_info["week"] = week
            atm_show(user_info)
        else:
            break


def add_user(*args):
    """
    添加用户函数
    :param args: 接收非固定参数
    :return:
    """
    get_file = db_handler.get_all_db()
    user_id_path = settings.DATABASE["userid"]
    user_id = get_file(user_id_path)
    tmp_username_list = user_id[1]  # 临时存储所有的用户名
    tmp_userid_list = user_id[0]
    while True:
        username = input("请输入要添加的用户名：").strip()
        if username in tmp_username_list:
            print("\033[31;1m您要添加的用户名已经存在，无需添加！\033[0m")
            break
        elif username.isidentifier():
            user_dict = settings.DEFAULT_USER_DICT
            id = tmp_userid_list[-1]+1  # id自增
            # 设置用户信息
            user_dict["id"] = id
            user_dict["username"] = username
            user_dict["enroll_date"] = str(today)
            tmp_expire_date = datetime.datetime.now().replace(year=datetime.datetime.now().year+5)
            user_dict["expire_date"] = str(tmp_expire_date)[:10]
            # 将用户ID，用户名添加至数据库以便核查
            user_id[0].append(id)
            user_id[1].append(username)
            # 创建两个导入信息至数据库的对象
            dump_file = db_handler.dump_all_db()
            dump_info = db_handler.dump_info_db()
            # 将用户信息以及userid更新至数据库
            dump_info(user_dict)
            dump_file(user_id,settings.DATABASE["userid"])
            # 创建一个新用户的报告文件
            report_file_path = os.path.join(settings.REPORT_PATH, "%s.rp" % username)
            data_access.write_file("",report_file_path)
            # 打印信息
            print("用户%s已被管理者%s添加至ATM系统！" % (username, args[0]["username"]))
            # 记录管理日志
            manage_logger.info("用户%s已被管理者%s添加至ATM系统！" % (username, args[0]["username"]))
            return
        else:
            print("\033[31;1m输入不规范，请重新输入！\033[0m")
            continue


def credit_change(*args):
    """
    用户信用额度调整函数
    :param args: 接收非固定参数
    :return:
    """
    while True:
        username = input("请输入要调整的用户名：").strip()
        credit = input("请输入要调整的额度：").strip()
        get_user_info = db_handler.get_info_db()
        user_dict = get_user_info(username)  # 获取用户信息
        if user_dict:
            if credit.isdigit() and int(credit) > 0:
                user_dict["credit"] = credit
                dump_info = db_handler.dump_info_db()
                dump_info(user_dict)
                print("\033[31;1m用户%s信用额度调整成功！\033[0m"%username)
                manage_logger.info("用户%s已被管理者%s重新设置信用额度，新额度为：%s"
                                   % (username, args[0]["username"], credit))
                time.sleep(1)
                break
            else:
                print("\033[31;1m输入不规范，请重新输入！\033[0m")
                continue
        else:
            print("要调整的用户不存在，请重新输入！")
            continue


def freeze_account(*args):
    """
    用户冻结函数
    :param args: 接收非固定参数
    :return:
    """
    while True:
        username = input("请输入要冻结的用户名：").strip()
        get_user_info = db_handler.get_info_db()
        user_dict = get_user_info(username)                # 获取用户信息
        if user_dict:
            if user_dict["status"] == 1:
                print("\033[31;1m用户%s已经处于冻结状态！\033[0m" % username)
                time.sleep(1)
                break
            user_dict["status"] = 1
            dump_info = db_handler.dump_info_db()
            dump_info(user_dict)
            print("\033[31;1m用户%s冻结成功！\033[0m" % username)
            manage_logger.info("用户%s已被管理者%s冻结" % (username, args[0]["username"]))
            time.sleep(1)
            break
        else:
            print("输入不规范，请重新输入！")
            continue


def unfreeze_account(*args):
    """
    用户解冻函数
    :param args:接收非固定参数
    :return:
    """
    while True:
        username = input("请输入要解冻的用户名：").strip()
        get_user_info = db_handler.get_info_db()           # 获取相应的数据访问函数
        user_dict = get_user_info(username)                # 获取用户信息
        if user_dict:
            if user_dict["status"] == 0:
                print("\033[31;1m用户%s是正常状态，不需要解冻！\033[0m" % username)
                time.sleep(1)
                break
            user_dict["status"] = 0
            dump_info = db_handler.dump_info_db()
            dump_info(user_dict)
            print("\033[31;1m用户%s解冻成功！\033[0m" % username)
            manage_logger.info("用户%s已被管理者%s解冻" % (username, args[0]["username"]))
            time.sleep(1)
            break
        else:
            print("输入不规范，请重新输入！")
            continue


# 以下代码程序一经启动manage.py便执行
def manage_action():
    """
    管理端执行函数
    :return:
    """
    print(exhibition.manage_firdt_show.format(today=today, week=week))             # 管理端登陆界面
    manage_dict = login_check(action_logger, settings.DATABASE["manage_dbpath"])   # 登陆验证，验证成功返回用户信息
    if manage_dict:
        quit_flag = False
        while not quit_flag:
            os.system("cls")  # 清屏
            print(exhibition.manage_show.format(today=today, week=week, manager=manage_dict["username"]))
            choose = {
                    "1": add_user,
                    "2": credit_change,
                    "3": freeze_account,
                    "4": unfreeze_account,
                    "5": logout
                    }
            manage_choice = input("请输入功能选项>>").strip()
            if manage_choice in choose:
                quit_flag = choose[manage_choice](manage_dict)
            else:
                print("\033[31;1m请输入正确的功能选项！\033[0m")
