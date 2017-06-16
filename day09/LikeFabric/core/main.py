#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/4
"""
主要服务模块,逻辑处理全在这
"""
import os
import json
import time
import datetime
import threading
from conf import settings
from conf import exhibition
from core.user import User
from core.mylogger import Mylogger
from lib import public
from core.myssh import Myssh

# 生成日志对象
action_logger = Mylogger(settings.ACTION_LOGPATH, "action", settings.LOG_LEVEL).get_logger()

# 生成日期，星期
week_list = ("一", "二", "三", "四", "五", "六", "日")       # 星期对照表
today = time.strftime("%Y-%m-%d", time.localtime())         # 获取今天的日期
week = week_list[int(datetime.datetime.now().weekday())]    # 获取星期

# 功能帮助清单
myhelp = """chose eg:chose 1 说明:选择一个主机;chose 1,2 同时选择两个主机
add eg:add 192.168.48.30 22 用户名 密码
del eg:del 1 说明:删除一号主机
quit 说明:退出程序"""

# 命令帮助清单
command_help = """ssh eg:ssh ls 说明:执行命令
put eg:put local_file server_path 说明:上传文件
get eg:get server_file local_path 说明:下载文件
q 说明:返回上级菜单"""


class Haproxy(object):
    """主机管理类"""

    @staticmethod
    def __get_host_list():
        """获取主机列表功能"""
        host_dir = settings.HOST_DIR
        host_list = []  # 所有主机信息列表
        host_path_list = []  # 存储主机路径列表
        for host_file_name in os.listdir(host_dir):
            host_path = os.path.join(host_dir, host_file_name)
            host = json.load(open(host_path, "r", encoding="utf-8"))
            host_list.append(host)
            host_path_list.append(host_path)
        return host_list, host_path_list

    def __info(self):
        """显示所有主机信息"""
        host_list, host_path_list = self.__get_host_list()
        print(exhibition.host_list_show)
        print("".center(74, "="))
        print("%-5s %-8s %s %s" % ("序号", "主机地址", "端口", "用户名"))
        for index, i in enumerate(host_list):
            print("%-3s %-15s %-5s %s" % (index+1, i["host"], i["port"], i["username"]))
        print("".center(74, "="))
        return host_list, host_path_list

    def start(self):
        """开始整个程序"""
        print(exhibition.action_show.format(today=today, week=week))
        data = User.login(action_logger)
        if data["status"] == "done":
            while True:
                os.system("cls")
                host_list, host_path_list = self.__info()
                print("帮助".center(72, "="))
                print(myhelp)
                print("".center(74, "="))
                cmd = input(">>>:").strip()
                cmd_list = cmd.split()
                if hasattr(self, "_%s" % cmd_list[0]):
                    func = getattr(self, "_%s" % cmd_list[0])
                    func(cmd, host_list, host_path_list)
                else:
                    print("\033[31;1m命令错误!\033[0m")

    def _chose(self, *args):
        """选取主机功能"""
        cmd = args[0]
        host_list = args[1]
        cmd_list = cmd.split()
        if len(cmd_list) == 2:
            chose_host_index = []  # 选取的主机序号存放列表
            myssh_obj_list = []  # 所选主机生成的myssh对象
            chose_host_before_index = cmd_list[1].split(",")
            for i in chose_host_before_index:
                if i.isdigit():  # 序号必须为数字
                    if int(i) <= 0 or int(i) > len(host_list):
                        print("\033[31;1m序号错误!\033[0m")
                        return
                    chose_host_index.append(int(i)-1)
                else:
                    print("\033[31;1m必须为数字!\033[0m")
                    return
            for index in chose_host_index:
                host = host_list[index]["host"]
                port = host_list[index]["port"]
                username = host_list[index]["username"]
                password = host_list[index]["password"]
                myssh_obj = Myssh(host, port, username, password, action_logger)
                myssh_obj_list.append(myssh_obj)
            while True:
                print("帮助".center(72, "="))
                print(command_help)
                print("".center(74, "="))
                command = input(">>>").strip()
                command_list = command.split()
                if command == "q":
                    return
                if hasattr(self, "_%s" % command_list[0]):
                    func = getattr(self, "_%s" % command_list[0])
                    print("\033[32;1m多线程启动，请耐心等待结果！\033[0m")
                    func(command_list, myssh_obj_list)
                else:
                    print("\033[31;1m命令错误!\033[0m")
        else:
            print("\033[31;1m命令错误!\033[0m")

    def _add(self, *args):
        """添加主机功能"""
        cmd = args[0]
        host_list = args[1]
        cmd_list = cmd.split()
        if len(cmd_list) == 5:
            host = cmd_list[1]
            port = int(cmd_list[2])
            username = cmd_list[3]
            password = cmd_list[4]
            for i in host_list:
                if host == i["host"] and port == i["port"] and username == i["username"]:
                    print("\033[31;1m主机已经存在不必重复添加！\033[0m")
                    time.sleep(0.5)
                    return
            h = {
                "host": host,
                "port": port,
                "username": username,
                "password": password
            }
            h_id = public.creat_id()
            host_dir = settings.HOST_DIR
            host_path = os.path.join(host_dir, "%s.json" % h_id)
            json.dump(h, open(host_path, "w", encoding="utf-8"))
            print("\033[32;1m主机%s,端口%s,用户名%s添加成功！\033[0m" % (host, port, username))
            action_logger.info("主机%s,端口%s,用户名%s添加成功！" % (host, port, username))
        else:
            print("\033[31;1m命令错误!\033[0m")

    def _del(self, *args):
        """删除主机功能"""
        cmd = args[0]
        host_list = args[1]
        host_path_list = args[2]
        cmd_list = cmd.split()
        if len(cmd_list) == 2:
            index = int(cmd_list[1])-1
            host = host_list[index]["host"]
            port = host_list[index]["port"]
            username = host_list[index]["username"]
            os.remove(host_path_list[index])
            print("\033[32;1m主机%s,端口%s,用户名%s删除完毕！\033[0m" % (host, port, username))
            action_logger.info("主机%s,端口%s,用户名%s删除完毕！" % (host, port, username))
        else:
            print("\033[31;1m命令错误!\033[0m")

    def _ssh(self, *args):
        """执行命令功能"""
        command_list = args[0]
        del command_list[0]
        command = " ".join(command_list)
        myssh_obj_list = args[1]
        task_obj_list = []
        for i in myssh_obj_list:
            t = threading.Thread(target=i.ssh, args=(command,))
            t.start()
            task_obj_list.append(t)
        for task in task_obj_list:
            task.join()

    def _put(self, *args):
        """上传文件功能"""
        command_list = args[0]
        if len(command_list) == 3:
            myssh_obj_list = args[1]
            task_obj_list = []
            for i in myssh_obj_list:
                t = threading.Thread(target=i.put, args=(command_list[1], command_list[2]))
                t.start()
                task_obj_list.append(t)
            for task in task_obj_list:
                task.join()
        else:
            print("\033[31;1m命令错误!\033[0m")

    def _get(self, *args):
        """下载文件功能"""
        command_list = args[0]
        if len(command_list) == 3:
            myssh_obj_list = args[1]
            task_obj_list = []
            for i in myssh_obj_list:
                t = threading.Thread(target=i.get, args=(command_list[1], command_list[2]))
                t.start()
                task_obj_list.append(t)
            for task in task_obj_list:
                task.join()
        else:
            print("\033[31;1m命令错误!\033[0m")

    def _quit(self, *args):
        """退出整个程序"""
        exit()
