#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering

"""
交易处理模块，处理所有的交易行为
"""
import time
from conf import settings
from core import db_handler
from core import report_handle


def make_trade(user_info, money, trade_type, logger_obj, **kwargs):
    """
    交易中心函数，处理所有的交易行为
    :param user_info: 用户信息
    :param money: 交易金额
    :param trade_type: 交易类型
    :param logger_obj: 日志对象
    :param kwargs: 其他拓展参数
    :return:
    """
    money = float(money)
    dump_info = db_handler.dump_info_db()
    if trade_type in settings.TRADE_TYPE:
        interest = money * settings.TRADE_TYPE[trade_type]['interest']     # 获取交易利息
        balance_before = user_info["user_dict"]["balance"]                 # 获取当前余额
        if settings.TRADE_TYPE[trade_type]['action'] == "plus":
            balance_after = balance_before + money + interest
            trade_money = money
            trade_interest = interest
        elif settings.TRADE_TYPE[trade_type]['action'] == "minus":
            balance_after = balance_before - money - interest
            trade_money = -money
            trade_interest = -interest
            if balance_after < 0:
                print("\033[31;1m您的当前余额为：%s,此次交易金额为-%s,余额不足无法完成交易！\033[0m"
                      % (balance_before, money+interest))
                return
        else:
            logger_obj.warning("交易类型%s配置信息有误，请检查！" % trade_type)
            return
        if trade_type == "transfer":
            other_account = kwargs["other_account"]
            if user_info["user_dict"]["username"] == other_account:
                print("\033[31;1m请不要自己转自己账户！OK！\033[0m")
                time.sleep(1)
                return
            get_user_info = db_handler.get_info_db()
            other_account_dict = get_user_info(other_account)
            if other_account_dict:
                expire_date_timestamp = time.mktime(time.strptime(other_account_dict["expire_date"], "%Y-%m-%d"))
                if time.time() > expire_date_timestamp:
                    print("\033[31;1m要转账的用户%s已经过期，请告知对方！\033[0m" % other_account)
                    time.sleep(1)
                    return
                if other_account_dict["status"] == 1:
                    print("\033[31;1m要转账的用户%s已被冻结，请告知对方！\033[0m" % other_account)
                    time.sleep(1)
                    return
                if other_account_dict:
                    other_account_dict["balance"] += money     # 将转账对象的账户里面添加一笔资金
                    dump_info(other_account_dict)              # 将新的转账对象的用户信息存入数据库
                    print("转账对象%s接收到%s来自您的资金!"%(other_account,money))
                    # 生成交易日志
                    logger_obj.info("account_id:%s  trade:%s  amount:%s " %
                                    (other_account_dict["id"], trade_type, money))
                    # 以下为报告生成
                    date = time.strftime("%Y-%m-%d&%H:%M:%S", time.localtime())
                    report = "%s %s %s %s %s" % (date, "收到转账", money, 0, other_account_dict["balance"])
                    report_handle.create_report(other_account_dict, report)
            else:
                print("\033[31;1m要转账的用户对象%s不存在，请检查！\033[0m"%other_account)
                return
        user_info["user_dict"]["balance"] = balance_after  # 获取用户最新余额
        user_dict = user_info["user_dict"]                 # 用户信息
        ret = dump_info(user_dict)                         # 将新的用户信息存入数据库
        if ret:
            print("您之前的余额为：%s,此次交易金额为：%s,利息为:%s,最新余额为：\033[31;1m%s\033[0m"
                  % (balance_before, trade_money, trade_interest, balance_after))
            time.sleep(1)
            # 生成交易日志
            logger_obj.info("account_id:%s  trade:%s  amount:%s  interest:%s" %
                                (user_dict["id"], trade_type, trade_money, trade_interest) )
            # 以下为报告生成
            date = time.strftime("%Y-%m-%d&%H:%M:%S", time.localtime())
            report = "%s %s %s %s %s" % (
                    date, settings.TRADE_TYPE[trade_type]["zh"],
                    trade_money, trade_interest, balance_after)
            report_handle.create_report(user_dict, report)
        else:
            logger_obj.warning("%s用户文件不存在！" % user_dict["username"])
            return
        return "done"
    else:
        print("\033[31;1m%s交易类型不存在!\033[0m" % trade_type)
        return
