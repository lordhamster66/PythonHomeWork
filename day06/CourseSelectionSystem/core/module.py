#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/6
import pickle
import os
import time
import datetime
from core import idmaker            # 导入创建唯一ID模块
from conf import settings           # 导入配置文件
from core.mylogger import mylogger  # 导入自定义日志模块

# 生成两种日志对象
action_logger = mylogger("action")             # 行为日志
manage_logger = mylogger("manage")             # 管理日志

# 生成日期，星期
week_list = ("一", "二", "三", "四", "五", "六", "日")       # 星期对照表
today = time.strftime("%Y-%m-%d", time.localtime())         # 获取今天的日期
week = week_list[int(datetime.datetime.now().weekday())]    # 获取星期


class BaseClass(object):
    """ 基础类 """
    def save(self):
        """
        保存函数，保存每个对象
        :return:
        """
        base_name = os.path.basename(self.db_path)
        file_dir = settings.MATCH_DIR[base_name]
        file_path = os.path.join(file_dir, str(self.id))
        pickle.dump(self, open(file_path, "wb"))

    @classmethod
    def get_all_obj(cls):
        """
        此类方法可以返回一个类生成的所有对象
        :return: 返回对象列表
        """
        base_name = os.path.basename(cls.db_path)
        file_dir = settings.MATCH_DIR[base_name]
        obj_list = []
        for file_name in os.listdir(file_dir):
            file_path = os.path.join(file_dir, file_name)
            obj = pickle.load(open(file_path, "rb"))
            obj_list.append(obj)
        return obj_list

    def enroll(self):
        """ 注册方法 """
        class_name = self.__class__.__name__
        if class_name in settings.CAN_ENROLL:  # 如过类名在可注册字典里则可以进行注册
            while True:
                username = input("请输入用户名:").strip()
                password = input("请输入密码:").strip()
                if len(username) == 0:
                    continue
                if len(password) == 0:
                    continue
                for obj in self.__class__.get_all_obj():  # 通过类名来获取该类生成的所有对象
                    if username == obj.username:
                        print("用户名已经存在！")
                        return
                self.username = username
                self.password = password
                self.save()
                action_logger.info("%s-%s注册了该系统！" % (settings.CAN_ENROLL[class_name], self.name))
                print("\033[31;1m%s-%s注册成功！\033[0m" % (settings.CAN_ENROLL[class_name], self.name))
                break
        else:
            raise Exception("%s类不可进行注册" % class_name)

    @classmethod
    def login(cls):
        status = 2
        obj = None
        data = '\033[31;1m用户名或密码错误\033[0m'
        class_name = cls.__name__
        if class_name in settings.CAN_ENROLL:  # 如果类名在可注册字典里则其可以进行登陆
            try:
                while True:
                    username = input("请输入您的用户名:").strip()
                    password = input("请输入您的密码:").strip()
                    if len(username) == 0 or len(password) == 0:
                        continue
                    obj_list = cls.get_all_obj()  # 通过类名获取该类下的所有对象
                    for obj in obj_list:
                        if username == obj.username and password == obj.password:
                            status = 1
                            obj = obj
                            data = '\033[32;1m登录成功\033[0m'
                            action_logger.info("%s-%s登陆了该系统！" % (settings.CAN_ENROLL[class_name], obj.name))
                            break
                    break
            except Exception as e:
                status = 0
                obj = None
                data = e
        return {"status": status, "obj": obj, "data": data}


class Admin(BaseClass):
    """ 管理员类 """
    db_path = settings.ADMIN_DIR

    def __init__(self, name):
        self.id = idmaker.MakeId(self.db_path)
        self.name = name

    def __str__(self):
        return self.name


class School(BaseClass):
    """ 学校类 """
    db_path = settings.SCHOOL_DIR

    def __init__(self, name, address, city):
        self.id = idmaker.MakeId(self.db_path)
        self.name = name
        self.address = address
        self.city = city
        self.create_time = time.strftime("%Y-%m-%d")

    def __str__(self):
        return self.name


class Course(BaseClass):
    """ 课程类 """
    db_path = settings.COURSE_DIR

    def __init__(self, name, cycle, price, school_id):
        self.id = idmaker.MakeId(self.db_path)
        self.name = name
        self.cycle = cycle
        self.price = price
        self.school_id = school_id

    def __str__(self):
        return self.name


class Classes(BaseClass):
    """ 班级类 """
    db_path = settings.CLASSES_DIR

    def __init__(self, name, semester, course_id, startdates, school_id, teacher_id):
        self.id = idmaker.MakeId(self.db_path)
        self.name = name
        self.semester = semester
        self.course_id = course_id
        self.startdates = startdates
        self.school_id = school_id
        self.teacher_id = teacher_id

    def check_student_num(self):
        """ 查看某班级学员人数 """
        student_id_list = StudentToClasses.get_classes_to_student_list(self.id)
        student_num = len(student_id_list)
        return student_num

    def get_classrecord_obj(self):
        """ 查找班级对应上课记录对象 """
        classrecord_obj = None
        classrecord_list = ClassRecord.get_all_obj()
        for obj in classrecord_list:
            if obj.classes_id.id == self.id.id:
                classrecord_obj = obj
        return classrecord_obj

    def __str__(self):
        return self.name


