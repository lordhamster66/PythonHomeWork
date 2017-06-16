#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/7
import os
import time
from core.module import Admin
from core.module import School
from core.module import Teacher
from core.module import Classes
from core.module import Course
from core.module import ClassRecord
from core.module import Student
from core.module import StudyRecord
from core.module import StudentToClasses
from core import module
from lib.public import login_decorator  # 登陆验证装饰器
from conf import exhibition  # 界面显示模板
from conf import settings

# 状态管理
admin_status = {"status": None, "user": "游客"}


def create_admin():
    """ 管理员注册 """
    name = input("请输入您的姓名：").strip()
    admin = Admin(name)
    admin.enroll()


def lunch_admin():
    """ 管理员登陆 """
    ret = Admin.login()
    print(ret["data"])
    admin_status["status"] = ret["status"]
    if ret["status"] == 1:
        admin_status["user"] = ret["obj"].name


@login_decorator(admin_status)
def create_school():
    """ 创建学校 """
    name = input("请输入学校名称：").strip()
    address = input("请输入学校地址：").strip()
    city = input("请输入学校所在城市：").strip()
    school_list = [(obj.name, obj.address) for obj in School.get_all_obj()]
    if (name, address) in school_list:
        print('\033[31;1m[%s] [%s]校区 已经存在,不可重复创建\033[0m' % (name, city))
        return
    school_obj = School(name, address, city)
    school_obj.save()
    print('\033[35;1m[%s] [%s]校区 创建成功\033[0m' % (name, city))
    module.manage_logger.info("[%s] [%s]校区 创建成功" % (name, city))


@login_decorator(admin_status)
def show_school():
    """ 展示学校 """
    print("".center(74, "="))
    print("\033[35;1m%-3s%-8s%-10s%-8s%-30s\033[0m" %
          ("编号", "学校", "创建日期", "市区", "地址"))
    for index, obj in enumerate(School.get_all_obj()):
        print("\033[35;1m%-5s%-7s%-13s%-8s%-30s\033[0m" %
              (index + 1, obj.name, obj.create_time, obj.city,  obj.address))
    print("".center(74, "="))
    while True:
        choice = input("请输入'q'返回：").strip()
        if len(choice) == 0:
            continue
        if choice == "q":
            return
        else:
            print("\033[31;1m输入有误，请重新输入！\033[0m")
            continue


@login_decorator(admin_status)
def create_course():
    """ 创建课程 """
    name = input("请输入您想创建的课程名称：").strip()
    cycle = input("请输入课程周期：").strip()
    price = input("请输入课程价格：").strip()
    school_list = School.get_all_obj()
    for index, obj in enumerate(school_list):
        print(index+1, obj.name, obj.address)
    choice = int(input("请选择学校编号：").strip())
    school_obj = school_list[choice-1]
    course_list = [(obj.name, obj.school_id.id) for obj in Course.get_all_obj()]
    if (name, school_obj.id.id) in course_list:
        print('\033[31;1m课程 [%s] 已经存在,不可重复创建\033[0m' % name)
        return
    course_obj = Course(name, cycle, price, school_obj.id)
    course_obj.save()
    print('\033[35;1m课程 [%s] 创建成功\033[0m' % name)
    module.manage_logger.info("课程 [%s] 创建成功" % name)


@login_decorator(admin_status)
def show_course():
    """ 展示课程 """
    print("".center(74, "="))
    print("\033[35;1m%-3s%-8s%-8s%-8s%-8s%-10s\033[0m" %
          ("编号", "课程", "周期", "价格", "学校", "学校地址"))
    for index, obj in enumerate(Course.get_all_obj()):
        print("\033[35;1m%-5s%-10s%-10s%-8s%-8s%-10s\033[0m" %
              (index + 1, obj.name, obj.cycle, obj.price,
               obj.school_id.get_obj_by_id().name, obj.school_id.get_obj_by_id().address))
    print("".center(74, "="))
    while True:
        choice = input("请输入'q'返回：").strip()
        if len(choice) == 0:
            continue
        if choice == "q":
            return
        else:
            print("\033[31;1m输入有误，请重新输入！\033[0m")
            continue


