#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/11
"""客户端模块"""
import os
import sys
import json
import socket
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

# 下载路径
download_path = os.path.join(path, "download")

# 主机地址、端口
HOST = "localhost"
PORT = 9000

# 帮助信息
HELP = """auth 注册 eg:auth Breakering 123
login 登陆 eg:login Breakering 123
ls 检查用户目录 eg:ls
put 发送文件 eg:put filepath
get 接收文件 eg:get filename
quit 退出 eg:quit"""

# 状态码
STATUS_CODE = {
    650: "\033[31;1m用户名已经存在\033[0m",
    651: "\033[32;1m注册成功\033[0m",
    652: "\033[31;1m禁止注册\033[0m",
    653: "\033[31;1m用户名或密码错误\033[0m",
    654: "\033[32;1m登陆成功\033[0m",
    655: "\033[31;1m禁止登陆\033[0m",
    656: "\033[31;1m您没登陆\033[0m",
    657: "\033[32;1m验证成功\033[0m",
    658: "\033[31;1m服务器端没有此文件\033[0m",
    659: "\033[31;1m命令错误\033[0m",
    660: "\033[31;1m文件或目录已存在\033[0m"
}


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
            choice = input(">>:").strip()
            if len(choice) == 0:
                continue
            cmd_list = choice.split()
            if hasattr(self, "_%s" % cmd_list[0]):
                f = getattr(self, "_%s" % cmd_list[0])
                f(cmd_list)
            else:
                print("\033[31;1m命令错误!\033[0m")
                continue

    def send_msg(self, data_header):
        """发送信息函数"""
        data_header = json.dumps(data_header).encode("utf-8")
        self.client.send(data_header)
        ret = json.loads(self.client.recv(1024).decode())
        return ret

    def _auth(self, *args):
        """注册功能"""
        cmd_list = args[0]
        if len(cmd_list) == 3:  # 确定输入格式规范
            username = cmd_list[1]
            password = cmd_list[2]
            data_header = {
                "action": "auth",
                "username": username,
                "password": password
            }
            ret = self.send_msg(data_header)
            status_code = ret["status_code"]
            if status_code in STATUS_CODE:
                print(STATUS_CODE[status_code])
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")
            return

    def _login(self, *args):
        """登陆功能"""
        cmd_list = args[0]
        if len(cmd_list) == 3:  # 确定输入格式规范
            username = cmd_list[1]
            password = cmd_list[2]
            data_header = {
                "action": "login",
                "username": username,
                "password": password
            }
            ret = self.send_msg(data_header)
            status_code = ret["status_code"]
            if status_code in STATUS_CODE:
                print(STATUS_CODE[status_code])
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")
            return

    def _ls(self, *args):
        """检查用户目录下文件功能"""
        cmd_list = args[0]
        if len(cmd_list) == 1:  # 确定输入格式规范
            data_header = {
                "action": "ls"
            }
            ret = self.send_msg(data_header)
            status_code = ret["status_code"]
            if status_code in STATUS_CODE:
                if status_code == 657:
                    print("".center(30, "="))
                    data = ret["data"]
                    if len(data) == 0:
                        print("\033[31;1m对不起，目前此目录下无文件！\033[0m")
                    for i in data:
                        print(i)
                    print("".center(30, "="))
                else:
                    print(STATUS_CODE[status_code])
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")
            return

    def _put(self, *args):
        """发送文件功能"""
        cmd_list = args[0]
        if len(cmd_list) == 2:  # 确定输入格式规范
            file_path = cmd_list[1]
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                filename = os.path.basename(file_path)
                data_header = {
                    "action": "put",
                    "filename": filename,
                    "file_size": file_size
                }
                ret = self.send_msg(data_header)
                status_code = ret["status_code"]
                if status_code in STATUS_CODE:
                    if status_code == 657:
                        f = open(file_path, "rb")
                        send_size = 0
                        for line in f:
                            self.client.sendall(line)
                            send_size += len(line)
                            self.view_bar(send_size, file_size)
                        print("\033[32;1m发送完毕\033[0m")
                    else:
                        print(STATUS_CODE[status_code])
                else:
                    print("未知错误")
            else:
                print("\033[31;1m文件不存在！\033[0m")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")
            return

    def _get(self, *args):
        """接收文件功能"""
        cmd_list = args[0]
        if len(cmd_list) == 2:  # 确定输入格式规范
            filename = cmd_list[1]
            data_header = {
                "action": "get",
                "filename": filename
            }
            ret = self.send_msg(data_header)
            status_code = ret["status_code"]
            if status_code in STATUS_CODE:
                if status_code == 657:
                    self.client.send(b"1")
                    file_size = ret["file_size"]
                    file_path = os.path.join(download_path, filename)
                    f = open(file_path, "wb")
                    recvd_size = 0
                    while recvd_size < file_size:
                        line = self.client.recv(1024)
                        f.write(line)
                        recvd_size += len(line)
                        self.view_bar(recvd_size, file_size)
                    print("接收完毕")
                else:
                    print(STATUS_CODE[status_code])
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")
            return

    def _quit(self, *args):
        """退出功能"""
        self.client.close()
        exit()

    def _help(self, *args):
        """帮助功能"""
        print("功能介绍".center(30, "-"))
        print(HELP)
        print("".center(32, "-"))


if __name__ == '__main__':
    client = FtpClient()
    client.start()
