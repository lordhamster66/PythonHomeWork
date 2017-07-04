#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/26
"""
学员视图
"""
import os
from core import table_structure
from sqlalchemy.orm import sessionmaker

# 学员界面
student_show = '''==========================================================================
                              学员界面

                                                今天 {today}   星期{week}
==========================================================================
【1.提交作业】
【2.查看作业成绩】
【3.查看班级成绩排名】
【4.返回上级菜单】
【5.退出】
=========================================================================='''

# 创建一个session实例
session_class = sessionmaker(bind=table_structure.engine)
session = session_class()


class StudentView(object):
    """学员视图类"""

    def __init__(self):
        self.student_id = None  # 定义学员id
        self.session = None  # 定义session实例
        self.logger = None  # 定义日志对象
        self.today = None  # 定义当前日期
        self.week = None  # 定义当前星期
        # 功能映射
        self.student_func_info = {
            "1": self.hand_in_homework,
            "2": self.check_homework_score,
            "3": self.check_class_ranking,
            "4": lambda: "back",
            "5": quit,
        }

    def chose_class(self):
        """选择班级"""
        student_obj = session.query(table_structure.Student).filter(
            table_structure.Student.id == self.student_id).first()
        class_obj_list = student_obj.classes
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

    @staticmethod
    def chose_node(class_obj):
        """选择上课节次"""
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

    def chose_study_record(self, class_record_obj):
        """选择学习记录"""
        study_record_obj = session.query(table_structure.StudyRecord).filter(
            table_structure.StudyRecord.student_id == self.student_id,
            table_structure.StudyRecord.class_record_id == class_record_obj.id
        ).first()
        # print(study_record_obj)
        print("学习记录".center(60, "-"))
        print("%-10s %-10s %-10s %-10s" % ("学员姓名", "签到状态", "作业提交状态", "作业成绩"))
        print("%-15s %-13s %-13s %-10s" % (
            study_record_obj.styrcd_student.name, study_record_obj.sign_status,
            study_record_obj.homework_status, study_record_obj.score)
              )
        print("".center(63, "-"))
        return study_record_obj

    def hand_in_homework(self):
        """提交作业"""
        while True:
            class_obj = self.chose_class()
            if not class_obj:
                break
            while True:
                class_record_obj = self.chose_node(class_obj)
                if not class_record_obj:
                    break
                while True:
                    study_record_obj = self.chose_study_record(class_record_obj)
                    if not study_record_obj:
                        break
                    choice = input("确认提交作业吗[y/n]？[Tip:'q'返回,'e'返回顶级菜单]").strip()
                    if choice == "q":  # 返回上级菜单
                        break
                    if choice == "e":  # 返回顶级菜单
                        session.close()  # 关闭会话
                        return
                    if len(choice) == 0:
                        continue
                    if choice == "y":
                        study_record_obj.homework_status = "已提交"
                        print("\033[32;1m学员[%s]的课程[%s]第%s节作业已提交!\033[0m" % (
                            study_record_obj.styrcd_student.name, study_record_obj.styrcd_clsrcd.clsrcd_class.name,
                            study_record_obj.styrcd_clsrcd.node))
                        self.logger.info("学员[%s]的课程[%s]第%s节作业已提交!" % (
                            study_record_obj.styrcd_student.name, study_record_obj.styrcd_clsrcd.clsrcd_class.name,
                            study_record_obj.styrcd_clsrcd.node))
                        session.commit()  # 刷新数据库
                        session.close()  # 关闭会话
                        return
                    if choice == "n":
                        break
                    else:
                        print("\033[31;1m输入有误!\033[0m")

    def check_homework_score(self):
        """查看作业成绩"""
        while True:
            class_obj = self.chose_class()
            if not class_obj:
                break
            while True:
                class_record_obj = self.chose_node(class_obj)
                if not class_record_obj:
                    break
                while True:
                    study_record_obj = self.chose_study_record(class_record_obj)
                    if not study_record_obj:
                        break
                    choice = input("继续查看成绩吗[y/n]？").strip()
                    if len(choice) == 0:
                        continue
                    if choice == "y":
                        break
                    if choice == "n":
                        session.close()
                        return
                    else:
                        print("\033[31;1m输入有误!\033[0m")

    def check_class_ranking(self):
        """查看班级成绩排名"""
        while True:
            class_obj = self.chose_class()
            if not class_obj:
                break
            score_list = []  # 存放所有学员的成绩
            myscore = 0  # 定义学员初始成绩
            # 取出该学员的所有学习记录
            mystudy_record_list = session.query(table_structure.StudyRecord).filter(
                table_structure.StudyRecord.student_id == self.student_id
            ).all()
            for i in mystudy_record_list:
                # 对该班级的学习记录进行分数累加
                if i.styrcd_clsrcd.class_id == class_obj.id:
                    myscore += i.score
            # 取出该班级的所有学生列表
            student_obj_list = class_obj.students
            for student_obj in student_obj_list:
                student_score = 0  # 定义一位学员的初始成绩
                # 取出该学员的所有学习记录
                study_record_list = session.query(table_structure.StudyRecord).filter(
                    table_structure.StudyRecord.student_id == student_obj.id
                ).all()
                for study_record in study_record_list:
                    # 对该学员在该班级的学习记录进行分数累加
                    if study_record.styrcd_clsrcd.class_id == class_obj.id:
                        student_score += study_record.score
                score_list.append(student_score)
            score_list.sort()  # 所有学员的成绩进行排序
            score_list.reverse()  # 排序完成之后反转，即从大到小排序
            # print(score_list)
            print("\033[33;1m您目前在该班级的排名为:\033[0m\033[31;1m%s\033[0m"
                  % (score_list.index(myscore)+1))  # 下标加1即为该学员的总排名
            while True:
                choice = input("继续查看排名吗[y/n]？").strip()
                if len(choice) == 0:
                    continue
                if choice == "y":
                    break
                if choice == "n":
                    session.close()
                    return
                else:
                    print("\033[31;1m输入有误!\033[0m")

    def __new__(cls, *args, **kwargs):
        """单例模式,只允许创建一个实例,降低内存消耗"""
        if not hasattr(cls, '_inst'):
            cls._inst = super(StudentView, cls).__new__(cls, *args, **kwargs)
        return cls._inst

    def student_show(self, *args):
        """讲师视图"""
        self.student_id = args[0]  # 获取学员id
        self.session = args[1]  # 获取session实例
        self.logger = args[2]  # 获取日志对象
        self.today = args[3]  # 获取当前日期
        self.week = args[4]  # 获取当前星期
        while True:
            os.system("cls")
            print(student_show.format(today=self.today, week=self.week))
            choice = input(">>:").strip()
            if len(choice) == 0:
                continue
            if choice in self.student_func_info:
                ret = self.student_func_info[choice]()
                if ret == "back":
                    break
            else:
                print("\033[31;1m输入有误！\033[0m")


