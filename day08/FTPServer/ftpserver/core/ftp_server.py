#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/5/29
"""
服务器主要功能模块
"""
import socketserver
import json
import os
import re
import hashlib
from conf import settings
from core import mylogger
from core.user import User
from core.manager import Manager

# 生成日志对象
action_logger = mylogger.Mylogger(settings.ACTION_LOGPATH, "action", settings.LOG_LEVEL).get_logger()  # 行为日志
manage_logger = mylogger.Mylogger(settings.MANAGE_LOGPATH, "manage", settings.LOG_LEVEL).get_logger()  # 管理日志

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


class MyTCPHandler(socketserver.BaseRequestHandler):
    """自定义socketserver处理类"""

    def handle(self):
        self.user = {
            "type": None,
            "user_id": None,
            "user_path": None
        }
        print("{} connect:".format(self.client_address[0]))
        while True:
            try:
                data_header = self.request.recv(1024).strip()
            except ConnectionResetError as e:
                print("\033[31;1m%s\033[0m" % e)
                break
            except ConnectionAbortedError as e:
                print("\033[31;1m%s\033[0m" % e)
                break
            try:
                data_header = json.loads(data_header.decode())
            except json.decoder.JSONDecodeError as e:
                print("\033[31;1m%s\033[0m" % e)
                break
            if data_header.get("action") is not None:
                if hasattr(self, "_%s" % data_header["action"]):
                    f = getattr(self, "_%s" % data_header["action"])
                    f(data_header)
                else:
                    print("\033[31;1m命令错误！\033[0m")
                    self.request.send("Invalid")

    @staticmethod
    def cd_parser(where):
        """解决cd ..的情况"""
        where_list = [x for x in re.split("\\\\|/", where) if x]
        flag = True
        for i in where_list:
            if i.count(".") == 2 and len(i) == 2:  # 只有两个点才符合规范
                continue
            else:
                flag = False
                break
        length = len(where_list)
        return {"status": flag, "length": length}

    @staticmethod
    def path_parser(change_path, username):
        """将用户家目录及之后的目录名放入列表返回"""
        user_path_list = change_path.split(os.sep)  # 将路径分裂
        where_list = []  # 存放想要的目录名称
        flag = False
        for i in user_path_list:
            if flag:
                where_list.append(i)
            if i == username:
                where_list.append(i)
                flag = True
            else:
                continue
        return where_list

    def send_msg(self, status_code, data=None):
        """向客户端返回数据"""
        msg = {'status_code': status_code, 'status_msg': STATUS_CODE[status_code]}
        if data:
            msg.update(data)
        self.request.send(json.dumps(msg).encode())

    def _auth(self, *args):
        """注册函数"""
        data_header = args[0]
        username = data_header["username"]
        password = data_header["password"]
        obj = User()
        status = obj.enroll(username, password)
        if status == 651:
            obj.create_directory()  # 创建用户家目录
        self.send_msg(status)

    def _login(self, *args):
        """登陆函数"""
        data_header = args[0]
        username = data_header["username"]
        password = data_header["password"]
        ret = User.login(username, password)
        if ret["status"] == 654:
            self.user["type"] = "用户"
            self.user["user_id"] = ret["obj"].id
            self.user["user_path"] = ret["obj"].home_path
        self.send_msg(ret["status"])

    def _manage(self, *args):
        """管理员登陆功能"""
        data_header = args[0]
        username = data_header["username"]
        password = data_header["password"]
        ret = Manager.login(username, password)
        if ret["status"] == 654:
            self.user["type"] = "管理员"
            self.user["user_id"] = ret["obj"].id
        self.send_msg(ret["status"])

    def _set(self, *args):
        """管理员设置用户信息功能"""
        if self.user["user_id"] is not None:
            if self.user["type"] == "管理员":
                manager_obj = self.user["user_id"].get_obj_by_id()
                data_header = args[0]
                username = data_header["username"]
                info = data_header["info"]
                value = data_header["value"]
                ret = manager_obj.get_user_obj(username)
                if ret["status"] == 654:
                    user_obj = ret["obj"]
                    if hasattr(user_obj, info):
                        f = getattr(user_obj, info)
                        setattr(user_obj, info, value)
                        user_obj.save()
                        manage_logger.info("管理员%s将用户%s的%s由%s改为%s" % (manager_obj.username,
                                                                     username, info, f, value))
                        data = "用户%s的%s由%s改为%s" % (username, info, f, value)
                        self.send_msg(663, {"data": data})
                    else:
                        self.send_msg(662)
                else:
                    self.send_msg(ret["status"])
            else:
                self.send_msg(660)
        else:
            self.send_msg(657)

    def _logout(self, *args):
        """注销功能"""
        if self.user["type"]:
            self.user["type"] = None
            self.user["user_id"] = None
            self.user["user_path"] = None
            self.send_msg(656)
        else:
            self.send_msg(657)

    def _ls(self, *args):
        """查看用户目录文件函数"""
        if self.user["user_id"] is not None:
            if self.user["type"] == "用户":
                path = self.user["user_path"]
                path_list = os.listdir(path)
                self.send_msg(658, {"data": path_list})
            else:
                self.send_msg(664)  # 管理员没有此类功能
        else:
            self.send_msg(657)   # 用户没登陆

    def _cd(self, *args):
        """切换目录功能"""
        data_header = args[0]
        where = data_header["where"]
        if self.user["user_id"] is not None:
            if self.user["type"] == "用户":
                path = self.user["user_path"]  # 当前路径
                path_list = os.listdir(path)
                username = self.user["user_id"].get_obj_by_id().username
                user_obj = self.user["user_id"].get_obj_by_id()
                if where in path_list:
                    change_path = os.path.join(path, where)  # 要切换的目录
                    if os.path.isfile(change_path):  # 要切换的目录是文件则不切换
                        self.send_msg(658)
                    else:
                        self.user["user_path"] = change_path  # 更新路径
                        where_list = self.path_parser(change_path, username)  # 用最新路径来获取路径前标列表
                        where = '\\'.join(where_list)  # 生成路径前标
                        self.send_msg(658, {"where": where})
                else:
                    ret = self.cd_parser(where)  # 解析..操作,返回语法正确性及回退格数
                    if ret["status"]:
                        length = ret["length"]
                        current_where_list = self.path_parser(path, username)
                        if length < len(current_where_list):  # 如果长度小于路径长度，说明可以进行回退
                            for i in range(length):
                                current_where_list.pop()
                            where = '\\'.join(current_where_list)  # 获得最新路径前标
                            current_path = user_obj.home_path  # 获取用户家目录
                            current_where_list.pop(0)  # 将用户名剔除
                            tmp_list = current_where_list
                            for j in tmp_list:
                                current_path = os.path.join(current_path, j)
                            self.user["user_path"] = current_path  # 更新路径
                            self.send_msg(658, {"where": where})  # 发送最新路径前标
                        else:
                            self.send_msg(660)  # 权限不足
                    else:
                        self.send_msg(665)  # 命令错误
            else:
                self.send_msg(664)  # 管理员没有此类功能
        else:
            self.send_msg(657)  # 用户没登陆

    def _mkdir(self, *args):
        """创建目录函数"""
        data_header = args[0]
        dir_info = data_header["dir_info"]
        if self.user["user_id"] is not None:
            if self.user["type"] == "用户":
                user_obj = self.user["user_id"].get_obj_by_id()
                path = self.user["user_path"]
                mk_path = os.path.join(path, dir_info)
                if os.path.exists(mk_path):
                    self.send_msg(666)
                else:
                    os.mkdir(mk_path)
                    action_logger.info("用户%s创建了目录%s" % (user_obj.username, mk_path))
                    self.send_msg(658)
            else:
                self.send_msg(664)  # 管理员没有此类功能
        else:
            self.send_msg(657)   # 用户没登陆

    def _put(self, *args):
        """接收客户端文件函数"""
        data_header = args[0]
        if self.user["user_id"] is not None:
            if self.user["type"] == "用户":
                file_name = data_header["file_name"]  # 获取文件名
                size = data_header["size"]  # 获取文件大小
                user_obj = self.user["user_id"].get_obj_by_id()  # 获取用户对象
                user_home_path = user_obj.home_path  # 获取用户总目录
                user_home_path_size = os.path.getsize(user_home_path)  # 获取用户目前总目录大小
                quota = int(user_obj.quota)  # 获取用户磁盘配额大小
                future_user_home_path_size = user_home_path_size + size  # 接收文件之后用户总目录大小
                if future_user_home_path_size > quota:  # 接收文件之后超出磁盘配额，则拒绝接收文件
                    self.send_msg(667)  # 超出磁盘配额
                else:
                    data = None
                    len_recv_data = 0
                    md5_obj = hashlib.md5()  # 生成一个md5对象
                    current_path = self.user["user_path"]  # 当前用户目录
                    file_path = os.path.join(current_path, file_name)  # 生成文件绝对路径
                    if user_obj.file_put_dict.get(file_path):  # 如果之前没传完文件就退出则会有此内容
                        file_obj = open(file_path, "ab")
                        file_obj.seek(user_obj.file_put_dict[file_path])  # 将文件游标放置于上次退出处
                        file_obj.tell()
                        data = {"cur": user_obj.file_put_dict[file_path]}  # 将此前光标位置封装，之后发送至客户端
                        len_recv_data = user_obj.file_put_dict[file_path]  # 将已经接收的文件大小更新
                    else:
                        file_obj = open(file_path, "wb")
                    self.send_msg(658, data)
                    while len_recv_data < size:
                        try:
                            recv_data = self.request.recv(4096)
                        except ConnectionResetError as e:  # 客户端异常退出，保存此次文件传输大小
                            print(e)
                            user_obj.file_put_dict[file_path] = file_obj.tell()
                            user_obj.save()  # 保存对象
                            break
                        file_obj.write(recv_data)
                        md5_obj.update(recv_data)
                        len_recv_data += len(recv_data)
                    else:
                        print("文件接收完毕！")
                        if user_obj.file_put_dict.get(file_path):  # 如果之前没传完文件就退出则会有此内容
                            user_obj.file_put_dict.pop(file_path)  # 文件传输完毕，则删除此记录
                            user_obj.save()  # 保存对象
                        action_logger.info("用户[%s]上传了文件[%s]" % (user_obj.username, file_name))
                        self.send_msg(658, {"md5": md5_obj.hexdigest()})
                        file_obj.close()
            else:
                self.send_msg(654)  # 管理员没有此类功能
        else:
            self.send_msg(657)  # 用户没登陆

    def _get(self, *args):
        """向客户端发送文件函数"""
        data_header = args[0]
        if self.user["user_id"] is not None:
            if self.user["type"] == "用户":
                file_name = data_header["file_name"]  # 获取文件名
                user_obj = self.user["user_id"].get_obj_by_id()  # 获取用户对象
                current_path = self.user["user_path"]  # 当前用户目录
                file_path = os.path.join(current_path, file_name)  # 生成文件绝对路径
                if not os.path.isfile(file_path):
                    self.send_msg(659)  # 服务器端没有此文件
                    return
                file_size = os.path.getsize(file_path)  # 获取文件大小
                data = {"size": file_size}
                md5_obj = hashlib.md5()  # 生成一个md5对象
                self.send_msg(658, data)  # 向客户端发送验证通过消息和文件大小
                info = json.loads(self.request.recv(1024).decode())  # 等待客户端确认信息
                file_obj = open(file_path, "rb")  # 打开一个文件
                if info.get("cur"):  # 如果之前没传完文件就退出则会有此内容
                    if info["cur"] < file_size:
                        cur = info["cur"]
                        file_obj.seek(cur)
                        file_obj.tell()
                for line in file_obj:
                    try:
                        self.request.send(line)
                    except ConnectionAbortedError as e:  # 客户端异常退出
                        print(e)
                        return
                    except ConnectionResetError as e:  # 客户端异常退出
                        print(e)
                        return
                    md5_obj.update(line)
                print("文件发送完毕！")
                action_logger.info("用户[%s]下载了文件[%s]" % (user_obj.username, file_name))
                self.send_msg(658, {"md5": md5_obj.hexdigest()})
                file_obj.close()
            else:
                self.send_msg(654)  # 管理员没有此类功能
        else:
            self.send_msg(657)  # 用户没登陆
