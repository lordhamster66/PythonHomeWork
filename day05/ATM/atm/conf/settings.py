#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
import os
import logging
# 主路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志文件存放目录
LOG_PATH = os.path.join(BASE_PATH, "log")

# 数据库信息
DATABASE = {
            "engine": "file",
            "dbpath": os.path.join(os.path.join(BASE_PATH, "db"), "user"),
            "manage_dbpath": os.path.join(os.path.join(BASE_PATH, "db"), "manage"),
            "userid": os.path.join(os.path.join(BASE_PATH, "db"), "user_id.json")
            }

# 设置日志显示级别
LOG_LEVEL = {
            "global_level": logging.INFO,
            "ch_level": logging.WARNING,
            "fh_level": logging.INFO
            }

# 日志类型
LOG_TYPE = {
            "trade": "trade.log",
            "action": "action.log",
            "manage": "manage.log"
            }

# 报告路径
REPORT_PATH = os.path.join(BASE_PATH, "report")


# 交易类型
TRADE_TYPE = {
            "consume": {"action": "minus", "interest": 0, "zh": "消费"},
            "repay": {"action": "plus", "interest": 0, "zh": "还款"},
            "withdraw": {"action": "minus", "interest": 0.05, "zh": "提现"},
            "transfer": {"action": "minus", "interest": 0, "zh": "转账"}
             }

# 状态对照表
STR_STATUS = ["正常", "冻结"]

# 默认用户信息
DEFAULT_USER_DICT = {
                    "id": None,
                    "username": None,
                    "password": "123",
                    "credit": 15000,
                    "balance": 15000,
                    "enroll_date": None,
                    "expire_date": None,
                    "status": 0  # 0:正常    1:冻结
                    }