#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/29
import os
import sys
import json
import socket
import hashlib
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
download_path = os.path.join(path, "download")

# 主机地址、端口
HOST = "localhost"
PORT = 9000

# 帮助信息
HELP = """auth 注册 eg:auth Breakering 123
login 登陆 eg:login Breakering 123
ls 检查用户目录 eg:check
cd 切换目录 eg:cd test,cd ..
mkdir 创建目录 eg:mkdir test
put 发送文件 eg:put D:\mylog.log
get 接收文件 eg:get filename
logout 注销 eg:logout
quit 退出 eg:quit"""

# 状态码
STATUS_CODE = {
    650: "\033[31;1m用户名已经存在\033[0m",
    651: "\033[32;1m注册成功\033[0m",
    652: "\033[31;1m禁止注册\033[0m",
    653: "\033[31;1m用户名或密码错误\033[0m",
    654: "\033[32;1m登陆成功\033[0m",
    655: "\033[31;1m禁止登陆\033[0m",
    656: "\033[32;1m注销成功\033[0m",
    657: "\033[31;1m您没登陆\033[0m",
    658: "\033[32;1m验证成功\033[0m",
    659: "\033[31;1m服务器端没有此文件\033[0m",
    660: "\033[31;1m权限不足\033[0m",
    661: "\033[31;1m用户名不存在\033[0m",
    662: "\033[31;1m用户没有此类信息\033[0m",
    663: "\033[32;1m用户信息修改成功\033[0m",
    664: "\033[31;1m管理员没有此类功能\033[0m",
    665: "\033[31;1m命令错误\033[0m",
    666: "\033[31;1m文件或目录已存在\033[0m",
    667: "\033[31;1m超出磁盘配额\033[0m"
}


