#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering

"""
初始化用户信息模块，并初始化日志以及报告
"""
import json
import os
path = os.path.dirname(os.path.abspath(__file__))
user_dict = {
    "id": 1,
    "username": "abc",
    "password": "123",
    "credit": 15000,
    "balance": 15000,
    "enroll_date": "2017-04-22",
    "expire_date": "2021-01-22",
    "status": 0  # 0:正常    1:冻结
}

user_dict1 = {
    "id": 2,
    "username": "abcd",
    "password": "1234",
    "credit": 15000,
    "balance": 15000,
    "enroll_date": "2017-04-23",
    "expire_date": "2021-01-23",
    "status": 0  # 0:正常    1:冻结
}

user_id = [[1, 2], ["abc", "abcd"]]

json.dump(user_dict, open(os.path.join(os.path.join(path, "user"), "%s.json"%user_dict["username"]), "w",
                          encoding="utf-8"))
json.dump(user_dict1, open(os.path.join(os.path.join(path, "user"), "%s.json"%user_dict1["username"]), "w",
                           encoding="utf-8"))
json.dump(user_id, open(os.path.join(path, "user_id.json"), "w", encoding="utf-8"))


log_path = os.path.join(os.path.dirname(path), "log")
f = open(os.path.join(log_path, "action.log"), "w", encoding="utf-8")
f.close()
f1 = open(os.path.join(log_path, "trade.log"), "w", encoding="utf-8")
f1.close()
f2 = open(os.path.join(log_path, "manage.log"), "w", encoding="utf-8")
f2.close()

report_path = os.path.join(os.path.dirname(path), "report")
f3 = open(os.path.join(report_path, "abc.rp"), "w", encoding="utf-8")
f3.close()
f4 = open(os.path.join(report_path, "abcd.rp"), "w", encoding="utf-8")
f4.close()

# user_dict2 =
# json.load(open(os.path.join(os.path.join(path,"user"),"%s.json"%user_dict1["username"]),"r",encoding="utf-8"))
# print(user_dict2)