@login_decorator(admin_status)
def create_teacher():
    """ 创建讲师 """
    while True:
        name = input("请输入讲师姓名：").strip()
        age = input("请输入讲师年龄：").strip()
        sex = input("请输入讲师性别：").strip()
        if len(name) == 0 or len(age) == 0 or len(sex) == 0:
            continue
        if not age.isdigit():
            print("\033[31;1m年龄必须为数字\033[0m")
            continue
        while True:
            school_list = School.get_all_obj()
            if len(school_list) == 0:
                print("\033[31;1m请创建学校！\033[0m")
                return
            print("".center(30, "="))
            print("%-3s%-5s%-5s" % ("编号", "学校名称", "学校地址"))
            for index, obj in enumerate(school_list):
                print("%-5s%-6s%-5s" % (index+1, obj.name, obj.address))
            print("".center(30, "="))
            choice = input("请输入您想关联的学校的编号:").strip()
            if choice == "q":
                return
            try:
                choice = int(choice)
                if 0 < choice <= len(school_list):
                    school_obj = school_list[choice-1]
                    school_id = school_obj.id
                    print("\033[32;1m学校 [%s] 关联成功\033[0m" % school_obj.name)
                    break
                else:
                    print("\033[31;1m不在编码范围内!\033[0m")
                    continue
            except ValueError:
                print("\033[31;1m输入不规范，请重新输入！\033[0m")
                continue
        teacher_obj = Teacher(name, age, sex, school_id)
        print("请为讲师创建初始用户名和密码，谢谢！")
        teacher_obj.enroll()
        module.manage_logger.info("讲师 [%s] 记录创建成功" % name)
        return


@login_decorator(admin_status)
def show_teacher():
    """ 展示讲师 """
    print("".center(74, "="))
    print("\033[35;1m%-3s%-8s%-8s%-8s%-8s\033[0m" %
          ("编号", "讲师", "年龄", "性别", "学校"))
    for index, obj in enumerate(Teacher.get_all_obj()):
        print("\033[35;1m%-5s%-10s%-10s%-8s%-10s\033[0m" %
              (index + 1, obj.name, obj.age, obj.sex, obj.school_id.get_obj_by_id().name))
    print("".center(74, "="))
    while True:
        choice = input("请输入'q'返回：").strip()
        if len(choice) == 0:
            continue
        if choice == "q":
            return
        else:
            print("\033[31;1m输入有误，请重新输入！\033[0m")
            continue


@login_decorator(admin_status)
def create_classes():
    """ 创建班级 """
    exit_flag = False
    while not exit_flag:
        name = input("请输入您想创建的班级名称:").strip()
        semester = input("请输入所在班级属于第几期:").strip()
        if len(name) == 0 or len(semester) == 0:
            continue
        classes_list = [(obj.name, obj.semester) for obj in Classes.get_all_obj()]
        if (name, semester) in classes_list:
            print('\033[31;1m班级 [%s] [%s] 已经存在,不可重复创建\033[0m' % (name, semester))
            return
        while True:
            school_list = School.get_all_obj()
            if len(school_list) == 0:
                print("\033[31;1m请创建学校！\033[0m")
                return
            print("".center(30, "="))
            print("%-3s%-5s%-5s" % ("编号", "学校名称", "学校地址"))
            for index, obj in enumerate(school_list):
                print("%-5s%-6s%-5s" % (index+1, obj.name, obj.address))
            print("".center(30, "="))
            choice1 = input("请输入您想关联的学校的编号:").strip()
            if choice1 == "q":
                return
            try:
                choice1 = int(choice1)
                if 0 < choice1 <= len(school_list):
                    school_obj = school_list[choice1-1]
                    school_id = school_obj.id
                    print("\033[32;1m学校 [%s] 关联成功\033[0m" % school_obj.name)
                    break
                else:
                    print("\033[31;1m不在编码范围内!\033[0m")
                    continue
            except ValueError:
                print("\033[31;1m输入不规范，请重新输入！\033[0m")
                continue
        while True:
            course_list = Course.get_all_obj()
            if len(course_list) == 0:
                print("\033[31;1m请创建课程！\033[0m")
                return
            print("".center(30, "="))
            print("%-3s%-5s%-5s%-10s" % ("编号", "课程名称", "课程周期", "课程价格"))
            for index, obj in enumerate(course_list):
                print("%-5s%-10s%-5s%-10s" % (index+1, obj.name, obj.cycle, obj.price))
            print("".center(30, "="))
            choice2 = input("请输入您想关联的课程的编号:").strip()
            if choice2 == "q":
                return
            try:
                choice2 = int(choice2)
                if 0 < choice2 <= len(course_list):
                    course_obj = course_list[choice2-1]
                    course_id = course_obj.id
                    print("\033[32;1m课程 [%s] 关联成功\033[0m" % course_obj.name)
                    break
                else:
                    print("\033[31;1m不在编码范围内!\033[0m")
                    continue
            except ValueError:
                print("\033[31;1m输入不规范，请重新输入！\033[0m")
                continue
        startdates = input("请输入开课日期:").strip()
        while True:
            teacher_list = Teacher.get_all_obj()
            if len(teacher_list) == 0:
                print("\033[31;1m请创建讲师！\033[0m")
                return
            print("".center(30, "="))
            print("%-3s%-5s" % ("编号", "讲师姓名"))
            for index, obj in enumerate(teacher_list):
                print("%-5s%-10s" % (index+1, obj.name))
            print("".center(30, "="))
            choice3 = input("请输入您想关联的讲师的编号:").strip()
            if choice3 == "q":
                return
            try:
                choice3 = int(choice3)
                if 0 < choice3 <= len(teacher_list):
                    teacher_obj = teacher_list[choice3-1]
                    teacher_id = teacher_obj.id
                    print("\033[32;1m讲师 [%s] 关联成功\033[0m" % teacher_obj.name)
                    break
                else:
                    print("\033[31;1m不在编码范围内!\033[0m")
                    continue
            except ValueError:
                print("\033[31;1m输入不规范，请重新输入！\033[0m")
                continue
        classes_obj = Classes(name, semester, course_id, startdates, school_id, teacher_id)
        classes_obj.save()
        classes_id = classes_obj.id
        section = []  # 上课记录节次
        classdate = []  # 上课记录中的上课日期
        classrecord_obj = ClassRecord(classes_id, section, classdate)
        classrecord_obj.save()
        print('\033[35;1m班级 [%s] [%s] 创建成功\033[0m' % (name, semester))
        module.manage_logger.info("班级 [%s] [%s] 创建成功" % (name, semester))
        module.manage_logger.info("班级 [%s] [%s] 上课记录创建成功" % (name, semester))
        return


