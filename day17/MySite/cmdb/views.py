from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
import json
import os
import hashlib
import time
from MySite import settings
from cmdb import models
from cmdb.utils import yaml_parser
from sqlalchemy.orm import sessionmaker
# Create your views here.


def home(request):
    """首页"""
    return render(request, "home.html")


def init(request):
    """初始化函数"""
    models.base.metadata.create_all()  # 初始化数据的表格
    host_file = os.path.join(settings.BASE_DIR, "static", "table", "host.yaml")  # 获取已经设置好的主机信息文件
    host_data = yaml_parser(host_file)  # 使用yaml解析
    session_class = sessionmaker(bind=models.engine)  # 创建一个session类
    session = session_class()  # 创建一个session实例
    for k, v in host_data.items():  # 创建所有的主机信息
        host_obj = models.Host(hostname=v.get("hostname"), ip=v.get("ip"), port=v.get("port"),
                               line_status=v.get("line_status"), server_style=v.get("server_style"),
                               cpu=v.get("cpu"), memory=v.get("memory"), disk=v.get("disk"))
        session.add(host_obj)
    session.commit()
    group_file = os.path.join(settings.BASE_DIR, "static", "table", "group.yaml")  # 获取分组信息文件
    group_data = yaml_parser(group_file)  # yaml解析
    for k, v in group_data.items():  # 创建所有的分组信息
        group_obj = models.Group(groupname=v[0])
        for h in v[1].get("host"):
            h_obj = session.query(models.Host).filter(models.Host.hostname == h).first()
            group_obj.hosts.append(h_obj)
        session.add(group_obj)
    session.commit()
    user_file = os.path.join(settings.BASE_DIR, "static", "table", "user.yaml")  # 获取用户信息文件
    user_data = yaml_parser(user_file)  # yaml解析
    for k, v in user_data.items():
        m_obj = hashlib.md5()  # 创建一个md5对象
        username = v.get("username")
        password = str(v.get("password"))
        m_obj.update(password.encode("utf-8"))
        password = m_obj.hexdigest()  # 加密的用户密码
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 获取实时的时间
        group = v.get("group")
        g_obj = session.query(models.Group).filter(models.Group.groupname == group).first()
        group_id = g_obj.id
        user_obj = models.User(username=username, password=password, create_time=create_time, group_id=group_id)
        session.add(user_obj)
    session.commit()
    session.close()
    return HttpResponse("done!")


def drop(request):
    """drop数据库函数"""
    models.base.metadata.drop_all()
    return HttpResponse("done!")


def login(request):
    return render(request, "login.html")


def login_check(request):
    """登录检查函数"""
    session_class = sessionmaker(bind=models.engine)  # 创建一个session类
    session = session_class()  # 创建一个session实例
    if request.method == "POST":
        loginObj = request.POST.get("loginObj")
        loginObj = json.loads(loginObj)
        username = loginObj.get("accountNo")  # 获取用户名
        m_obj = hashlib.md5()  # 创建一个md5对象
        password = str(loginObj.get("pwd"))  # 获取密码
        m_obj.update(password.encode("utf-8"))
        password = m_obj.hexdigest()  # 加密的用户密码
        user_obj = session.query(models.User).filter(models.User.username == username).first()
        if user_obj:  # 能获取结果，说明用户名在数据库里面
            if password == user_obj.password:  # 密码匹配则登录成功
                ret = json.dumps({"user": "ok!"})
            else:  # 否则返回密码错误
                ret = json.dumps({"pwdMsg": "用户名密码错误"})
        else:
            ret = json.dumps({"accountMsg": "用户名不存在"})
        session.close()
        return HttpResponse(ret)


def register(request):
    return render(request, "register.html")


def register_check(request):
    """注册检查函数"""
    session_class = sessionmaker(bind=models.engine)  # 创建一个session类
    session = session_class()  # 创建一个session实例
    if request.method == "POST":
        registerObj = request.POST.get("registerObj")
        registerObj = json.loads(registerObj)
        username = registerObj.get("accountNo")  # 获取用户名
        m_obj = hashlib.md5()  # 创建一个md5对象
        password = str(registerObj.get("pwd"))  # 获取密码
        password_again = str(registerObj.get("pwdAgain"))  # 获取第二次输入的密码
        if password != password_again:
            ret = json.dumps({"pwdMsg": "两次密码不一样!"})
        else:
            m_obj.update(password.encode("utf-8"))
            password = m_obj.hexdigest()  # 加密的用户密码
            user_obj = session.query(models.User).filter(models.User.username == username).first()
            if user_obj:
                ret = json.dumps({"accountMsg": "用户名已存在!"})
            else:
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 获取实时的时间
                g_obj = session.query(models.Group).filter(models.Group.groupname == "运维部").first()
                new_user = models.User(username=username, password=password, create_time=create_time, group_id=g_obj.id)
                session.add(new_user)
                session.commit()
                session.close()
                ret = json.dumps({"user": "ok!"})
        session.close()
        return HttpResponse(ret)


