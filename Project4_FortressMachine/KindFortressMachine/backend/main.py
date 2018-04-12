#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/3/3
import logging
import os
import getpass
import subprocess
import uuid
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.timezone import datetime
from web import models

logger = logging.getLogger(__name__)  # 生成一个以当前模块名为名字的logger实例
c_logger = logging.getLogger("collect")  # 生成一个名为'collect'的logger实例，用于收集一些需要特殊记录的日志

# 程序启动画面
action_show = '''==========================================================================
                    Welcome KindFortressMachine

==========================================================================
      * 使用说明：
            1. 直接登陆您的堡垒机账户
            2. 选择已经授权主机远程登陆
            3. 修改授权请联系管理员
      * 注意：  您的所有操作将被记录
==========================================================================
请在下方输入用户名密码登录'''


class HostManage(object):

    def __init__(self):
        pass

    def interactive(self):
        print(action_show)  # 程序启动画面
        # 验证用户登录
        count = 0  # 计数项
        authenticate_status = False  # 是否验证通过
        user = None  # 登录成功的用户对象
        while count < 3:
            username = input("用户名:").strip()
            password = getpass.getpass("密码:").strip()
            user = authenticate(username=username, password=password)
            if user:
                authenticate_status = True
                break
            else:
                print("\033[31;1mWrong Username or Password!Please try again!\033[0m")

            count += 1
        else:
            logger.warning(f"用户{username}密码输错三次以上！")
            exit("\033[31;1mYou have tried too many times!\033[0m")

        if authenticate_status:  # 登录成功
            logger.info(f"用户{username}登录成功！")
            print("\033[32;1mWelcome KindFortressMachine\033[0m")
            error_message = None  # 错误提示信息
            # 展示用户可以选择的主机组
            while True:
                subprocess.run("clear", shell=True)  # 清屏
                if error_message:  # 有错误信息，则提示
                    print(error_message)
                print(f"用户[{username}]可使用主机组详情".center(30, "="))
                print('%-6s %-7s %-13s' % ('选项', '主机组名', '主机数量'))
                print("%-8s %-7s %-13s" % (0, "未分组", user.bind_hosts.count()))
                for index, host_group in enumerate(user.host_groups.all()):
                    print("%-8s %-7s %-13s" % (index + 1, host_group.name, host_group.bind_hosts.count()))
                print("".center(33, "="))
                user_choice = input("Please chose one(q:exit):").strip()
                bind_host_objs = None  # 用户要选择的组别下面的所有绑定账号的主机对象
                if len(user_choice) == 0:
                    error_message = None  # 清空错误信息
                    continue
                if user_choice == "q":
                    exit("Thanks for using it!")
                elif user_choice.isdigit():  # 用户输入的数字则为已分组的主机
                    user_choice = int(user_choice)
                    host_groups_num = user.host_groups.count()  # 用户所拥有的主机组数量
                    if user_choice > 0 and user_choice <= host_groups_num:
                        bind_host_objs = user.host_groups.all()[user_choice - 1].bind_hosts.all()
                    elif user_choice == 0:  # 说明用户选择的是未分组的机器
                        bind_host_objs = user.bind_hosts.all()
                    else:
                        error_message = "\033[31;1mWrong choice!\033[0m"
                        continue
                else:
                    error_message = "\033[31;1mWrong choice!\033[0m"
                    continue

                # 展示用户可以选择的绑定账号的主机
                error_message = None  # 清空错误信息
                while True:
                    subprocess.run("clear", shell=True)  # 清屏
                    if error_message:  # 有错误信息，则提示
                        print(error_message)
                    print(f"用户[{username}]可使用主机详情".center(60, "="))
                    print('%-6s %-7s %-10s %-7s %-7s' % ('选项', '主机名', '主机地址', '端口', '远程账户名'))
                    for index, bind_host in enumerate(bind_host_objs):
                        print("%-6s %-10s %-18s %-7s %-7s" % (
                            index + 1, bind_host.host.host_name, bind_host.host.ip_adr,
                            bind_host.host.port, bind_host.remote_user.username
                        ))
                    print("".center(63, "="))
                    user_choice = input("Please chose one(q:back):").strip()
                    if len(user_choice) == 0:
                        error_message = None  # 清空错误信息
                        continue
                    if user_choice == "q":
                        error_message = None  # 清空错误信息
                        break
                    elif user_choice.isdigit():
                        user_choice = int(user_choice)
                        if user_choice > 0 and user_choice <= len(bind_host_objs):
                            error_message = None  # 清空错误信息
                            select_bind_host = bind_host_objs[user_choice - 1]  # 获取用户选中的主机
                            unique_id = str(uuid.uuid4())  # 生成一个唯一标识
                            temp_file_abs_path = os.path.join(settings.TEMP_FILES_DIR, unique_id)  # 临时文件存放的绝对路径

                            current_date = datetime.strftime(datetime.now(), "%Y-%m-%d")  # 获取当前日期
                            current_date_audit_log_path = os.path.join(
                                settings.AUDIT_LOG_DIR,
                                current_date
                            )  # 当前日期为名称的文件夹路径

                            # 创建或者确保以当前日期作为文件夹名称的文件夹存在
                            os.makedirs(current_date_audit_log_path, exist_ok=True)
                            # 创建用户本次SSH操作记录的对象
                            session_obj = models.Session.objects.create(
                                user=user,
                                bind_host=select_bind_host,
                                tag=str(temp_file_abs_path)
                            )
                            strace_log_path = os.path.join(current_date_audit_log_path, f"strace_{session_obj.id}.log")

                            subprocess.Popen(
                                f"bash {settings.SESSION_TRACKER_SCRIPT} {str(temp_file_abs_path)} {strace_log_path}",
                                shell=True
                            )

                            # 连接远程主机
                            print(f"\033[32;1mGoing connect to {select_bind_host.host.ip_adr}\033[0m")
                            logger.info(
                                f"""用户{username}连接了{select_bind_host.host.ip_adr},
                                使用远程账户{select_bind_host.remote_user.username}"""
                            )
                            # 连接用户选择的主机
                            subprocess.run("sshpass -p %s ssh %s@%s -o StrictHostKeyChecking=no -E %s" % (
                                select_bind_host.remote_user.password,
                                select_bind_host.remote_user.username,
                                select_bind_host.host.ip_adr, temp_file_abs_path
                            ), shell=True)
                            subprocess.run(f"rm -rf {temp_file_abs_path}", shell=True)  # 将临时文件删除
                            logger.info(f"临时文件{temp_file_abs_path}删除成功！")
                        else:
                            error_message = "\033[31;1mWrong choice!\033[0m"
                            continue
                    else:
                        error_message = "\033[31;1mWrong choice!\033[0m"
                        continue
