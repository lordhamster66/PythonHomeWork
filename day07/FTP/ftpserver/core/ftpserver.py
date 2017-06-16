#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/20
"""服务端类，提供服务器功能"""
import os
import socket
import json
from conf import settings
from core import mylogger
from core import user

# 创建行为日志对象
log = mylogger.Mylogger(settings.ACTION_LOGPATH, "acion", settings.LOG_LEVEL)
action_logger = log.get_logger()


class FtpServer(object):
    """服务器类"""
    def __init__(self):
        self.server = socket.socket()
        self.server.bind((settings.HOST, settings.PORT))
        self.server.listen(5)
        self.conn = None
        self.client_addr = None
        self.user_id = None

    def start(self):
        print("\033[32;1m服务端已启动！\033[0m")
        while True:
            self.conn, self.client_addr = self.server.accept()  # 阻塞
            print("已连接客户端", self.client_addr)
            while True:
                try:
                    data_header = self.conn.recv(1024)  # 接收客户端数据
                except ConnectionResetError as e:
                    print(e)
                    break
                try:
                    data_header = json.loads(data_header.decode())
                except json.decoder.JSONDecodeError as e:
                    print(e)
                    break
                if data_header.get("action") is not None:
                    if hasattr(self, "_%s" % data_header["action"]):
                        f = getattr(self, "_%s" % data_header["action"])
                        f(data_header)
                    else:
                        print("\033[31;1m命令错误！\033[0m")
                        self.conn.send("Invalid")

    def _auth(self, data_header):
        """注册函数"""
        # print(data_header)
        username = data_header['username']
        password = data_header['password']
        obj = user.User()
        status = obj.enroll(username, password)
        self.conn.send(status.encode("utf-8"))
        if status == "done":
            ret = obj.create_directory()
            if ret:
                action_logger.info("%s用户目录创建成功！" % obj.username)

    def _login(self, data_header):
        """登陆函数"""
        # print(data_header)
        username = data_header['username']
        password = data_header['password']
        ret = user.User.login(username, password)
        status = ret["status"]
        self.conn.send(status.encode("utf-8"))
        if ret["obj"]:
            self.user_id = ret["obj"].id  # 获取用户对象的id对象

    def _logout(self, data_header):
        """注销功能"""
        # print(data_header)
        if self.user_id:
            self.user_id = None
            self.conn.send("done".encode("utf-8"))
        else:
            self.conn.send("unneeded".encode("utf-8"))

    def _check(self, data_header):
        """查看用户目录文件函数"""
        if self.user_id:
            self.conn.send("pass".encode("utf-8"))
            obj = self.user_id.get_obj_by_id()
            username = obj.username
            user_directory_dir = settings.USER_DIRECTORY_DIR
            user_directory_path = os.path.join(user_directory_dir, username)  # 获取用户目录路径
            file_list = os.listdir(user_directory_path)  # 获取用户目录路径下所有文件
            self.conn.send(json.dumps(file_list).encode("utf-8"))
        else:
            self.conn.send("unlogin".encode("utf-8"))
            return

    def _put(self, data_header):
        """接收客户端文件函数"""
        if self.user_id:
            self.conn.send("pass".encode("utf-8"))
            file_name = data_header["file_name"]  # 获取文件名
            size = data_header["size"]  # 获取文件大小
            obj = self.user_id.get_obj_by_id()  # 获取用户对象
            user_directory_dir = settings.USER_DIRECTORY_DIR  # 用户总目录
            user_directory_path = os.path.join(user_directory_dir, obj.username)  # 当前用户目录
            file_path = os.path.join(user_directory_path, file_name)  # 生成文件绝对路径
            file_obj = open(file_path, "wb")  # 打开一个文件
            len_recv_data = 0
            while len_recv_data < size:
                recv_data = self.conn.recv(4096)
                file_obj.write(recv_data)
                len_recv_data += len(recv_data)
            else:
                print("文件接收完毕！")
                action_logger.info("用户[%s]下载了文件[%s]" % (obj.username, file_name))
                file_obj.close()
        else:
            self.conn.send("unlogin".encode("utf-8"))
            return

    def _get(self, data_header):
        """向客户端发送文件函数"""
        if self.user_id:
            file_name = data_header["file_name"]  # 获取文件名
            obj = self.user_id.get_obj_by_id()  # 获取用户对象
            user_directory_dir = settings.USER_DIRECTORY_DIR  # 用户总目录
            user_directory_path = os.path.join(user_directory_dir, obj.username)  # 当前用户目录
            file_path = os.path.join(user_directory_path, file_name)  # 获取文件绝对路径
            if os.path.isfile(file_path):
                self.conn.send("pass".encode("utf-8"))
                file_size = os.path.getsize(file_path)  # 获取文件大小
                file_send_header = {"file_size": file_size}
                self.conn.send(json.dumps(file_send_header).encode("utf-8"))
                if self.conn.recv(1024).decode() == "start":
                    file_obj = open(file_path, "rb")  # 打开一个文件
                    for line in file_obj:
                        self.conn.send(line)
                    print("文件发送完毕！")
                    action_logger.info("用户[%s]下载了文件[%s]" % (obj.username, file_name))
                    file_obj.close()
            else:
                self.conn.send("not_exist".encode("utf-8"))
        else:
            self.conn.send("unlogin".encode("utf-8"))



