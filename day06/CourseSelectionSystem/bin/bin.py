#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/7
import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from core.main import admin_view
from core.main import student_view
from core.main import teacher_view
from conf import exhibition
from core import module


# 功能编号对应至conf下的exhibition.action_show
function_match = {
                "1": admin_view.admin_show,
                "2": teacher_view.teacher_show,
                "3": student_view.student_show,
                "4": exit
                }

if __name__ == '__main__':
    while True:
        os.system("cls")
        print(exhibition.action_show.format(today=module.today, week=module.week))
        choice = input("请输入您的选项:").strip()
        if len(choice) == 0:
            continue
        if choice in function_match:
            function_match[choice]()
        else:
            print("\033[31;1m您的输入有误请重新输入！\033[0m")
            continue
