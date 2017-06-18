#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/14
"""RPC客户端主要功能模块"""
import pika
import uuid
import json
import re
import random

# RabbitMQ地址
RABBITMQ_IP = "localhost"

# 帮助清单
HELPER = """===================================================
help  帮助
run  执行命令 eg:run "dir" --hosts 192.168.3.55 10.4.3.4
check_task  检查任务结果 eg:check_task 45334
task_info  检查已经或正在处理的任务详情
quit  退出程序
==================================================="""

# 服务器对应队列
host_to_queue = {
    "192.168.3.55": "server1",
    "10.4.3.4": "server2"
}


class RpcClient(object):
    """RPC客户端类"""

    def __init__(self, server_ip, server_queue):
        """初始化"""
        self.server_ip = server_ip  # 服务器端名称
        self.server_queue = server_queue  # 服务器端队列
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_IP))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            self.on_response,  # 只要一收到消息就调用on_response
            no_ack=True,
            queue=self.callback_queue
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def check_task(self, data_header):
        """检查任务结果"""
        self.response = None
        self.corr_id = str(uuid.uuid4())
        # 发送消息至服务器端，并等待结果
        self.channel.basic_publish(
            exchange='',
            routing_key=self.server_queue,
            properties=pika.BasicProperties(
               reply_to=self.callback_queue,
               correlation_id=self.corr_id,
            ),
            body=data_header
        )
        while self.response is None:
            self.connection.process_data_events()  # 非阻塞版的start_consuming()
        return self.response

    def run(self, data_header, msg_id):
        """发送任务让服务器端运行"""
        # 发送任务至服务器端
        self.channel.basic_publish(
            exchange='',
            routing_key=self.server_queue,
            properties=pika.BasicProperties(
                message_id=msg_id
            ),
            body=data_header
        )


class Handle(object):
    """处理用户命令类"""
    def __init__(self):
        self.client_list = {}  # 存放已经生成的客户端处理对象
        self.task_id_to_client = {}  # 存放任务ID对应的客户端处理对象
        self.task_id_to_cmd = {}  # 存放任务ID对应的任务内容

    def _run(self, cmd, *args):
        """执行命令功能"""
        tmp_list = [i.strip() for i in cmd.split("--hosts")]
        if len(tmp_list) == 2:
            if '"' in tmp_list[0] or "'" in tmp_list[0]:
                command = [i.strip() for i in re.split(""""|'""", tmp_list[0]) if i][1]
            else:
                command = [i.strip() for i in tmp_list[0].split() if i][1]
            host_list = tmp_list[1].split()
            for host in host_list:  # 检测主机是否存在
                if host not in host_to_queue:
                    print("\033[31;1m主机:%s不存在\033[0m" % host)
                    return
            data_header = {
                "action": "run",
                "cmd": command
            }
            data_header = json.dumps(data_header)
            while True:
                task_id = str(random.randint(10000, 99999))  # 随机生成一个任务ID
                if task_id not in self.task_id_to_client:  # 随机ID不存在，则结束循环，存在的话继续循环直到生成一个不存在的ID
                    break
            self.task_id_to_client[task_id] = []
            for host in host_list:  # 批量给主机发送任务
                if host in self.client_list:
                    client = self.client_list[host]  # 如果该主机已经有一个客户端对象了，则直接调用
                else:
                    client = RpcClient(host, host_to_queue[host])  # 没有的话创建一个客户端对象
                    self.client_list[host] = client  # 将创建好的客户端对象放入列表中
                client.run(data_header, task_id)  # 给主机端发送任务
                self.task_id_to_client[task_id].append(client)  # 存储任务ID对应的客户端对象
                self.task_id_to_cmd[task_id] = command  # 存储任务ID对应的任务内容
            print("task id:", task_id)
        else:
            print("\033[31;1m命令不符合规范！\033[0m")

    def _check_task(self, cmd, *args):
        """检查任务完成情况功能"""
        cmd_list = cmd.split()
        if len(cmd_list) == 2:
            task_id = cmd_list[1]
            data_header = {
                "action": "check_task",
                "task_id": task_id
            }
            data_header = json.dumps(data_header)
            if self.task_id_to_client.get(task_id):
                client_list = self.task_id_to_client[task_id]
            else:
                print("\033[31;1m任务ID不存在!\033[0m")
                return
            for client in client_list:
                result = client.check_task(data_header)
                print("\033[31;1mfrom %s\033[0m" % client.server_ip)
                print(result.decode())
        else:
            print("\033[31;1m命令不符合规范！\033[0m")

    def _task_info(self, *args):
        """检查处理的任务内容"""
        print("".center(26, "*"))
        print("%-6s%-10s%-10s" % ("任务ID", "主机地址", "命令内容"))
        for task_id in self.task_id_to_client:
            for client in self.task_id_to_client[task_id]:
                print("%-6s%-15s%-10s" % (task_id, client.server_ip, self.task_id_to_cmd[task_id]))
        print("".center(26, "*"))

    def start(self):
        """开始处理用户输入的命令"""
        print(HELPER)
        while True:
            cmd = input(">>:").strip()  # 获取用户输入的命令
            if len(cmd) == 0:
                continue
            cmd_list = cmd.split()
            if hasattr(self, "_%s" % cmd_list[0]):  # 反射到对应的函数
                func = getattr(self, "_%s" % cmd_list[0])
                func(cmd)
            else:
                print("\033[31;1m命令错误！\033[0m")

    @staticmethod
    def _help(*args):
        print(HELPER)

    @staticmethod
    def _quit(*args):
        """退出功能"""
        exit()

# run "dir" --hosts 192.168.3.55 10.4.3.4
# check_task 45334
if __name__ == '__main__':
    h = Handle()
    h.start()