def index(request):
    """主机管理功能"""
    session_class = sessionmaker(bind=models.engine)  # 创建一个session类
    session = session_class()  # 创建一个session实例
    if request.method == "POST":
        username = request.POST.get("accountNo")
        m_obj = hashlib.md5()  # 创建一个md5对象
        password = request.POST.get("pwd")
        m_obj.update(password.encode("utf-8"))
        password = m_obj.hexdigest()  # 加密的用户密码
        user_obj = session.query(models.User).filter(models.User.username == username and
                                                     models.User.password == password).first()
        hosts = user_obj.user_group.hosts
        session.close()
        return render(request, "index.html", {"username": username, "hosts": hosts})


def select(request):
    """提供根据host_id查询信息的功能"""
    session_class = sessionmaker(bind=models.engine)  # 创建一个session类
    session = session_class()  # 创建一个session实例
    if request.method == "POST":
        host_id = request.POST.get("host_id")
        host_obj = session.query(models.Host).filter(models.Host.id == host_id).first()
        host_obj = {"hostname": host_obj.hostname, "ip": host_obj.ip, "port": host_obj.port,
                    "line_status": host_obj.line_status,"server_style": host_obj.server_style,
                    "cpu": host_obj.cpu, "memory": host_obj.memory, "disk": host_obj.disk}
        host_obj = json.dumps(host_obj)
        session.close()
        return HttpResponse(host_obj)


def update(request):
    """提供更新功能"""
    session_class = sessionmaker(bind=models.engine)  # 创建一个session类
    session = session_class()  # 创建一个session实例
    if request.method == "POST":
        host_info = request.POST.get("host_info")
        host_info = json.loads(host_info)
        session.query(models.Host).filter(models.Host.id == host_info.get("host_id")).update(
            {"hostname": host_info.get("hostname"), "ip": host_info.get("ip"),
             "port": host_info.get("port"), "line_status": host_info.get("line_status"),
             "server_style": host_info.get("server_style"), "cpu": host_info.get("cpu"),
             "memory": host_info.get("memory"), "disk": host_info.get("disk")}
        )  # 更新主机信息
        session.commit()
        session.close()
        return HttpResponse("ok")


def insert(request):
    """提供添加功能"""
    session_class = sessionmaker(bind=models.engine)  # 创建一个session类
    session = session_class()  # 创建一个session实例
    if request.method == "POST":
        host_info = request.POST.get("host_info")
        host_info = json.loads(host_info)
        username = request.POST.get("username")
        user_obj = session.query(models.User).filter(models.User.username == username).first()
        h1 = session.query(models.Host).filter(models.Host.hostname == host_info.get("hostname")).first()
        if h1:  # 主机名存在
            ret = json.dumps({"HostName": "repeat"})
        else:
            h2 = session.query(models.Host).filter(models.Host.ip == host_info.get("ip")).first()
            if h2:  # 主机地址存在
                ret = json.dumps({"IP": "repeat"})
            else:
                host_obj = models.Host(hostname=host_info.get("hostname"), ip=host_info.get("ip"),
                                       port=host_info.get("port"), line_status=host_info.get("line_status"),
                                       server_style=host_info.get("server_style"), cpu=host_info.get("cpu"),
                                       memory=host_info.get("memory"), disk=host_info.get("disk"))
                host_obj.groups.append(user_obj.user_group)  # 将其分组至当前用户所在的组别
                session.add(host_obj)  # 添加主机信息
                session.commit()
                session.close()
                ret = json.dumps({"Confirm": "ok"})
        session.close()
        return HttpResponse(ret)


def delete(request):
    """提供删除功能"""
    session_class = sessionmaker(bind=models.engine)  # 创建一个session类
    session = session_class()  # 创建一个session实例
    if request.method == "POST":
        host_id = request.POST.get("host_id")
        host_obj = session.query(models.Host).filter(models.Host.id == host_id).first()
        host_obj.groups.clear()  # 清空分组才能删除主机
        session.commit()
        session.query(models.Host).filter(models.Host.id == host_id).delete()
        session.commit()
        session.close()
        return HttpResponse("ok")
