#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/9
import os
import time
import datetime
from core import module
from core.module import Student
from core.module import Course
from core.module import Classes
from core.module import StudentToClasses
from lib.public import login_decorator
from conf import exhibition

# 状态管理
student_status = {"status": None, "user": "游客", "obj": None}


def create_student():
    """ 学员注册 """
    while True:
        print("".center(30, "="))
        name = input("请输入您的姓名：").strip()
        age = input("请输入您的年龄：").strip()
        sex = input("请输入您的性别：").strip()
        qq = input("请输入您的qq号码：").strip()
        phone = input("请输入您的手机号码：").strip()
        if (len(name) == 0 or len(age) == 0 or len(sex) == 0
           or len(qq) == 0 or len(phone) == 0):
            continue
        if not age.isdigit() or not qq.isdigit() or not phone.isdigit():
            print("\033[31;1m年龄，qq号码以及手机号码必须都为数字！\033[0m")
            continue
        student = Student(name, age, sex, qq, phone)
        student.enroll()
        return


def lunch_student():
    """ 学员登陆 """
    ret = Student.login()
    print(ret["data"])
    student_status["status"] = ret["status"]
    if ret["status"] == 1:
        student_status["user"] = ret["obj"].name
        student_status["obj"] = ret["obj"]


def get_classes():
    """ 查看并获取所选班级函数 """
    student_obj = student_status["obj"]
    classes_obj_list = []
    classes_id_list = StudentToClasses.get_student_to_classes_list(student_obj.id)
    for i in classes_id_list:
        classes_obj_list.append(i.get_obj_by_id())
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


@login_decorator(student_status)
def course_report():
    """ 报班 """
    student_obj = student_status["obj"]  # 从状态信息中获取已经登陆的学员对象
    match_courseid_classes_list = []  # 符合学员所选课程的班级列表
    print("".center(74, "="))
    print("\033[35;1m%-3s%-5s%-5s%-5s%-10s%-10s\033[0m" %
          ("编号", "课程名称", "课程周期", "课程价格", "课程所在学校名称", "课程所在学校地址"))
    course_list = Course.get_all_obj()  # 获取所有的课程对象
    if len(course_list) == 0:
        print("\033[31;1m抱歉，目前没有任何开设课程！请下次再来！\033[0m")
        time.sleep(1)
        return
    for index, obj in enumerate(course_list):
        print("\033[35;1m%-5s%-10s%-7s%-10s%-13s%-10s\033[0m" %
              (index+1, obj.name, obj.cycle, obj.price,
               obj.school_id.get_obj_by_id().name,
               obj.school_id.get_obj_by_id().address))
    print("".center(74, "="))
    while True:
        choice = input("请输入您想报的课程的编号：[tip:输入'q'返回]").strip()
        if choice == "q":
            return
        if len(choice) == 0:
            continue
        try:
            choice = int(choice)
            if 0 < choice <= len(course_list):
                course_obj = course_list[choice-1]
                break
            else:
                print("\033[31;1m您的输入不在编号范围内，请重新输入！\033[0m")
                continue
        except ValueError:
            print("\033[31;1m您的输入有误，请重新输入！\033[0m")
            continue
    classes_list = Classes.get_all_obj()
    if len(classes_list) == 0:
        print("\033[31;1m抱歉，目前没有任何班级可供选择！请下次再来！\033[0m")
        time.sleep(1)
        return
    print("目前开设此课程班级如下".center(63, "="))
    print("\033[35;1m%-3s%-15s%-5s%-5s%-10s%-10s\033[0m" %
          ("编号", "班级名称", "学期", "课程", "开课日期", "讲师"))
    for index, obj in enumerate(classes_list):
        if obj.course_id.id == course_obj.id.id:  # 如果班级对象里面的课程id号和学员选择的课程id号相等，则输入该班级信息
            print("\033[35;1m%-3s%-15s%-5s%-8s%-15s%-10s\033[0m" %
                  (index + 1, obj.name, obj.semester, obj.course_id.get_obj_by_id().name,
                   obj.startdates, obj.teacher_id.get_obj_by_id().name))
            match_courseid_classes_list.append(obj)  # 将符合课程的班级添加进列表中
    print("".center(74, "="))
    if len(match_courseid_classes_list) == 0:
        print("\033[31;1m抱歉，目前没有任何班级开设此类课程！请下次再来！\033[0m")
        time.sleep(1)
        return
    while True:
        classes_choice = input(
            "\033[32;1m请输入您想上的班级[tip:输入\033[0m\033[31;1m'q'\033[0m\033[32;1m返回]：\033[0m").strip()
        if classes_choice == "q":
            return
        if len(classes_choice) == 0:
            continue
        try:
            classes_choice = int(classes_choice)
            if 0 < classes_choice <= len(classes_list):
                classes_obj = classes_list[classes_choice - 1]
                for i in student_obj.want_classes:
                    if i.id == classes_obj.id.id:
                        print("\033[31;1m您已经报名了该班级，请不要重复报名！\033[0m")
                        time.sleep(1)
                        return
                classes_id_list = StudentToClasses.get_student_to_classes_list(student_obj.id)
                for i in classes_id_list:
                    if i.id == classes_obj.id.id:
                        print("\033[31;1m您已经报名了该班级，请不要重复报名！\033[0m")
                        time.sleep(1)
                        return
                ret = student_obj.pay_tuition(course_obj)  # 学员对象中自带交学费方法
                if ret:  # 学费提交成功
                    student_obj.want_classes.append(classes_obj.id)
                    student_obj.save()
                    print("\033[32;1m学员[%s]报名了班级[%s][%s]!\033[0m" %
                          (student_obj.name, classes_obj.name, classes_obj.semester))
                    module.action_logger.info("学员[%s]报名了班级[%s][%s]!"
                                              % (student_obj.name, classes_obj.name, classes_obj.semester))
                return
            else:
                print("\033[31;1m您的输入不在编号范围内，请重新输入！\033[0m")
                continue
        except ValueError:
            print("\033[31;1m您的输入有误，请重新输入！\033[0m")
            continue


