#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/7/8
"""
ssh交互模块
"""
import os
import sys
import time
import socket
import select
import paramiko
import threading
from core import db_conn
from core import table_structure
from paramiko.py3compat import u

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan, user_name, host):
    if has_termios:
        posix_shell(chan, user_name, host)
    else:
        windows_shell(chan, user_name, host)


def posix_shell(chan, username, host):

    sys.stdout.write("\033[32;1m终端启动成功...\033[0m\r\n\r\n")

    # 获取原tty属性
    old_tty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)

        flag = False
        temp_list = []

        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    # 如果用户上一次点击的是tab键，则获取返回的内容写入在记录中
                    if flag:
                        if x.startswith('\r\n'):
                            pass
                        else:
                            temp_list.append(x)
                        flag = False
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                # 读取用户在终端数据每一个字符
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                # 如果用户点击TAB键
                if x == '\t':
                    flag = True
                else:
                    # 未点击TAB键，则将每个操作字符记录添加到列表中，以便之后写入文件
                    temp_list.append(x)

                # 如果用户敲回车，则将操作记录写入文件
                if x == '\r':
                    # 开始写入日志
                    times = time.strftime('%Y-%m-%d %H:%M')
                    obj = table_structure.AuditLog(time=times, username=username, host=host, cmd=''.join(temp_list))
                    db_conn.session.add(obj)
                    db_conn.session.commit()
                    temp_list.clear()
                chan.send(x)

    finally:
        # 重新设置终端属性
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)


def windows_shell(chan, username, host):
    sys.stdout.write("终端启动成功...\r\n\r\n")

    def write_all(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(str(data, encoding='utf-8'))
            sys.stdout.flush()

    writer = threading.Thread(target=write_all, args=(chan,))
    writer.start()

    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        pass


def login():
    """堡垒机用户登陆"""
    while True:
        username = input("请输入用户名:")
        password = input("请输入密码:")
        if len(username) == 0 or len(password) == 0:
            continue
        user_obj = db_conn.session.query(table_structure.User).filter_by(username=username).first()
        if not user_obj:
            print("\033[31;1m用户不存在...\033[0m")
            continue
        if password == user_obj.password:
            print("\033[32;1m登陆成功！\033[0m")
            return user_obj
        else:
            print("\033[31;1m密码错误！\033[0m")

# 程序启动画面
action_show = '''==========================================================================
                            Welcome MyStrongHold

                                                
==========================================================================
      * 使用说明：
            1. 直接登陆您的堡垒机账户
            2. 选择已经授权主机远程登陆
            3. 修改授权请联系管理员

      * 注意：  您的所有操作将被记录
=========================================================================='''


def run():
    """主程序启动函数"""
    print(action_show)
    user_obj = login()
    username = user_obj.username
    host_list = []
    print("用户[{username}]详情".center(30, "=").format(username=username))
    print("1.分组数量：%s" % len(user_obj.groups))
    print("2.未分组数量：%s" % len(user_obj.bind_hosts))
    print("".center(33, "="))
    while True:
        choice = input("请选择其中一种:").strip()
        if len(choice) == 0:
            continue
        if choice == "1":
            if len(user_obj.groups) > 0:
                for group in user_obj.groups:
                    bind_hosts = group.bind_hosts
                    for bind_host in bind_hosts:
                        host_list.append(bind_host)
                break
            else:
                print("\033[31;1m您目前没有分组的机器！\033[0m")
                continue
        elif choice == "2":
            host_list = user_obj.bind_hosts
            break
        else:
            print("\033[31;1m选择有误，请重新选择!\033[0m")
    print("".center(50, "="))
    print('%-8s %-7s %-13s %-10s' % ('序号', '主机名', 'IP地址', '用户名'))
    print("".center(50, "="))
    for index, bind_host in enumerate(host_list):
        print('%-10s %-10s %-15s %-10s' % (index + 1,
                                           bind_host.host.hostname,
                                           bind_host.host.ip,
                                           bind_host.host_user.username))
    print("".center(50, "="))
    while True:
        chose_host = input("选择主机编号 >>:")
        if len(chose_host) == 0:
            continue
        try:
            chose_host = int(chose_host)-1
            host = host_list[chose_host].host.ip
            host_port =host_list[chose_host].host.port
            host_username = host_list[chose_host].host_user.username
            host_password = host_list[chose_host].host_user.password
        except Exception as e:
            print("输入错误...")
            print(e)
            continue
        try:
            tran = paramiko.Transport((host, host_port))
            tran.start_client()
            tran.auth_password(host_username, host_password)
            break
        except Exception as e:
            print("连接失败, 请检查用户名或者密码是否正确...")
            print(e)
            continue

    chan = tran.open_session()
    chan.get_pty()
    chan.invoke_shell()

    interactive_shell(chan, username, host)

    chan.close()
    tran.close()
    sys.exit()

if __name__ == "__main__":
    run()