class ClassRecord(BaseClass):
    """ 上课记录类 """
    db_path = settings.CLASSRECORD_DIR

    def __init__(self, classes_id, section, classdate):
        self.id = idmaker.MakeId(self.db_path)
        self.classes_id = classes_id
        self.section = section
        self.classdate = classdate

    def __str__(self):
        classes_name = self.classes_id.get_obj_by_id().name
        classes_semester = self.classes_id.get_obj_by_id().semester
        return "%s%s班级上课记录" % (classes_name, classes_semester)


class StudyRecord(BaseClass):
    """ 学习记录类 """
    db_path = settings.STUDYRECORD_DIR

    def __init__(self, classrecord_id, sign, signdate, score, student_id, homework, note):
        self.id = idmaker.MakeId(self.db_path)
        self.classrecord_id = classrecord_id
        self.sign = sign
        self.signdate = signdate
        self.score = score
        self.student_id = student_id
        self.homework = homework
        self.note = note


class Teacher(BaseClass):
    """ 教师类 """
    db_path = settings.TEACHER_DIR

    def __init__(self, name, age, sex, school_id):
        self.id = idmaker.MakeId(self.db_path)
        self.name = name
        self.age = age
        self.sex = sex
        self.school_id = school_id

    def get_classes_obj(self):
        """ 查找讲师对应班级对象 """
        classes_obj_list = []  # 存储该讲师所对应的所有班级对象
        class_list = Classes.get_all_obj()
        for obj in class_list:
            if obj.teacher_id.id == self.id.id:
                classes_obj_list.append(obj)
        return classes_obj_list

    def __str__(self):
        return self.name


class Student(BaseClass):
    """ 学员类 """
    db_path = settings.STUDENT_DIR

    def __init__(self, name, age, sex, qq, phone):
        self.id = idmaker.MakeId(self.db_path)
        self.name = name
        self.age = age
        self.sex = sex
        self.qq = qq
        self.phone = phone
        self.want_classes = []
        self._tuition = 0

    def pay_tuition(self, course_obj):
        """ 交学费 """
        course_name = course_obj.name
        course_price = int(course_obj.price)
        while True:
            print("\033[32;1m课程[%s]的价格为\033[0m[\033[31;1m%s\033[0m]!" % (course_name, course_price))
            your_price = input(
                "\033[32;1m请输入您想交的学费[tip:输入\033[0m\033[31;1m'q'\033[0m\033[32;1m返回]：\033[0m").strip()
            if your_price == "q":
                return
            if len(your_price) == 0:
                continue
            try:
                your_price = int(your_price)
                if your_price == course_price:
                    self._tuition += your_price
                    print("\033[32;1m学费提交完成!\033[0m")
                    action_logger.info("[%s]为其报名的课程[%s]交了学费！" % (self.name, course_name))
                    return "done"
                elif your_price < course_price:
                    print("\033[31;1m钱不够！\033[0m")
                    continue
                else:
                    print("\033[31;1m您不用交这么多！\033[0m")
                    continue
            except ValueError:
                print("\033[31;1m输入不规范，请重新输入!\033[0m")
                continue

    def get_studyrecord_by_classrecord_id(self, classrecord_id):
        """ 通过上课记录对象id寻找学习记录对象 """
        studyrecord_obj = None
        studyrecord_list = StudyRecord.get_all_obj()
        for obj in studyrecord_list:
            if obj.student_id.id == self.id.id and obj.classrecord_id.id == classrecord_id.id:
                studyrecord_obj = obj
        return studyrecord_obj

    def __str__(self):
        return self.name


class StudentToClasses(BaseClass):
    """ 学员班级多对多关联类 """
    db_path = settings.STUDENTTOCLASSES_DIR

    def __init__(self, student_id, classes_id):
        self.id = idmaker.MakeId(self.db_path)
        self.student_id = student_id
        self.classes_id = classes_id

    @classmethod
    def get_student_to_classes_list(cls, student_id):
        """ 获取学员所对应的班级id """
        obj_list = cls.get_all_obj()
        classes_id_list = []  # 学员对应班级id列表
        if obj_list:
            for obj in obj_list:
                if obj.student_id.id == student_id.id:
                    classes_id_list.append(obj.classes_id)
        return classes_id_list

    @classmethod
    def get_classes_to_student_list(cls, classes_id):
        """ 获取班级所对应的学员id """
        obj_list = cls.get_all_obj()
        student_id_list = []  # 学员对应班级id列表
        if obj_list:
            for obj in obj_list:
                if obj.classes_id.id == classes_id.id:
                    student_id_list.append(obj.student_id)
        return student_id_list