@login_decorator(student_status)
def study():
    """ 上课 """
    student_obj = student_status["obj"]  # 获取学员对象
    classes_obj = get_classes()  # 获取所选班级对象
    if not classes_obj:
        print("\033[31;1m您没有报班!\033[0m")
        return
    classrecord_obj = classes_obj.get_classrecord_obj()  # 通过班级对象获取上课记录对象
    studyrecord_obj = student_obj.get_studyrecord_by_classrecord_id(classrecord_obj.id)  # 通过学生对象以及上课记录对象获取学习记录对象
    sign_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if len(classrecord_obj.classdate) == 0:
        print("\033[31;1m还没开课!\033[0m")
        return
    # 上课日期和当前日期相同则可以进行上课行为
    if classrecord_obj.classdate[-1] == sign_date:
        # 在上过课的前提下如果上次上课日期和本次日期相同则表明上过课了
        if len(studyrecord_obj.signdate) != 0 and studyrecord_obj.signdate[-1] == sign_date:
            print("\033[31;1m您已经上过课了！\033[0m")
            return
        else:
            current_section = classrecord_obj.section[-1]
            studyrecord_obj.sign.append("签到")
            studyrecord_obj.signdate.append(sign_date)
            studyrecord_obj.score.append(0)
            studyrecord_obj.homework.append(None)
            studyrecord_obj.note.append(None)
            studyrecord_obj.save()
            print("\033[31;1m[%s]上课中！请勿打扰！\033[0m" % student_obj.name)
            module.action_logger.info("学员 [%s] 在 [%s] [%s] [%s] 签到了"
                                      % (student_obj.name, classrecord_obj.classes_id.get_obj_by_id().name,
                                         classrecord_obj.classes_id.get_obj_by_id().semester,
                                         current_section))
            time.sleep(2)
    else:
        print("\033[31;1m今天不上课，或者老师还没来，嘻嘻！\033[0m")
        return


def get_studyrecord():
    """ 获取学习记录函数 """
    student_obj = student_status["obj"]
    classes_obj = get_classes()
    if not classes_obj:
        print("\033[31;1m您没有报班!\033[0m")
        return
    classrecord_obj = classes_obj.get_classrecord_obj()
    studyrecord_obj = student_obj.get_studyrecord_by_classrecord_id(classrecord_obj.id)
    print("".center(74, "="))
    print("\033[35;1m%-3s%-7s%-7s%-7s%-7s\033[0m" %
          ("编号", "签到日期", "签到状态", "作业成绩", "老师评语"))
    for index, obj in enumerate(studyrecord_obj.signdate):
        print("\033[35;1m%-5s%-13s%-7s%-10s%-7s\033[0m" %
              (index + 1, obj, studyrecord_obj.sign[index],
               studyrecord_obj.score[index], studyrecord_obj.note[index]))
    print("".center(74, "="))
    return studyrecord_obj, classrecord_obj


@login_decorator(student_status)
def hand_homework():
    """ 交作业 """
    student_obj = student_status["obj"]
    studyrecord_obj, classrecord_obj = get_studyrecord()
    if studyrecord_obj:
        while True:
            choice = input("请输入编号交作业：[tip:输入'q'返回]").strip()
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
    while True:
        homework = input("请输入作业内容:[tip:输入'q'返回]").strip()
        if homework == "q":
            return
        if len(homework) == 0:
            continue
        studyrecord_obj.homework[one_studyrecord_index] = homework
        studyrecord_obj.save()
        print("\033[31;1m作业提交成功!\033[0m")
        module.action_logger.info("学员 [%s] 提交了[%s][%s][%s] 的作业"
                                  % (student_obj.name, classrecord_obj.classes_id.get_obj_by_id().name,
                                     classrecord_obj.classes_id.get_obj_by_id().semester,
                                     classrecord_obj.section[one_studyrecord_index]))
        return


@login_decorator(student_status)
def view_score():
    """ 查看成绩函数 """
    get_studyrecord()
    time.sleep(3)


def logout():
    """ 注销函数 """
    student_status["status"] = None
    student_status["user"] = "游客"
    student_status["obj"] = None

# 功能编号对应至conf下的exhibition.student_show
student_function_match = {
                        "1": create_student,
                        "2": lunch_student,
                        "3": course_report,
                        "4": study,
                        "5": hand_homework,
                        "6": view_score,
                        "7": logout,
                        "8": exit
                        }


def student_show():
    while True:
        os.system("cls")
        print(exhibition.student_show.format(today=module.today, week=module.week, user=student_status["user"]))
        choice = input("请输入您的选项:[Tip:输入'q'返回上一级]").strip()
        if choice == "q":
            return
        if len(choice) == 0:
            continue
        if choice in student_function_match:
            student_function_match[choice]()
        else:
            print("\033[31;1m您的输入有误请重新输入！\033[0m")
            continue










