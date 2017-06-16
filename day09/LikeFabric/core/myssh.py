#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/4
"""
自定义ssh，sftp类
"""
import paramiko


class Myssh(object):

    def __init__(self, host, port, username, password, logger):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.logger = logger

    def __conn(self):
        """建立连接"""
        try:
            self.transport = paramiko.Transport((self.host, self.port))
            self.transport.connect(username=self.username, password=self.password)
            return "done"
        except Exception as e:
            print("\033[33;1m[%s %s %s]\033[0m:%s" % (self.host, self.port, self.username, e))
            return

    def __close(self):
        """关闭连接"""
        self.transport.close()

    def ssh(self, cmd):
        """执行命令功能"""
        ret = self.__conn()
        if ret:
            ssh = paramiko.SSHClient()
            ssh._transport = self.transport
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout = stdout.read().decode()
            stderr = stderr.read().decode()
            result = stdout if stdout else stderr
            self.__close()
            print("\033[33;1m[%s %s %s]的执行结果为\033[0m：\n%s" % (self.host, self.port, self.username, result))
            self.logger.info("[%s %s %s] 执行了命令 %s" % (self.host, self.port, self.username, cmd))
            return

    def put(self, local_file, server_path):
        """上传文件功能"""
        ret = self.__conn()
        if ret:
            sftp = paramiko.SFTPClient.from_transport(self.transport)
            try:
                sftp.put(local_file, server_path)
                print("\033[33;1m[%s %s %s]上传完成\033[0m" % (self.host, self.port, self.username))
                self.logger.info("[%s %s %s] 接收了文件 %s" % (self.host, self.port, self.username, server_path))
            except FileNotFoundError as e:
                print("\033[33;1m[%s %s %s]\033[0m:%s" % (self.host, self.port, self.username, e))
            except Exception as e:
                print("\033[33;1m[%s %s %s]\033[0m:%s" % (self.host, self.port, self.username, e))
            finally:
                self.__close()

    def get(self, server_file, local_path):
        """下载文件功能"""
        ret = self.__conn()
        if ret:
            sftp = paramiko.SFTPClient.from_transport(self.transport)
            try:
                sftp.get(server_file, local_path)
                print("\033[33;1m[%s %s %s]下载完成\033[0m" % (self.host, self.port, self.username))
                self.logger.info("[%s %s %s] 发送了文件 %s" % (self.host, self.port, self.username, server_file))
            except FileNotFoundError as e:
                print("\033[33;1m[%s %s %s]\033[0m:%s" % (self.host, self.port, self.username, e))
            except Exception as e:
                print("\033[33;1m[%s %s %s]\033[0m:%s" % (self.host, self.port, self.username, e))
            finally:
                self.__close()


# if __name__ == '__main__':
#     h = Myssh("192.168.48.20", 22, "root", "hadoop")
#     h.ssh("ls")
#     h.put('C:\\Users\\Administrator\\Desktop\\module04.zip', '/tmp/module04.zip')
#     h.get('/tmp/module04.zip', 'C:\\Users\\Administrator\\Desktop\\Python-3.5.1.tgz')
