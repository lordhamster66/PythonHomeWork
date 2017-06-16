#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/20
import os
import sys
import json
import socket
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
HOST = "localhost"
PORT = 9000
HELP = """auth 注册 eg:auth Breakering 123
login 登陆 eg:login Breakering 123
check 检查用户目录 eg:check
put 发送文件 eg:put D:\mylog.log
get 接收文件 eg:get filename
logout 注销 eg:logout
quit 退出 eg:quit"""


class FtpClient(object):
    """客户端类"""
    def __init__(self):
        self.client = socket.socket()
        self.client.connect((HOST, PORT))

    @staticmethod
    def view_bar(num, total):
        """进度条函数"""
        rate = float(num) / float(total)
        len_mark = int(rate * 30)
        rate_num = int(rate * 100)
        r = '\r\033[32;1m%s>%d%%\033[0m' % ("=" * len_mark, rate_num)
        sys.stdout.write(r)
        sys.stdout.flush()

    def start(self):
        """客户端启动函数"""
        print("\033[32;1mTip:可以使用help查看已支持功能！\033[0m")
        while True:
            choice = input(">>>").strip()
            if len(choice) == 0:
                continue
            cmd_list = choice.split()
            if hasattr(self, "_%s" % cmd_list[0]):
                f = getattr(self, "_%s" % cmd_list[0])
                f(cmd_list)
            else:
                print("\033[31;1m命令错误!\033[0m")
                continue

    def _auth(self, cmd_list):
        """注册功能"""
        status = {
            "exist": "\033[31;1m用户名已经存在\033[0m",
            "done": "\033[32;1m注册成功\033[0m",
            "ban": "\033[31;1m禁止注册\033[0m"
        }
        if len(cmd_list) == 3:  # 确定输入格式规范
            username = cmd_list[1]
            password = cmd_list[2]
            data_header = {
                "action": "auth",
                "username": username,
                "password": password
            }
            data_header = json.dumps(data_header).encode("utf-8")
            self.client.send(data_header)
            ret = self.client.recv(1024).decode()
            if ret in status:
                print(status[ret])
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")
            return

    def _login(self, cmd_list):
        """登陆功能"""
        status = {
            "error": "\033[31;1m用户名或密码错误\033[0m",
            "done": "\033[32;1m登陆成功\033[0m",
            "ban": "\033[31;1m禁止登陆\033[0m"
        }
        if len(cmd_list) == 3:  # 确定输入格式规范
            username = cmd_list[1]
            password = cmd_list[2]
            data_header = {
                "action": "login",
                "username": username,
                "password": password
            }
            data_header = json.dumps(data_header).encode("utf-8")
            self.client.send(data_header)
            ret = self.client.recv(1024).decode()
            if ret in status:
                print(status[ret])
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")

    def _logout(self, cmd_list):
        """注销功能"""
        status = {
            "done": "\033[32;1m注销成功\033[0m",
            "unneeded": "\033[31;1m您没登陆\033[0m",
        }
        if len(cmd_list) == 1:
            data_header = {"action": "logout"}
            data_header = json.dumps(data_header).encode("utf-8")
            self.client.send(data_header)
            ret = self.client.recv(1024).decode()
            if ret in status:
                print(status[ret])
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")

    def _check(self, cmd_list):
        """检查用户目录下文件功能"""
        status = {
            "pass": "\033[32;1m您的目录文件如下:\033[0m",
            "unlogin": "\033[31;1m您没登陆\033[0m",
        }
        if len(cmd_list) == 1:
            data_header = {"action": "check"}
            data_header = json.dumps(data_header).encode("utf-8")
            self.client.send(data_header)
            ret = self.client.recv(1024).decode()
            if ret in status:
                print(status[ret])
                if ret == "pass":
                    print("".center(30, "="))
                    file_list = json.loads(self.client.recv(1024).decode())
                    if len(file_list) == 0:
                        print("\033[31;1m对不起，目前服务器下无文件！\033[0m")
                        return
                    for i in file_list:
                        print(i)
                    print("".center(30, "="))
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")

    def _put(self, cmd_list):
        """发送文件功能"""
        status = {
            "pass": "\033[32;1m开始发送文件\033[0m",
            "unlogin": "\033[31;1m您没登陆\033[0m",
        }
        if len(cmd_list) == 2:
            action = cmd_list[0]
            file_name = cmd_list[1]
            if os.path.isfile(file_name):
                file_obj = open(file_name, "rb")  # 打开文件
                base_name = os.path.basename(file_name)  # 获取文件名
                file_size = os.path.getsize(file_name)  # 获取文件大小
                data_header = {
                    "action": action,
                    "file_name": base_name,
                    "size": file_size
                }
                data_header = json.dumps(data_header).encode("utf-8")
                self.client.send(data_header)
                ret = self.client.recv(1024).decode()
                if ret in status:
                    print(status[ret])
                    if ret == "pass":
                        curent_len = 0
                        for line in file_obj:
                            self.client.send(line)
                            curent_len += len(line)
                            self.view_bar(curent_len, file_size)
                        file_obj.close()
                        print("\033[31;1m文件传输完毕！\033[0m")
                else:
                    print("未知错误")
            else:
                print("\033[31;1m文件不存在！\033[0m")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")

    def _get(self, cmd_list):
        """接收文件功能"""
        status = {
            "pass": "\033[32;1m开始接收文件\033[0m",
            "unlogin": "\033[31;1m您没登陆\033[0m",
            "not_exist": "\033[31;1m服务器端没有此文件\033[0m",
        }
        if len(cmd_list) == 2:
            action = cmd_list[0]
            file_name = cmd_list[1]
            data_header = {
                "action": action,
                "file_name": file_name
            }
            data_header = json.dumps(data_header).encode("utf-8")
            self.client.send(data_header)
            ret = self.client.recv(1024).decode()
            if ret in status:
                print(status[ret])
                if ret == "pass":
                    file_path = os.path.join(path, "download", file_name)
                    file_obj = open(file_path, "wb")
                    file_get_header = json.loads(self.client.recv(1024).decode())
                    self.client.send("start".encode("utf-8"))
                    file_size = file_get_header["file_size"]
                    current_size = 0
                    while current_size < file_size:
                        line = self.client.recv(4096)
                        file_obj.write(line)
                        current_size += len(line)
                        self.view_bar(current_size, file_size)
                    else:
                        print("\033[31;1m文件接收完毕\033[0m")
                        file_obj.close()
                        return
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")

    def _quit(self, cmd_list):
        """退出功能"""
        self.client.close()
        exit()

    def _help(self, cmd_list):
        """帮助功能"""
        print("功能介绍".center(30, "-"))
        print(HELP)
        print("".center(32, "-"))


if __name__ == '__main__':
    client = FtpClient()
    client.start()
