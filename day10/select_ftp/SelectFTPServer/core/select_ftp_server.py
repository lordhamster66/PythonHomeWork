#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/11
"""服务器主要功能模块"""
import selectors
import socket
import json
import queue
import os
from conf import settings
from core import mylogger
from core.user import User

# 创建日志对象
action_logger = mylogger.Mylogger(settings.ACTION_LOGPATH, "action", settings.LOG_LEVEL).get_logger()

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


class MYSelectFTP(object):
    """自定义select ftp类"""
    def __init__(self):
        self.sel = selectors.DefaultSelector()
        self.sock = socket.socket()
        self.sock.bind((settings.HOST, settings.PORT))
        self.user_info = {}  # 存储连接对应的用户信息
        self.msg_dic = {}  # 存储对应连接的消息队列
        self.sock.listen(100)
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, self.accept)

    def start(self):
        """开始服务器"""
        print("\033[32;1m服务器已启动！\033[0m")
        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def accept(self, sock, mask):
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)

    @staticmethod
    def send_msg(conn, status_code, data=None):
        """向客户端返回数据"""
        msg = {'status_code': status_code, 'status_msg': STATUS_CODE[status_code]}
        if data:
            msg.update(data)
        conn.send(json.dumps(msg).encode())

    def read(self, conn, mask):
        """获取客户端指令，然后分发任务"""
        try:
            data = conn.recv(1024)  # Should be ready
            self.msg_dic[conn] = queue.Queue()  # 创建或者重置消息队列
            data_header = json.loads(data.decode())  # 获取信息头
            if hasattr(self, "_%s" % data_header["action"]):
                func = getattr(self, "_%s" % data_header["action"])
                func(conn, data_header)
        except (ConnectionAbortedError, ConnectionResetError) as e:
            print(e)
            print('closing', conn)
            self.sel.unregister(conn)  # 注销连接，不再监听
            if self.msg_dic.get(conn):
                del self.msg_dic[conn]  # 删除连接对应的消息队列
            if self.user_info.get(conn):
                del self.user_info[conn]  # 删除连接对应的用户信息
            conn.close()

    def _auth(self, conn, data_header):
        """注册功能"""
        username = data_header["username"]
        password = data_header["password"]
        user_obj = User()
        ret = user_obj.enroll(username, password, action_logger)
        if ret == 651:
            user_obj.create_directory()
            user_obj.save()
        self.send_msg(conn, ret)

    def _login(self, conn, data_header):
        """登陆功能"""
        username = data_header["username"]
        password = data_header["password"]
        ret = User.login(username, password, action_logger)
        if ret["status"] == 654:
            self.user_info[conn] = {}
            self.user_info[conn]["obj"] = ret["obj"]
            home_path = os.path.join(settings.USER_DIRECTORY_DIR, ret["obj"].username)
            self.user_info[conn]["home"] = home_path
        self.send_msg(conn, ret["status"])

    def _ls(self, conn, data_header):
        """查看用户目录文件"""
        if self.user_info.get(conn) is not None:
            home_path = self.user_info[conn]["home"]  # 获取用户目录地址
            file_list = os.listdir(home_path)
            data = {"data": file_list}
            self.send_msg(conn, 657, data)
        else:
            self.send_msg(conn, 656)

    def _put(self, conn, data_header):
        """上传文件至服务器调度功能"""
        if self.user_info.get(conn) is not None:
            self.send_msg(conn, 657)  # 发送验证成功信息，这样服务端就准备好接收客户端发送的文件内容了
            filename = data_header["filename"]
            file_path = os.path.join(self.user_info[conn]["home"], filename)
            file_size = data_header["file_size"]
            recvd_size = 0
            f = open(file_path, "wb")
            info = {
                "file_size": file_size,
                "file_obj": f,
                "recvd_size": recvd_size
            }
            self.msg_dic[conn].put(info)
            self.sel.unregister(conn)
            self.sel.register(conn, selectors.EVENT_READ, self.write_file)
        else:
            self.send_msg(conn, 656)  # 客户没登陆

    def write_file(self, conn, mask):
        """向服务器写入文件功能"""
        info = self.msg_dic[conn].get()
        while info["recvd_size"] < info["file_size"]:  # 接收到的数据小于文件大小则一直接收
            try:
                line = conn.recv(1024)
            except BlockingIOError:  # 没有数据则下次再收
                self.msg_dic[conn].put(info)  # 保存此次接收信息
                return
            else:  # 正常收到数据,则执行以下代码
                info["file_obj"].write(line)
                info["recvd_size"] += len(line)
        else:
            print("接收完毕!")
            info["file_obj"].close()  # 关闭文件句柄
            self.sel.unregister(conn)
            self.sel.register(conn, selectors.EVENT_READ, self.read)

    def _get(self, conn, data_header):
        """发送文件至客户端调度功能"""
        if self.user_info.get(conn) is not None:
            filename = data_header["filename"]
            filepath = os.path.join(self.user_info[conn]["home"], filename)
            if os.path.isfile(filepath):
                file_size = os.path.getsize(filepath)
                data = {"file_size": file_size}
                self.send_msg(conn, 657, data)
                while True:  # 这时需要等待客户端确认
                    try:
                        conn.recv(1024)
                    except BlockingIOError:  # 等待客户端确认
                        pass
                    except (ConnectionAbortedError, ConnectionResetError) as e:  # 客户端异常断开
                        print(e)
                        self.sel.unregister(conn)  # 注销连接，不再监听
                        if self.msg_dic.get(conn):
                            del self.msg_dic[conn]  # 删除连接对应的消息队列
                        if self.user_info.get(conn):
                            del self.user_info[conn]  # 删除连接对应的用户信息
                        conn.close()
                        return
                    else:
                        break
                f = open(filepath, "rb")
                info = {
                    "file_size": file_size,
                    "file_obj": f,
                    "send_size": 0
                }
                self.msg_dic[conn].put(info)
                self.sel.unregister(conn)
                self.sel.register(conn, selectors.EVENT_WRITE, self.send_file)
            else:
                self.send_msg(conn, 658)  # 服务端没有此文件
        else:
            self.send_msg(conn, 656)  # 客户没登陆

    def send_file(self, conn, mask):
        """向客户端发送文件内容功能"""
        info = self.msg_dic[conn].get()
        line = info["file_obj"].readline()
        if info["send_size"] < info["file_size"]:
            conn.sendall(line)
            info["send_size"] += len(line)
            self.msg_dic[conn].put(info)
        else:
            print("发送完毕!")
            info["file_obj"].close()  # 关闭文件句柄
            self.sel.unregister(conn)
            self.sel.register(conn, selectors.EVENT_READ, self.read)
