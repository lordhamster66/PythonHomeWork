#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/9
import os
import time
import datetime
from core import module
from core.module import Teacher
from core.module import StudentToClasses
from lib.public import login_decorator
from conf import exhibition

# 状态管理
teacher_status = {"status": None, "user": "游客", "obj": None}


def lunch_teacher():
    """ 讲师登陆 """
    ret = Teacher.login()
    print(ret["data"])
    teacher_status["status"] = ret["status"]
    if ret["status"] == 1:
        teacher_status["user"] = ret["obj"].name
        teacher_status["obj"] = ret["obj"]


def get_classes():
    """ 查看并获取所选班级函数 """
    teacher_obj = teacher_status["obj"]
    classes_obj_list = teacher_obj.get_classes_obj()
    print("".center(74, "="))
    print("\033[35;1m%-3s%-16s%-7s%-7s%-5s\033[0m" %
          ("编号", "班级名称", "学期", "课程名称", "班级人数"))
    for index, obj in enumerate(classes_obj_list):
        print("\033[35;1m%-5s%-15s%-7s%-10s%-10s\033[0m" %
              (index + 1, obj.name, obj.semester, obj.course_id.get_obj_by_id().name,
               obj.check_student_num()))
    print("".center(74, "="))
    while True:
        choice = input("请输入班级编号：[tip:输入'q'返回]").strip()
        if choice == "q":
            return
        if len(choice) == 0:
            continue
        try:
            choice = int(choice)
            if 0 < choice <= len(classes_obj_list):
                classes_obj = classes_obj_list[choice - 1]
                break
            else:
                print("\033[31;1m您的输入不在编号范围内，请重新输入！\033[0m")
                continue
        except ValueError:
            print("\033[31;1m您的输入有误，请重新输入！\033[0m")
            continue
    return classes_obj


def get_student(classes_obj):
    """ 查看并获取所选学员函数 """
    student_obj_list = []
    student_id_list = StudentToClasses.get_classes_to_student_list(classes_obj.id)
    for i in student_id_list:  # 通过id获取每一个学员对象
        student_obj_list.append(i.get_obj_by_id())
    print("".center(74, "="))
    print("\033[35;1m%-3s%-5s%-7s%-7s\033[0m" %
          ("编号", "姓名", "年龄", "性别"))
    for index, obj in enumerate(student_obj_list):
        print("\033[35;1m%-5s%-5s%-7s%-10s\033[0m" %
              (index + 1, obj.name, obj.age, obj.sex))
    print("".center(74, "="))
    while True:
        choice = input("请输入学员编号：[tip:输入'q'返回]").strip()
        if choice == "q":
            return
        if len(choice) == 0:
            continue
        try:
            choice = int(choice)
            if 0 < choice <= len(student_obj_list):
                student_obj = student_obj_list[choice - 1]
                break
            else:
                print("\033[31;1m您的输入不在编号范围内，请重新输入！\033[0m")
                continue
        except ValueError:
            print("\033[31;1m您的输入有误，请重新输入！\033[0m")
            continue
    return student_obj


@login_decorator(teacher_status)
def teaching():
    """ 讲师授课函数 """
    teacher_obj = teacher_status["obj"]
    classes_obj = get_classes()
    if classes_obj:  # 获取班级对象后以下代码才执行
        classrecord_obj = classes_obj.get_classrecord_obj()
        print("目前已有上课节次如下".center(70, '='))
        for i in classrecord_obj.section:
            print(i)
        while True:
            current_section = input("请输入本节课节次：[Tip:输入'q'返回]").strip()
            if current_section == "q":
                return
            if len(current_section) == 0:
                continue
            if current_section in classrecord_obj.section:
                print("\033[31;1m该节次已经存在，请重新输入！\033[0m")
                continue
            classrecord_obj.section.append(current_section)
            break
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_date_timestamp = time.mktime(time.strptime(current_date, "%Y-%m-%d"))
        classes_startdates = classrecord_obj.classes_id.get_obj_by_id().startdates
        classes_startdates_timestamp = time.mktime(time.strptime(classes_startdates, "%Y-%m-%d"))
        if current_date_timestamp < classes_startdates_timestamp:
            print("\033[31;1m本班级还没开课！\033[0m")
            return
        if current_date in classrecord_obj.classdate:
            print("\033[31;1m您今天已经上过课了！\033[0m")
            return
        classrecord_obj.classdate.append(current_date)
        print("\033[32;1m[%s] 上课中，请勿打扰！\033[0m" % teacher_obj.name)
        module.action_logger.info("讲师 [%s] 创建 了一条 [%s] [%s]"
                                  % (teacher_obj.name, str(classrecord_obj), current_section))
        classrecord_obj.save()  # 将新的上课记录对象存入文件中
        time.sleep(2)


