#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/7/8
"""
创建表，即初始化数据库专用模块
"""
import os
from core import db_conn
from core import table_structure
from core import utils
from conf.settings import TABLES_DIR


def init_db():
    """初始化数据库"""
    table_structure.BaseModule.metadata.create_all(db_conn.engine)


def drop_db():
    """清空BaseModule下的所有表结构"""
    table_structure.BaseModule.metadata.drop_all(db_conn.engine)


def create_host():
    """创建主机信息"""
    host_file = os.path.join(TABLES_DIR, "host.yaml")
    data = utils.yaml_parser(host_file)
    for k, v in data.items():
        host_obj = table_structure.Host(hostname=k, ip=v.get("ip"), port=v.get("port") or 22)
        db_conn.session.add(host_obj)
    db_conn.session.commit()


def create_host_user():
    """创建主机用户名密码"""
    host_user_file = os.path.join(TABLES_DIR, "host_user.yaml")
    data = utils.yaml_parser(host_user_file)
    for k, v in data.items():
        host_user_obj = table_structure.HostUser(login_type=v.get("login_type"),
                                                 username=v.get("username"),
                                                 password=v.get("password") or ""
                                                 )
        db_conn.session.add(host_user_obj)
    db_conn.session.commit()


def create_user():
    """创建堡垒机用户"""
    user_file = os.path.join(TABLES_DIR, "user.yaml")
    data = utils.yaml_parser(user_file)
    for k, v in data.items():
        user_obj = table_structure.User(username=v.get("username"), password=v.get("password"))
        db_conn.session.add(user_obj)
    db_conn.session.commit()


def create_group():
    """创建分组"""
    group_file = os.path.join(TABLES_DIR, "group.yaml")
    data = utils.yaml_parser(group_file)
    for k, v in data.items():
        group_obj = table_structure.Group(name=v[0])
        db_conn.session.add(group_obj)
    db_conn.session.commit()


def create_bind_host():
    """创建绑定主机"""
    bind_host_file = os.path.join(TABLES_DIR, "bind_host.yaml")
    data = utils.yaml_parser(bind_host_file)
    for k, v in data.items():
        # print(k, v)
        host_info = v.get("host")  # 获取主机信息
        host_obj = db_conn.session.query(table_structure.Host).filter(
            host_info.get("ip") == table_structure.Host.ip).first()

        host_user_info = v.get("hostuser")  # 获取主机用户名密码信息
        login_type = host_user_info.get("login_type")  # 获取主机用户登陆类型
        username = host_user_info.get("username")  # 获取主机用户名
        password = host_user_info.get("password") or ""  # 获取主机用户密码，如果为空则输出""
        host_user_obj = db_conn.session.query(table_structure.HostUser).filter(
            login_type == table_structure.HostUser.login_type,
            username == table_structure.HostUser.username,
            password == table_structure.HostUser.password
        ).first()

        bind_host_obj = table_structure.BindHost(host_id=host_obj.id, host_user_id=host_user_obj.id)
        db_conn.session.add(bind_host_obj)
    db_conn.session.commit()


def create_bind_host_2_group():
    """创建绑定主机对应分组"""
    bind_host_file = os.path.join(TABLES_DIR, "bind_host.yaml")
    data = utils.yaml_parser(bind_host_file)
    for k, v in data.items():
        # print(k, v)
        host_info = v.get("host")  # 获取主机信息
        host_obj = db_conn.session.query(table_structure.Host).filter(
            host_info.get("ip") == table_structure.Host.ip).first()

        host_user_info = v.get("hostuser")  # 获取主机用户名密码信息
        login_type = host_user_info.get("login_type")  # 获取主机用户登陆类型
        username = host_user_info.get("username")  # 获取主机用户名
        password = host_user_info.get("password") or ""  # 获取主机用户密码，如果为空则输出""
        host_user_obj = db_conn.session.query(table_structure.HostUser).filter(
            login_type == table_structure.HostUser.login_type,
            username == table_structure.HostUser.username,
            password == table_structure.HostUser.password
        ).first()

        bind_host_obj = db_conn.session.query(table_structure.BindHost).filter(
            host_obj.id == table_structure.BindHost.host_id,
            host_user_obj.id == table_structure.BindHost.host_user_id,
        ).first()

        group_info = v.get("groups")  # 获取分组信息
        if group_info:  # 如果存在分组则进行分组操作
            for i in group_info:
                group_obj = db_conn.session.query(table_structure.Group).filter(i == table_structure.Group.name).first()
                bind_host_obj.groups.append(group_obj)
    db_conn.session.commit()


def create_user_2_bindhost():
    """创建堡垒机用户对应绑定主机"""
    user_file = os.path.join(TABLES_DIR, "user.yaml")
    data = utils.yaml_parser(user_file)
    for k, v in data.items():
        user_username = v.get("username")
        user_password = v.get("password")
        user_obj = db_conn.session.query(table_structure.User).filter(
            user_username == table_structure.User.username,
            user_password == table_structure.User.password
        ).first()
        bind_host_info = v.get("bindhosts")
        if bind_host_info:
            for bind_host in bind_host_info:
                host_info = bind_host.get("host")  # 获取主机信息
                host_obj = db_conn.session.query(table_structure.Host).filter(
                    host_info.get("ip") == table_structure.Host.ip).first()

                host_user_info = bind_host.get("hostuser")  # 获取主机用户名密码信息
                login_type = host_user_info.get("login_type")  # 获取主机用户登陆类型
                username = host_user_info.get("username")  # 获取主机用户名
                password = host_user_info.get("password") or ""  # 获取主机用户密码，如果为空则输出""
                host_user_obj = db_conn.session.query(table_structure.HostUser).filter(
                    login_type == table_structure.HostUser.login_type,
                    username == table_structure.HostUser.username,
                    password == table_structure.HostUser.password
                ).first()

                bind_host_obj = db_conn.session.query(table_structure.BindHost).filter(
                    host_obj.id == table_structure.BindHost.host_id,
                    host_user_obj.id == table_structure.BindHost.host_user_id,
                ).first()
                user_obj.bind_hosts.append(bind_host_obj)
    db_conn.session.commit()


def create_user_2_group():
    """创建堡垒机用户对应分组"""
    user_file = os.path.join(TABLES_DIR, "user.yaml")
    data = utils.yaml_parser(user_file)
    for k, v in data.items():
        user_username = v.get("username")
        user_password = v.get("password")
        user_obj = db_conn.session.query(table_structure.User).filter(
            user_username == table_structure.User.username,
            user_password == table_structure.User.password
        ).first()
        group_info = v.get("groups")
        if group_info:
            for group in group_info:
                group_name = group
                group_obj = db_conn.session.query(table_structure.Group).filter(
                    group_name == table_structure.Group.name).first()
                user_obj.groups.append(group_obj)
    db_conn.session.commit()


def run():
    """初始化数据库"""
    drop_db()
    init_db()
    create_host()
    create_host_user()
    create_user()
    create_group()
    create_bind_host()
    create_bind_host_2_group()
    create_user_2_bindhost()
    create_user_2_group()
