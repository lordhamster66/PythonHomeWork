#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/26
"""
主界面模块
"""
import time
import datetime
import os
import hashlib
from core import mylogger
from conf import settings
from core import table_structure
from sqlalchemy.orm import sessionmaker
from core.view import student_view
from core.view import teacher_view

# 创建一个session实例
session_class = sessionmaker(bind=table_structure.engine)
session = session_class()

# 生成日期，星期
week_list = ("一", "二", "三", "四", "五", "六", "日")      # 星期对照表
today = time.strftime("%Y-%m-%d", time.localtime())        # 获取今天的日期
week = week_list[int(datetime.datetime.now().weekday())]   # 获取星期

# 生成日志对象
action_logger = mylogger.Mylogger(settings.ACTION_LOGPATH, "action", settings.LOG_LEVEL).get_logger()

# 程序启动画面
action_show = '''==========================================================================
                            学员管理系统

                                                今天 {today}   星期{week}
==========================================================================
【-1.删除该系统在数据库创建的所有表格】
【0.初始化数据库】
【1.讲师登陆】
【2.学员登陆】
【3.学员注册】
【4.退出】
=========================================================================='''


def login(user_type):
    """登陆接口"""
    user_type_class = {
        "teacher": table_structure.Teacher,
        "student": table_structure.Student
    }
    if user_type_class.get(user_type):
        user_class = user_type_class[user_type]
        while True:
            username = input("请输入用户名[Tip:'q'退出]:").strip()
            if username == "q":
                return
            password = input("请输入密码:").strip()
            if len(username) == 0 or len(password) == 0:
                continue
            md5_obj = hashlib.md5()
            md5_obj.update(password.encode())
            password = md5_obj.hexdigest()
            user_obj = session.query(user_class).filter(user_class.username == username).first()
            session.commit()
            if user_obj:
                if password == user_obj.password:
                    print("\033[32;1m登陆成功!\033[0m")
                    user_id = user_obj.id
                    session.close()
                    return user_id
                else:
                    print("\033[31;1m密码错误!\033[0m")
            else:
                print("\033[31;1m用户名不存在!\033[0m")
    else:
        print("\033[31;1m类型错误!\033[0m")


def drop_system():
    """注销系统"""
    session.commit()  # 刷新数据库
    table_structure.drop_db()
    print("\033[31;1m已清空该系统在数据库创建的所有表！\033[0m")
    time.sleep(1)


def init_system():
    """初始化系统"""
    session.commit()  # 刷新数据库
    table_structure.drop_db()
    table_structure.init_db()
    m1 = hashlib.md5()
    m1.update("123".encode())
    teacher1 = table_structure.Teacher(name="Alex", age=22, username="alex", password=m1.hexdigest())
    class1 = table_structure.Class(teacher_id=1, name="Python自动化开发第100期")
    student1 = table_structure.Student(name="Breakering", age=22,
                                       qq=123456, username="breakering", password=m1.hexdigest())
    student2 = table_structure.Student(name="Profhua", age=23,
                                       qq=321654, username="profhua", password=m1.hexdigest())
    student3 = table_structure.Student(name="Wolf", age=24,
                                       qq=654321, username="wolf", password=m1.hexdigest())
    session.add_all([teacher1, class1, student1, student2, student3])
    class1.students = [student1, student2, student3]
    session.commit()
    session.close()
    print("\033[32;1m已初始化该系统在数据库的所有表！\033[0m")
    time.sleep(1)


def teacher_login():
    """讲师登陆"""
    teacher_id = login("teacher")
    # print(teacher_id)
    if teacher_id:
        teacher_view_obj = teacher_view.TeacherView()
        teacher_view_obj.teacher_show(teacher_id, session, action_logger, today, week)
    else:
        return


def student_login():
    """学员登陆"""
    student_id = login("student")
    # print(student_id)
    if student_id:
        student_view_obj = student_view.StudentView()
        student_view_obj.student_show(student_id, session, action_logger, today, week)
    else:
        return


def student_sign():
    """学员注册"""
    while True:
        name = input("请输入您的姓名[Tip:'q'返回]:").strip()
        if name == "q":
            break
        age = input("请输入您的年龄:").strip()
        qq = input("请输入您的qq号:").strip()
        username = input("请输入您的用户名:").strip()
        password = input("请输入您的密码:").strip()
        if len(name) == 0 or len(age) == 0 or len(qq) == 0 or len(username) == 0 or len(password) == 0:
            continue
        if not age.isdigit() or not qq.isdigit():
            print("\033[31;1m年龄和qq号必须为数字!\033[0m")
            continue
        age = int(age)
        qq = int(qq)
        s1 = session.query(table_structure.Student).filter(table_structure.Student.qq == qq).first()
        if s1:
            print("\033[31;1mqq号已经注册过!\033[0m")
            continue
        s2 = session.query(table_structure.Student).filter(table_structure.Student.username == username).first()
        if s2:
            print("\033[31;1m用户名已存在!\033[0m")
            continue
        md5_obj = hashlib.md5()
        md5_obj.update(password.encode())
        password = md5_obj.hexdigest()
        student_obj = table_structure.Student(name=name, age=age, qq=qq, username=username, password=password)
        session.add(student_obj)
        session.commit()
        session.close()
        print("\033[32;1m学员:%s成功注册了该系统！\033[0m" % name)
        action_logger.info("学员:%s成功注册了该系统！" % name)
        break

# 功能映射
main_func_info = {
    "-1": drop_system,
    "0": init_system,
    "1": teacher_login,
    "2": student_login,
    "3": student_sign,
    "4": quit
}


def main_show(*args):
    """展示主界面"""
    while True:
        os.system("cls")
        print(action_show.format(today=today, week=week))
        choice = input(">>:").strip()
        if len(choice) == 0:
            continue
        if choice in main_func_info:
            main_func_info[choice]()
        else:
            print("\033[31;1m输入有误！\033[0m")
