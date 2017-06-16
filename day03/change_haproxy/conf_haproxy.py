#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
import os
import time
def show():
    '''
    欢迎界面
    :return: 无返回值
    '''
    os.system('cls')
    print('''
==========================================================================
*                                                                        *
*                          配置文件修改系统                              *
*                                                                        *
==========================================================================
1.查询配置文件
2.添加或修改配置文件
3.删除配置文件
4.退出
            '''
          )

def get_info(backend_ip):
    '''
    获取backend_ip下所有server信息函数
    :param backend_ip:
    :return: 返回所有server信息
    '''
    server_list = []
    with open("haproxy.txt", "r", encoding="utf-8") as f:
        print_flag = False                                 #输出控制，只会打印相应的信息
        for line in f:
            if line.startswith("backend") and line.strip().endswith(backend_ip):
                print_flag = True
                continue
            elif not line.startswith(" "):
                print_flag = False
                continue
            if print_flag:server_list.append(line.strip())
    return server_list

def copy_file():
    '''
    备份函数
    :return: 无返回值
    '''
    date = time.strftime('%Y%m%d%H%M%S')
    copy_file_name = "haproxy-%s.txt"%date
    with open("haproxy.txt","r",encoding="utf-8") as f1 \
        ,open(os.path.join("copy_file",copy_file_name),"w", encoding="utf-8") as f2:
        for line in f1:
            f2.write(line)
    print("文件%s备份完毕"%copy_file_name)
    time.sleep(1)

def select():
    '''
    查询功能
    :return: 无返回值
    '''
    exit_flag = True
    while exit_flag:
        backend_ip = input("请输入backend_ip:").strip()
        if len(backend_ip) == 0: continue
        server_list = get_info(backend_ip)
        if len(server_list) == 0:
            print("backend_ip不存在，请检查后输入")
            continue
        else:
            print("%s的server信息如下：" % backend_ip)
            for info in server_list:
                print(info)
            while True:
                choose = input("是否继续查询[Y/N]:").strip()
                if choose == "Y":break
                else:
                    exit_flag = False
                    break

def change():
    '''
    添加&修改功能
    :return: 无返回值
    '''
    while True:
        try:
            arg = eval(input("请输入要添加或修改的内容：").strip())
            if len(arg) == 0: continue
            server_info = "server %s  weight %s maxconn %s" % (arg["record"]["server"],
                                                               arg["record"]["weight"],
                                                               arg["record"]["maxconn"])
            server_list = get_info(arg["backend"])
        except Exception as e:
            print(e)
            continue
        if server_list:
            ip_list = []
            server_info_list = []
            for i in server_list:
                tmp = i.split(" ")                         #将server信息分裂，这样可以得到每一个信息的值
                tmp.remove("")
                if len(tmp)==0:continue
                else:
                    ip_list.append(tmp[1])
                    server_info_list.append(tmp)
            if arg["record"]["server"] in ip_list:
                old_server_info_list = server_info_list[ip_list.index(arg["record"]["server"])]
                old_server_info = "server %s  weight %s maxconn %s" % (old_server_info_list[1],
                                                                       old_server_info_list[3],
                                                                       old_server_info_list[5])
                if int(old_server_info_list[3]) == int(arg["record"]["weight"]) \
                and int(old_server_info_list[5]) == int(arg["record"]["maxconn"]): #如果其他信息都匹配则无需修改
                    print("配置信息相同，无需修改！")
                    time.sleep(1)
                    continue
                else:                                                 #只要有一项不匹配，则进行修改
                    with open("haproxy.txt", "r", encoding="utf-8") as f1, \
                            open("haproxy_new.txt", "w", encoding="utf-8") as f2:
                        for line in f1:
                            if line.strip() == old_server_info:       #要修改的信息和文件中信息匹配
                                f2.write("        %s\n"%server_info)  #将新的信息覆盖原有的server信息
                            else:
                                f2.write(line)                        #其余部分不变
                            f1.flush(), f2.flush()
                    copy_file()                                       # 备份历史文件
                    os.remove("haproxy.txt")
                    os.rename("haproxy_new.txt", "haproxy.txt")
                    print('''%s修改完成\n新的server信息：%s'''%(old_server_info,server_info))  #将所修改的server信息打印出来
                time.sleep(1)
                break
            else:                                          #ip不存在则创建
                with open("haproxy.txt", "r", encoding="utf-8") as f1, \
                        open("haproxy_new.txt", "w", encoding="utf-8") as f2:
                    for line in f1:
                        if line.startswith("backend") and line.strip().endswith(arg["backend"]):
                            f2.write(line)
                            f2.write("        %s\n" % server_info)
                        else:
                            f2.write(line)                 # 其余部分不变
                        f1.flush(), f2.flush()
                copy_file()                                # 备份历史文件
                os.remove("haproxy.txt")
                os.rename("haproxy_new.txt", "haproxy.txt")
                print('''%s追加完毕''' % server_info)
                time.sleep(1)
                break
        else:
            backend_title = "backend %s"%arg["backend"]
            with open("haproxy.txt", "r", encoding="utf-8") as f1, \
                    open("haproxy_new.txt", "w", encoding="utf-8") as f2:
                for line in f1:
                    f2.write(line)                         #其余部分不变
                f2.write("\n%s\n"%backend_title)           #添加一个backend
                f2.write("        %s\n"%server_info)       #添加backend下的信息
                f1.flush(), f2.flush()
            print('''%s添加完成''' % arg["backend"])
            copy_file()                                    # 备份历史文件
            os.remove("haproxy.txt")
            os.rename("haproxy_new.txt", "haproxy.txt")
            time.sleep(1)
            break