class FtpClient(object):
    """客户端类"""
    def __init__(self):
        self.client = socket.socket()
        self.client.connect((HOST, PORT))
        self.user_dir = ""

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
            choice = input("%s>>>" % self.user_dir).strip()
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
                if status_code == 654:
                    self.user_dir = username
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")
            return

    def _manage(self, *args):
        """管理员登陆功能"""
        cmd_list = args[0]
        if len(cmd_list) == 3:  # 确定输入格式规范
            username = cmd_list[1]
            password = cmd_list[2]
            data_header = {
                "action": "manage",
                "username": username,
                "password": password
            }
            ret = self.send_msg(data_header)
            status_code = ret["status_code"]
            if status_code in STATUS_CODE:
                print(STATUS_CODE[status_code])
                if status_code == 654:
                    self.user_dir = username
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")
            return

    def _set(self, *args):
        """管理员设置用户信息功能"""
        cmd_list = args[0]
        if len(cmd_list) == 4:  # 确定输入格式规范
            username = cmd_list[1]
            info = cmd_list[2]
            value = cmd_list[3]
            data_header = {
                "action": "set",
                "username": username,
                "info": info,
                "value": value
            }
            ret = self.send_msg(data_header)
            status_code = ret["status_code"]
            if status_code in STATUS_CODE:
                if status_code == 663:
                    data = ret["data"]
                    print(STATUS_CODE[status_code])
                    print("\033[32;1m%s\033[0m" % data)
                else:
                    print(STATUS_CODE[status_code])
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")
            return

    def _logout(self, *args):
        """注销功能"""
        cmd_list = args[0]
        if len(cmd_list) == 1:  # 确定输入格式规范
            data_header = {
                "action": "logout"
            }
            ret = self.send_msg(data_header)
            status_code = ret["status_code"]
            if status_code in STATUS_CODE:
                if status_code == 656:
                    self.user_dir = ""
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
                if status_code == 658:
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

    def _cd(self, *args):
        """切换目录功能"""
        cmd_list = args[0]
        if len(cmd_list) == 2:  # 确定输入格式规范
            where = cmd_list[1]
            data_header = {
                "action": "cd",
                "where": where
            }
            ret = self.send_msg(data_header)
            status_code = ret["status_code"]
            if status_code in STATUS_CODE:
                if status_code == 658:
                    if ret.get("where"):
                        self.user_dir = ret["where"]
                else:
                    print(STATUS_CODE[status_code])
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")
            return

    def _mkdir(self, *args):
        """创建目录功能"""
        cmd_list = args[0]
        if len(cmd_list) == 2:  # 确定输入格式规范
            dir_info = cmd_list[1]
            data_header = {
                "action": "mkdir",
                "dir_info": dir_info
            }
            ret = self.send_msg(data_header)
            status_code = ret["status_code"]
            if status_code in STATUS_CODE:
                if status_code == 658:
                    pass
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
        if len(cmd_list) == 2:
            action = cmd_list[0]
            file_name = cmd_list[1]
            if os.path.isfile(file_name):
                file_obj = open(file_name, "rb")  # 打开文件
                base_name = os.path.basename(file_name)  # 获取文件名
                file_size = os.path.getsize(file_name)  # 获取文件大小
                md5_obj = hashlib.md5()
                data_header = {
                    "action": action,
                    "file_name": base_name,
                    "size": file_size
                }
                ret = self.send_msg(data_header)
                status_code = ret["status_code"]
                if status_code in STATUS_CODE:
                    print(STATUS_CODE[status_code])
                    if status_code == 658:  # 验证通过，可以发送文件
                        curent_len = 0  # 定义一个已经发送的文件大小
                        if ret.get("cur"):  # 能获取到值，说明之前发送了部分文件内容
                            cur = ret["cur"]
                            file_obj.seek(cur)  # 将文件游标置于上次中断的部分
                            file_obj.tell()
                            curent_len = cur  # 更新已经发送的文件大小
                        for line in file_obj:
                            self.client.send(line)
                            md5_obj.update(line)
                            curent_len += len(line)
                            self.view_bar(curent_len, file_size)  # 进度条
                        file_obj.close()
                        res = json.loads(self.client.recv(1024).decode())
                        print("\033[31;1m文件传输完毕！\033[0m")
                        if res["md5"] == md5_obj.hexdigest():
                            print("\033[32;1m文件一致性验证成功！\033[0m")
                        else:
                            print("\033[31;1m文件一致性验证失败！\033[0m")
                else:
                    print("未知错误")
            else:
                print("\033[31;1m文件不存在！\033[0m")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")

    def _get(self, *args):
        """接收文件功能"""
        cmd_list = args[0]
        if len(cmd_list) == 2:
            action = cmd_list[0]
            file_name = cmd_list[1]
            md5_obj = hashlib.md5()  # 生成一个md5对象
            data_header = {
                "action": action,
                "file_name": file_name
            }
            ret = self.send_msg(data_header)
            status_code = ret["status_code"]
            if status_code in STATUS_CODE:
                print(STATUS_CODE[status_code])
                if status_code == 658:  # 验证通过，可以接收文件
                    file_size = ret["size"]  # 获取文件大小
                    file_path = os.path.join(download_path, file_name)
                    curent_len = 0  # 定义一个已经接收的文件大小
                    info = {}  # 定义一个要发给服务端的空字典
                    if os.path.isfile(file_path):  # 说明之前已经接收了部分文件内容
                        cur = os.path.getsize(file_path)
                        if cur < file_size:
                            file_obj = open(file_path, "ab")
                            file_obj.seek(cur)  # 将文件游标置于上次中断的部分
                            file_obj.tell()
                            curent_len = cur  # 更新已经接收的文件大小
                            info = {"cur": cur}
                        else:
                            file_obj = open(file_path, "wb")
                    else:
                        file_obj = open(file_path, "wb")
                    self.client.send(json.dumps(info).encode())  # 向服务端发送确认信息
                    while curent_len < file_size:
                        recv_data = self.client.recv(4096)
                        file_obj.write(recv_data)
                        md5_obj.update(recv_data)
                        curent_len += len(recv_data)
                        self.view_bar(curent_len, file_size)  # 进度条
                    else:
                        file_obj.close()
                        res = json.loads(self.client.recv(1024).decode())
                        print("\033[31;1m文件传输完毕！\033[0m")
                        if res["md5"] == md5_obj.hexdigest():
                            print("\033[32;1m文件一致性验证成功！\033[0m")
                        else:
                            print("\033[31;1m文件一致性验证失败！\033[0m")
            else:
                print("未知错误")
        else:
            print("\033[31;1m输入不规范，请检查后再输入！\033[0m")

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
