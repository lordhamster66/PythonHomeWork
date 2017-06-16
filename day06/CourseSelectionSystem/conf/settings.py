#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/7

import os
import logging

# 路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADMIN_DIR = os.path.join(BASE_DIR, "db", "admin")
SCHOOL_DIR = os.path.join(BASE_DIR, "db", "school")
COURSE_DIR = os.path.join(BASE_DIR, "db", "course")
CLASSES_DIR = os.path.join(BASE_DIR, "db", "classes")
CLASSRECORD_DIR = os.path.join(BASE_DIR, "db", "classrecord")
STUDYRECORD_DIR = os.path.join(BASE_DIR, "db", "studyrecord")
STUDENT_DIR = os.path.join(BASE_DIR, "db", "student")
TEACHER_DIR = os.path.join(BASE_DIR, "db", "teacher")
STUDENTTOCLASSES_DIR = os.path.join(BASE_DIR, "db", "studenttoclasses")

# 类对应路径
MATCH_DIR = {
            "admin": ADMIN_DIR,
            "school": SCHOOL_DIR,
            "course": COURSE_DIR,
            "classes": CLASSES_DIR,
            "classrecord": CLASSRECORD_DIR,
            "studyrecord": STUDYRECORD_DIR,
            "student": STUDENT_DIR,
            "teacher": TEACHER_DIR,
            "studenttoclasses": STUDENTTOCLASSES_DIR,
            }

# 可注册角色列表
CAN_ENROLL = {"Admin": "管理员", "Teacher": "讲师", "Student": "学员"}

# 日志类型
LOG_TYPE = {
            "action": "action.log",
            "manage": "manage.log"
           }

# 设置日志显示级别
LOG_LEVEL = {
            "global_level": logging.INFO,
            "ch_level": logging.WARNING,
            "fh_level": logging.INFO
            }

# 班级学员人数限制
limit_student_num = 60


if __name__ == '__main__':
    print(BASE_DIR)
    print(SCHOOL_DIR)
    print(COURSE_DIR)
    print(CLASSES_DIR)