def delete_info():
    '''
    删除功能
    :return:
    '''
    while True:
        try:
            arg = eval(input("请输入要删除的内容：").strip())
            if len(arg) == 0: continue
            server_info = "server %s  weight %s maxconn %s" % (arg["record"]["server"],
                                                               arg["record"]["weight"],
                                                               arg["record"]["maxconn"])
            server_list = get_info(arg["backend"])
        except Exception as e:
            print(e)
            continue
        if server_list:
            flag = True                                    #flag为真，代表循环里面没有进行删除操作
            delete_flag = True                             #用来控制删除对应backend下的server信息
            for i in server_list:
                if i == server_info:
                    with open("haproxy.txt","r",encoding="utf-8") as f1, \
                         open("haproxy_new.txt", "w", encoding="utf-8") as f2:
                        for line in f1:
                            if line.startswith("backend") and line.strip().endswith(arg["backend"])\
                                and len(server_list) == 1:#如果该backend下只有一条信息，则backend也删除
                                delete_flag = False
                                continue
                            elif line.startswith("backend") and line.strip().endswith(arg["backend"]):
                                delete_flag = False
                            if not delete_flag and line.strip()==server_info:
                                delete_flag = True
                                continue
                            else:f2.write(line)
                        f1.flush(),f2.flush()
                    copy_file()  # 备份历史文件
                    os.remove("haproxy.txt")
                    os.rename("haproxy_new.txt", "haproxy.txt")
                    print("%s删除完成" % server_info)
                    flag = False
                else:
                    continue
            if flag:print("您要修改的server信息不存在，或者输入有误，请检查后输入！")
            time.sleep(1)
            break
        else:
            print("您要删除的内容不存在")
            time.sleep(1)
            break

if __name__ == '__main__':
    while True:
        show()                                             #欢迎界面
        num = input('请输入功能编号：').strip()
        if num.isdigit() and int(num)>0 and int(num) <=4:
            num = int(num)
            if num == 1:
                select()                                   #查询功能
            elif num == 2:
                change()                                   #添加修改功能
            elif num == 3:
                delete_info()                              #删除功能
            elif num == 4:
                break
        elif len(num) == 0:
            continue
        else:
            print('您的输入有误，请重新输入！')
            continue