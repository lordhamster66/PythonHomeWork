#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/7/8
"""
数据库连接模块
"""
from sqlalchemy import create_engine, Table  # sqlalchemy相关模块
from sqlalchemy.orm import sessionmaker  # 创建session实例相关模块

from conf import settings  # 导入配置信息

DB_CONNECT_STRING = "{db_type}+{db_connect}://{user}:{password}@{host}:{port}/{db}?charset={charset}".format(
    db_type=settings.DB_INFO["db_type"], db_connect=settings.DB_INFO["db_connect"],
    user=settings.DB_INFO["user"], password=settings.DB_INFO["password"],
    host=settings.DB_INFO["host"], port=settings.DB_INFO["port"],
    db=settings.DB_INFO["db"], charset=settings.DB_INFO["charset"]
)

engine = create_engine(DB_CONNECT_STRING)  # 创建数据库连接引擎
# engine = create_engine(DB_CONNECT_STRING)

SessionCls = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = SessionCls()  # 创建session实例