@login_decorator(admin_status)
def show_classes():
    """ 展示班级 """
    print("".center(74, "="))
    print("\033[35;1m%-5s%-15s%-8s%-10s%-10s%-15s\033[0m" %
          ("编号", "班级", "学期", "课程", "学校", "讲师"))
    for index, obj in enumerate(Classes.get_all_obj()):
            print("\033[35;1m%-5s%-15s%-7s%-10s%-10s%-10s\033[0m" %
                  (index+1, obj.name, obj.semester, obj.course_id.get_obj_by_id().name,
                   obj.school_id.get_obj_by_id().name, obj.teacher_id.get_obj_by_id().name))
    print("".center(74, "="))
    while True:
        choice = input("请输入'q'返回：").strip()
        if len(choice) == 0:
            continue
        if choice == "q":
            return
        else:
            print("\033[31;1m输入有误，请重新输入！\033[0m")
            continue


@login_decorator(admin_status)
def manage_student():
    """ 管理学员  """
    student_list = Student.get_all_obj()  # 学员对象列表
    need_match_list = []  # 需要关联的班级列表
    if len(student_list) == 0:
        print("\033[31;1m目前没有学员使用该系统！\033[0m")
        time.sleep(1)
        return
    print("".center(74, "="))
    print("\033[35;1m%-3s%-5s%-5s%-5s\033[0m" %
          ("编号", "学员姓名", "学员年龄", "学员性别"))
    for index, obj in enumerate(student_list):
        print("\033[35;1m%-5s%-10s%-7s%-10s\033[0m" %
              (index+1, obj.name, obj.age, obj.sex))
    print("".center(74, "="))
    while True:
        student_choice = input("请选择学员编号：[tip:输入'q'返回]").strip()
        if student_choice == "q":
            return
        if len(student_choice) == 0:
            return
        try:
            student_choice = int(student_choice)
            if 0 < student_choice <= len(student_list):
                student_obj = student_list[student_choice-1]
                break
            else:
                print("\033[31;1m不在编码范围内!\033[0m")
                continue
        except ValueError:
            print("\033[31;1m输入不规范，请重新输入！\033[0m")
            continue
    student_want_classes = student_obj.want_classes
    if len(student_want_classes) == 0:
        print("\033[31;1m该学员并没有报名任何班级！\033[0m")
        time.sleep(1)
        return
    for i in student_want_classes:
        need_match_list.append(i.get_obj_by_id())
    print("".center(74, "="))
    print("\033[35;1m%-3s%-15s%-8s%-8s%-5s%-5s%-30s\033[0m" %
          ("编号", "所报班级名称", "学期", "课程", "老师", "学校", "学校地址"))
    for index, obj in enumerate(need_match_list):
        print("\033[35;1m%-5s%-14s%-8s%-10s%-5s%-5s%-30s\033[0m" %
              (index + 1, obj.name, obj.semester, obj.course_id.get_obj_by_id().name,
               obj.teacher_id.get_obj_by_id().name, obj.school_id.get_obj_by_id().name,
               obj.school_id.get_obj_by_id().address))
    print("".center(74, "="))
    while True:
        choice = input("请选择编号为其关联班级和学校：[tip:输入'q'返回]").strip()
        if choice == "q":
            return
        if len(choice) == 0:
            continue
        try:
            choice = int(choice)
            if 0 < choice <= len(need_match_list):
                student_want_classes_obj = need_match_list[choice-1]
                student_num = student_want_classes_obj.check_student_num()
                if student_num < settings.limit_student_num:  # 班级已有学生数量小于限制数量，则可以添加学员
                    classes_id = student_want_classes_obj.id
                    school_obj = student_want_classes_obj.school_id.get_obj_by_id()

                    # 以下代码生成学习记录对象
                    classrecord_id = student_want_classes_obj.get_classrecord_obj().id  # 上课记录id
                    sign = []  # 签到状态
                    signdate = []  # 签到日期
                    score = []  # 成绩
                    student_id = student_obj.id  # 学员id
                    homework = []  # 作业
                    note = []  # 上课信息
                    study_record_obj = StudyRecord(classrecord_id, sign, signdate, score, student_id, homework, note)

                    # 以下代码生成学员与班级关联对象
                    student_to_classes_obj = StudentToClasses(student_obj.id, classes_id)

                    # 将关联成功的班级从学员所报班级列表中删除
                    student_obj.want_classes.pop(choice-1)

                    # 将各种对象存储至文件
                    student_obj.save()
                    study_record_obj.save()
                    student_to_classes_obj.save()

                    # 以下为屏幕输出及日志打印
                    print("\033[32;1m学员 [%s] 关联班级 [%s] 学校 [%s] 成功!\033[0m" %
                          (student_obj.name, student_want_classes_obj.name, school_obj.name))
                    module.manage_logger.info("学员 [%s] 关联班级 [%s] 学校 [%s] 成功！" %
                                              (student_obj.name, student_want_classes_obj.name, school_obj.name))
                    module.manage_logger.info("学员 [%s] 对应班级 [%s] 学习记录创建成功！" %
                                              (student_obj.name, student_want_classes_obj.name))
                    module.manage_logger.info("学员 [%s] 关联班级 [%s] 对应表创建成功！" %
                                              (student_obj.name, student_want_classes_obj.name))
                    return
                else:
                    print("\033[31;1m班级学员已满，请管理员采取其他方案！\033[0m")
                    time.sleep(1)  # TODO(Breakering) 以后需要添加换班操作
                    return
            else:
                print("\033[31;1m不在编码范围内!\033[0m")
                continue
        except ValueError:
            print("\033[31;1m输入不规范，请重新输入！\033[0m")
            continue


def logout():
    """ 注销函数 """
    admin_status["status"] = None
    admin_status["user"] = "游客"

# 功能编号对应至conf下的exhibition.manage_show
admin_function_match = {
                        "1": create_admin,
                        "2": lunch_admin,
                        "3": create_school,
                        "4": show_school,
                        "5": create_course,
                        "6": show_course,
                        "7": create_teacher,
                        "8": show_teacher,
                        "9": create_classes,
                        "10": show_classes,
                        "11": manage_student,
                        "12": logout,
                        "13": exit
                        }


def admin_show():
    while True:
        os.system("cls")
        print(exhibition.manage_show.format(today=module.today, week=module.week, user=admin_status["user"]))
        choice = input("请输入您的选项:[Tip:输入'q'返回上一级]").strip()
        if choice == "q":
            return
        if len(choice) == 0:
            continue
        if choice in admin_function_match:
            admin_function_match[choice]()
        else:
            print("\033[31;1m您的输入有误请重新输入！\033[0m")
            continue
