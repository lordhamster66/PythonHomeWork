#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/26
"""
表结构定义模块
"""
from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

# 创建一个基类
BaseModule = declarative_base()

BindHost2Group = Table(
    'bindhost_2_group', BaseModule.metadata,
    Column('bind_host_id', ForeignKey('bind_host.id'), primary_key=True),
    Column('group_id', ForeignKey('group.id'), primary_key=True),
)

User2BindHost = Table(
    'user_2_bindhost', BaseModule.metadata,
    Column('bind_host_id', ForeignKey('bind_host.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True),
)

User2Group = Table(
    'user_2_group', BaseModule.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('group_id', ForeignKey('group.id'), primary_key=True),
)


class User(BaseModule):
    """堡垒机用户表结构"""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), unique=True, nullable=True)
    password = Column(String(128), unique=True, nullable=True)

    groups = relationship('Group', secondary=User2Group)
    bind_hosts = relationship('BindHost', secondary=User2BindHost)

    def __repr__(self):
        return "<User(id='%s',username='%s')>" % (self.id, self.username)


class HostUser(BaseModule):
    """主机用户表结构"""
    __tablename__ = 'host_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login_type = Column(String(64), nullable=True)
    username = Column(String(64), nullable=True)
    password = Column(String(255))

    __table_args__ = (UniqueConstraint('login_type', 'username', 'password', name='_user_passwd_uc'),)

    def __repr__(self):
        return "<HostUser(id='%s',login_type='%s',user='%s')>" % (self.id, self.login_type, self.username)


class Host(BaseModule):
    """主机表结构"""

    __tablename__ = "host"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(64), unique=True, nullable=True)
    ip = Column(String(128), unique=True, nullable=True)
    port = Column(Integer, default=22)

    def __repr__(self):
        return "<Host(id='%s',hostname='%s')>" % (self.id, self.hostname)

    __str__ = __repr__


class Group(BaseModule):
    """分组表结构"""

    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True, unique=True)

    bind_hosts = relationship("BindHost", secondary=BindHost2Group, back_populates='groups')
    users = relationship("User", secondary=User2Group)

    def __repr__(self):
        return "<Group(id='%s',name='%s')>" % (self.id, self.name)


class BindHost(BaseModule):
    """绑定主机表结构"""
    __tablename__ = 'bind_host'

    id = Column(Integer, primary_key=True, autoincrement=True)
    host_id = Column(Integer, ForeignKey('host.id'))
    host_user_id = Column(Integer, ForeignKey('host_user.id'))

    host = relationship("Host")
    host_user = relationship("HostUser")
    groups = relationship("Group", secondary=BindHost2Group, back_populates='bind_hosts')
    # user_profiles = relationship("UserProfile",secondary=BindHost2UserProfile)

    __table_args__ = (UniqueConstraint('host_id', 'host_user_id', name='_bindhost_and_user_uc'),)

    def __repr__(self):
        return "<BindHost(id='%s',name='%s',user='%s')>" % (self.id,
                                                            self.host.hostname,
                                                            self.host_user.username
                                                            )


class AuditLog(BaseModule):
    """日志表结构"""

    __tablename__ = 'auditlog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(String(128))
    username = Column(String(64))
    host = Column(String(64))
    cmd = Column(String(128))

    def __repr__(self):
        temp = '<AuditLog(id=%s,time=%s,username=%s,host=%s,cmd=%s)>' % (
            self.id, self.time, self.username, self.host, self.cmd)
        return temp