@login_decorator(teacher_status)
def view_classes():
    """ 查看班级 """
    teacher_obj = teacher_status["obj"]
    classes_obj = get_classes()
    if not classes_obj:
        return
    student_obj = get_student(classes_obj)
    if not student_obj:
        return
    classrecord_obj = classes_obj.get_classrecord_obj()
    studyrecord_obj = student_obj.get_studyrecord_by_classrecord_id(classrecord_obj.id)
    print("".center(74, "="))
    print("\033[35;1m%-3s%-7s%-7s%-7s\033[0m" %
          ("编号", "签到日期", "签到状态", "作业成绩"))
    for index, obj in enumerate(studyrecord_obj.signdate):
        print("\033[35;1m%-5s%-13s%-7s%-10s\033[0m" %
              (index + 1, obj, studyrecord_obj.sign[index], studyrecord_obj.score[index]))
    print("".center(74, "="))
    while True:
        choice = input("请输入编号查看作业：[tip:输入'q'返回]").strip()
        if choice == "q":
            return
        if len(choice) == 0:
            continue
        try:
            choice = int(choice)
            if 0 < choice <= len(studyrecord_obj.signdate):
                one_studyrecord_index = choice - 1
                break
            else:
                print("\033[31;1m您的输入不在编号范围内，请重新输入！\033[0m")
                continue
        except ValueError:
            print("\033[31;1m您的输入有误，请重新输入！\033[0m")
            continue
    if studyrecord_obj.homework[one_studyrecord_index]:
        print("学员本次作业如下".center(74, "="))
        print("\033[33;1m%s\033[0m" % studyrecord_obj.homework[one_studyrecord_index])
        print("".center(74, "="))
        while True:
            mark = input("请给本次作业打分：[tip:输入'q'返回]").strip()
            if mark == "q":
                return
            comment = input("请给本次作业写上评语:").strip()
            if len(mark) == 0 or len(comment) == 0:
                continue
            studyrecord_obj.score[one_studyrecord_index] = mark
            studyrecord_obj.note[one_studyrecord_index] = comment
            studyrecord_obj.save()
            print("\033[32;1m修改作业完成!\033[0m")
            module.action_logger.info("讲师 [%s] 为学员[%s] [%s][%s][%s] 进行了评分! "
                                      % (teacher_obj.name, student_obj.name,
                                         classrecord_obj.classes_id.get_obj_by_id().name,
                                         classrecord_obj.classes_id.get_obj_by_id().semester,
                                         classrecord_obj.section[one_studyrecord_index]))
            return
    else:
        print("\033[31;1m学员本次作业没提交!\033[0m")
        time.sleep(1)
        return


def logout():
    """ 注销函数 """
    teacher_status["status"] = None
    teacher_status["user"] = "游客"
    teacher_status["obj"] = None


# 功能编号对应至conf下的exhibition.student_show
teacher_function_match = {
                        "1": lunch_teacher,
                        "2": teaching,
                        "3": view_classes,
                        "4": logout,
                        "5": exit
                        }


def teacher_show():
    while True:
        os.system("cls")
        print(exhibition.teacher_show.format(today=module.today, week=module.week, user=teacher_status["user"]))
        choice = input("请输入您的选项:[Tip:输入'q'返回上一级]").strip()
        if choice == "q":
            return
        if len(choice) == 0:
            continue
        if choice in teacher_function_match:
            teacher_function_match[choice]()
        else:
            print("\033[31;1m您的输入有误请重新输入！\033[0m")
            continue
