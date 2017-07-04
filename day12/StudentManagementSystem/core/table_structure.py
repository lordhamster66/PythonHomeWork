#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/26
"""
表结构定义模块
"""
from conf import settings
from sqlalchemy import create_engine, Table, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, Date


# 数据库连接信息
DB_CONNECT_STRING = "{db_type}+{db_connect}://{user}:{password}@{host}:{port}/{db}?charset={charset}".format(
    db_type=settings.DB_INFO["db_type"], db_connect=settings.DB_INFO["db_connect"],
    user=settings.DB_INFO["user"], password=settings.DB_INFO["password"],
    host=settings.DB_INFO["host"], port=settings.DB_INFO["port"],
    db=settings.DB_INFO["db"], charset=settings.DB_INFO["charset"]
)

# 创建一个连接引擎
engine = create_engine(
    DB_CONNECT_STRING,
    # echo=True
)

# 创建一个基类
BaseModule = declarative_base()


def init_db():
    """初始化数据库"""
    BaseModule.metadata.create_all(engine)


def drop_db():
    """清空BaseModule下的所有表结构"""
    BaseModule.metadata.drop_all(engine)


class Teacher(BaseModule):
    """讲师表结构"""

    __tablename__ = "teacher"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(32), nullable=False)
    age = Column(Integer, nullable=False)
    username = Column(String(32), nullable=False)
    password = Column(String(32), nullable=False)

    def __repr__(self):
        return "<name:%s>" % self.name

    __str__ = __repr__

# 学员关联班级表
stu_classes = Table(
    "stu_classes", BaseModule.metadata,
    Column("student_id", Integer, ForeignKey("student.id")),
    Column("class_id", Integer, ForeignKey("class.id"))
)


class Student(BaseModule):
    """学员表结构"""

    __tablename__ = "student"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(32), nullable=False)
    age = Column(Integer, nullable=False)
    qq = Column(Integer, nullable=False)
    username = Column(String(32), nullable=False)
    password = Column(String(32), nullable=False)
    classes = relationship("Class", secondary=stu_classes, backref="students")

    def __repr__(self):
        return "<name:%s, age:%s, qq:%s>" % (self.name, self.age, self.qq)

    __str__ = __repr__


class Class(BaseModule):
    """班级表结构"""

    __tablename__ = "class"

    id = Column(Integer, autoincrement=True, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    name = Column(String(32), nullable=False)
    class_teacher = relationship("Teacher", backref="teacher_class")

    def __repr__(self):
        return "%s" % self.name

    __str__ = __repr__


class ClassRecord(BaseModule):
    """班级上课记录表结构"""

    __tablename__ = "class_record"

    id = Column(Integer, autoincrement=True, primary_key=True)
    class_id = Column(Integer, ForeignKey("class.id"))
    qdate = Column(Date, nullable=False)
    node = Column(Integer, nullable=False)
    info = Column(String(32), nullable=False)
    clsrcd_class = relationship("Class", backref="class_clsrcd")

    def __repr__(self):
        return "<classname:%s, node:%s, info:%s>" % (self.clsrcd_class.name, self.node, self.info)

    __str__ = __repr__


class StudyRecord(BaseModule):
    """学员上课记录表结构"""

    __tablename__ = "study_record"

    id = Column(Integer, autoincrement=True, primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"))
    class_record_id = Column(Integer, ForeignKey("class_record.id"))
    sign_status = Column(String(32), default="未签到")
    homework_status = Column(String(32), default="未交")
    score = Column(Integer, nullable=False, default=0)
    styrcd_student = relationship("Student", backref="student_styrcd")
    styrcd_clsrcd = relationship("ClassRecord", backref="clsrcd_styrcd")

    def __repr__(self):
        return "<stuname:%s, clasname:%s, node:%s, sign_status:%s, homework_status:%s, score:%s>" % (
            self.styrcd_student.name, self.styrcd_clsrcd.clsrcd_class.name, self.styrcd_clsrcd.node,
            self.sign_status, self.homework_status, self.score
        )

    __str__ = __repr__
