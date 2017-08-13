from django.db import models

# Create your models here.
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine("mysql+pymysql://root:dmc19930417@192.168.48.20:3306/s18?charset=utf8", max_overflow=5)

base = declarative_base(bind=engine)

group_to_host = Table('group_to_host', base.metadata,
                      Column('group_id', Integer, ForeignKey('group.id')),
                      Column('host_id', Integer, ForeignKey('host.id'))
                      )


class User(base):
    """用户表"""
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), unique=True, nullable=False)  # 用户名
    password = Column(String(128), nullable=False)  # 密码
    create_time = Column(DateTime, nullable=False)  # 注册时间
    group_id = Column(Integer, ForeignKey("group.id"))  # 对应分组ID

    user_group = relationship("Group", backref="group_user")  # 查看分组详情

    def __repr__(self):
        return "username:%s, groupname:%s" % (self.username, self.user_group.groupname)


class Group(base):
    """分组表"""
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    groupname = Column(String(32), unique=True, nullable=False)  # 分组名称
    hosts = relationship("Host", secondary=group_to_host, backref="groups")  # 分组下的主机

    def __repr__(self):
        return "groupname:%s" % self.groupname


class Host(base):
    """主机表"""
    __tablename__ = "host"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(32), unique=True, nullable=False)  # 主机名
    ip = Column(String(32), unique=True, nullable=False)  # 主机地址
    port = Column(Integer, nullable=False)  # 主机端口
    line_status = Column(String(32), nullable=False)  # 在线状态
    server_style = Column(String(32), nullable=False)  # 服务器类型
    cpu = Column(String(32), nullable=False)  # 主机CPU详情
    memory = Column(String(32), nullable=False)  # 主机内存信息
    disk = Column(String(32), nullable=False)  # 主机硬盘信息

    def __repr__(self):
        return "hostname:%s, ip:%s, port:%s" % (self.hostname, self.ip, self.port)
