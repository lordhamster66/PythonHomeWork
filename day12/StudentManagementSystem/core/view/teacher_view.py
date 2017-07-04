#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/26
"""
讲师视图模块
"""
import os
import time
from core import table_structure
from sqlalchemy.orm import sessionmaker

# 讲师界面
teacher_show = '''==========================================================================
                            讲师管理界面

                                                今天 {today}   星期{week}
==========================================================================
【1.创建班级】
【2.为班级添加学员】
【3.创建班级上课记录】
【4.上课点名】
【5.批改成绩】
【6.返回上级菜单】
【7.退出】
=========================================================================='''

# 创建一个session实例
session_class = sessionmaker(bind=table_structure.engine)
session = session_class()


class TeacherView(object):
    """讲师视图类"""

    def __init__(self):
        self.teacher_id = None  # 定义讲师id
        self.session = None  # 定义session实例
        self.logger = None  # 定义日志对象
        self.today = None  # 定义当前日期
        self.week = None  # 定义当前星期
        # 功能映射
        self.teacher_func_info = {
            "1": self.create_class,
            "2": self.add_student,
            "3": self.create_class_record,
            "4": self.roll_call,
            "5": self.correct_homework,
            "6": lambda: "back",
            "7": quit,
        }

    def create_class(self):
        """创建班级"""
        while True:
            name = input("请输入班级名称[Tip:'q'返回]:").strip()
            if len(name) == 0:
                continue
            if name == "q":
                return
            class_obj = session.query(table_structure.Class).filter(table_structure.Class.name == name).first()
            if class_obj:
                print("\033[31;1m班级已经存在!\033[0m")
                continue
            class_obj = table_structure.Class(teacher_id=self.teacher_id, name=name)
            session.add(class_obj)
            session.commit()
            session.close()
            print("\033[32;1m班级:%s创建成功！\033[0m" % name)
            self.logger.info("班级:%s创建成功！" % name)
            break

    def chose_class(self):
        """选择班级"""
        session.commit()
        teacher_obj = session.query(table_structure.Teacher).filter(
            table_structure.Teacher.id == self.teacher_id).first()
        class_obj_list = teacher_obj.teacher_class
        print("选择班级".center(30, "-"))
        print("%-10s %-20s" % ("编号", "班级名称"))
        for index, i in enumerate(class_obj_list):
            print("%-5s %-20s" % (index+1, i))
        print("".center(33, "-"))
        while True:
            choice = input("请输入班级编号[Tip:'q'返回]:").strip()
            if len(choice) == 0:
                continue
            if choice == "q":
                return
            if choice.isdigit():
                if 0 < int(choice) <= len(class_obj_list):
                    class_obj = class_obj_list[int(choice)-1]
                    print("\033[32;1m已选择:%s\033[0m" % class_obj)
                    return class_obj
                else:
                    print("\033[31;1m超出编号范围!\033[0m")
            else:
                print("\033[31;1m编号必须为数字!\033[0m")

    def add_student(self):
        """为班级添加学员"""
        while True:
            class_obj = self.chose_class()
            if not class_obj:
                break
            while True:
                qq = input("请输入要添加的学员qq号[Tip:'q'返回,'e'返回顶级菜单]:").strip()
                if len(qq) == 0:
                    continue
                if qq == "q":
                    break
                if qq == "e":
                    session.close()
                    return
                if qq.isdigit():
                    qq = int(qq)
                    student_obj = session.query(
                        table_structure.Student).filter(table_structure.Student.qq == qq).first()
                    if student_obj:
                        # print(student_obj)
                        if student_obj in class_obj.students:
                            print("\033[31;1m学员已在该班级,无须重复添加!\033[0m")
                            continue
                        else:
                            class_obj.students.append(student_obj)
                            session.commit()
                            print("\033[32;1m学员:%s已添加进该班级!\033[0m" % student_obj.name)
                            self.logger.info("学员[%s]已添加进班级[%s]" % (student_obj.name, class_obj.name))
                            continue
                    else:
                        print("\033[31;1m没有该qq号的学员注册该系统!\033[0m")
                        continue
                else:
                    print("\033[31;1mqq号必须为数字!\033[0m")

    def create_class_record(self):
        """创建班级上课记录"""
        class_obj = self.chose_class()
        if class_obj:
            while True:
                node = input("请输入上课节次[Tip:'q'返回]:").strip()
                if node == "q":
                    break
                info = input("请输入上课内容:").strip()
                if len(node) == 0 or len(info) == 0:
                    continue
                if node.isdigit():
                    node = int(node)
                    class_record_obj = session.query(table_structure.ClassRecord).filter(
                        table_structure.ClassRecord.class_id == class_obj.id,
                        table_structure.ClassRecord.node == node
                    ).first()
                    if class_record_obj:
                        print("\033[31;1m节次已经存在!\033[0m")
                    else:
                        qdate = time.strftime("%Y-%m-%d", time.localtime())
                        class_record_obj = table_structure.ClassRecord(class_id=class_obj.id,
                                                                       qdate=qdate,
                                                                       node=node,
                                                                       info=info
                                                                       )
                        session.add(class_record_obj)
                        for student_obj in class_obj.students:
                            session.add(table_structure.StudyRecord(
                                student_id=student_obj.id,
                                class_record_id=class_record_obj.id
                            )
                                        )
                        session.commit()
                        print("\033[32;1m[%s]上课记录[%s]已创建!\033[0m" % (class_obj.name, node))
                        self.logger.info("[%s]上课记录[%s]已创建!" % (class_obj.name, node))
                        session.close()
                        return
                else:
                    print("\033[31;1m节次必须为数字!\033[0m")
        else:
            return

    @staticmethod
    def chose_node(class_obj):
        """选择上课节次"""
        session.commit()
        class_record_obj_list = class_obj.class_clsrcd
        print("上课记录".center(60, "-"))
        print("%-10s %-10s %-10s %-10s" % ("编号", "创建日期", "节次", "上课内容"))
        for index, i in enumerate(class_record_obj_list):
            print("%-10s %-15s %-10s %-10s" % (index + 1, i.qdate, i.node, i.info))
        print("".center(63, "-"))
        while True:
            choice = input("请输入节次编号[Tip:'q'返回]:").strip()
            if len(choice) == 0:
                continue
            if choice == "q":
                return
            if choice.isdigit():
                if 0 < int(choice) <= len(class_record_obj_list):
                    class_record_obj = class_record_obj_list[int(choice) - 1]
                    return class_record_obj
                else:
                    print("\033[31;1m超出编号范围!\033[0m")
            else:
                print("\033[31;1m编号必须为数字!\033[0m")

    @staticmethod
    def chose_study_record(class_record_obj):
        """选择学习记录"""
        session.commit()
        study_record_obj_list = session.query(table_structure.StudyRecord).filter(
            table_structure.StudyRecord.class_record_id == class_record_obj.id
        ).all()
        # print(study_record_obj_list)
        print("学习记录".center(60, "-"))
        print("%-10s %-10s %-10s %-10s %-10s" % ("编号", "学员姓名", "签到状态", "作业提交状态", "作业成绩"))
        for index, i in enumerate(study_record_obj_list):
            print("%-10s %-15s %-13s %-13s %-10s" % (
                index + 1, i.styrcd_student.name, i.sign_status, i.homework_status, i.score))
        print("".center(63, "-"))
        while True:
            choice = input("请输入学员记录编号[Tip:'q'返回]:").strip()
            if len(choice) == 0:
                continue
            if choice == "q":
                return
            if choice.isdigit():
                if 0 < int(choice) <= len(study_record_obj_list):
                    study_record_obj = study_record_obj_list[int(choice) - 1]
                    return study_record_obj
                else:
                    print("\033[31;1m超出编号范围!\033[0m")
            else:
                print("\033[31;1m编号必须为数字!\033[0m")

    def roll_call(self):
        """点名"""
        while True:
            class_obj = self.chose_class()
            if not class_obj:
                break
            while True:
                class_record_obj = self.chose_node(class_obj)
                if not class_record_obj:  # 如果没有任何返回，说明没选择直接退出
                    break
                while True:
                    study_record_obj = self.chose_study_record(class_record_obj)
                    if not study_record_obj:  # 如果没有任何返回，说明没选择直接退出
                        break
                    sign_status = input("请修改学员签到状态[Tip:'q'返回,'e'返回顶级菜单]:").strip()
                    if sign_status == "q":
                        break
                    if sign_status == "e":
                        session.close()
                        return
                    if len(sign_status) == 0:
                        continue
                    study_record_obj.sign_status = sign_status
                    session.commit()
                    print("\033[32;1m学员[%s]的课程[%s]第%s节签到状态已修改为%s!\033[0m" % (
                        study_record_obj.styrcd_student.name, class_obj.name,
                        class_record_obj.node, study_record_obj.sign_status))
                    self.logger.info("学员[%s]的课程[%s]第%s节签到状态已修改为%s!" % (
                        study_record_obj.styrcd_student.name, class_obj.name,
                        class_record_obj.node, study_record_obj.sign_status))

    def correct_homework(self):
        """批改成绩"""
        while True:
            class_obj = self.chose_class()
            if not class_obj:
                break
            while True:
                class_record_obj = self.chose_node(class_obj)
                if not class_record_obj:  # 如果没有任何返回，说明没选择直接退出
                    break
                while True:
                    study_record_obj = self.chose_study_record(class_record_obj)
                    if not study_record_obj:  # 如果没有任何返回，说明没选择直接退出
                        break
                    score = input("请输入学员成绩[Tip:'q'返回,'e'返回顶级菜单]:").strip()
                    if score == "q":
                        break
                    if score == "e":
                        session.close()
                        return
                    if len(score) == 0:
                        continue
                    if score.isdigit():
                        if 0 <= int(score) <= 100:
                            if study_record_obj.homework_status == "未交":
                                print("\033[31;1m该学员未提交本次作业！\033[0m")
                                continue
                            study_record_obj.score = score
                            session.commit()
                            print("\033[32;1m学员[%s]的课程[%s]第%s节成绩已修改为%s!\033[0m" % (
                                study_record_obj.styrcd_student.name, class_obj.name,
                                class_record_obj.node, study_record_obj.score))
                            self.logger.info("学员[%s]的课程[%s]第%s节成绩已修改为%s!" % (
                                study_record_obj.styrcd_student.name, class_obj.name,
                                class_record_obj.node, study_record_obj.score))
                            continue
                        else:
                            print("\033[31;1m成绩必须在0-100分以内！\033[0m")
                    else:
                        print("\33[31;1m成绩必须为数字！\033[0m")

    def __new__(cls, *args, **kwargs):
        """单例模式,只允许创建一个实例,降低内存消耗"""
        if not hasattr(cls, '_inst'):
            cls._inst = super(TeacherView, cls).__new__(cls, *args, **kwargs)
        return cls._inst

    def teacher_show(self, *args):
        """讲师视图"""
        self.teacher_id = args[0]  # 获取讲师id
        self.session = args[1]  # 获取session实例
        self.logger = args[2]  # 获取日志对象
        self.today = args[3]  # 获取当前日期
        self.week = args[4]  # 获取当前星期
        while True:
            os.system("cls")
            print(teacher_show.format(today=self.today, week=self.week))
            choice = input(">>:").strip()
            if len(choice) == 0:
                continue
            if choice in self.teacher_func_info:
                ret = self.teacher_func_info[choice]()
                if ret == "back":
                    break
            else:
                print("\033[31;1m输入有误！\033[0m")

