#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
# 题目：编写登陆接口
#
# •输入用户名密码
# •认证成功后显示欢迎信息
# •输错三次后锁定

# import  getpass                                         # 为方便pycharm测试没有使用该模块
import json                                               # 序列化模块
import os
import time


def show():
    '''
    开始界面，提供功能清单
    :return:
    '''
    print('''
==========================================================================
*                                                                        *
*                     欢迎来到Breakering世界                             *
*                                                                        *
==========================================================================
    ''')
    print('功能清单：', '\033[31;1mR\033[1m注册选项  ', '\033[31;1mL\033[1m登录选项  ', '\033[31;1mQ\033[1m退出选项  ')
    customer_input = input("请问您目前想干什么？[R/L/Q]:").strip()
    return  customer_input


def black_list_check(name):
    '''
    黑名单检测函数
    :param name: 用户名
    :return: 返回检测结果
    '''
    try:
        black_list = json.load(open("black_list.js","r"))
        if name in black_list:
            return "%s is in black_list"%name
        else:
            return
    except Exception as a:
        print("黑名单文件可能不存在，错误信息：",a)
        black_list = []
        json.dump(black_list, open("black_list.js", "w"))


def add_black_list(name):
    '''
    黑名单增加函数
    :param name: 用户名
    :return: 无返回结果
    '''
    try:
        black_list = json.load(open("black_list.js","r"))
        black_list.append(name)
        json.dump(black_list,open("black_list.js","w"))
    except Exception as a:
        print("黑名单文件可能不存在，错误信息：",a)


def all_check(name,passwd):
    '''
    用户名密码验证函数
    :param name: 用户名
    :param passwd: 密码
    :return: 返回验证结果
    '''
    try:
        customer_dict = json.load(open("customer_dict.json","r"))
        if name in customer_dict.keys():
            if passwd == customer_dict[name]:
                return "right"
            else:
                return  "wrone"
        else:
            return "non-existent"
    except Exception as b:
        print("存放用户名密码文件可能不存在，错误信息：", b)


def login():
    tmp_list = []                                          #用来临时存放用户输入的账户信息
    while True:
        username = input("Please input your name:")
        passwd = input("Please input your passwd:")
        if  black_list_check(username):                    #如果用户名在黑名单里面，则显示锁定信息
            print("该账户已经被锁定!!")
            return "done"
        ret = all_check(username,passwd)
        if  ret == "non-existent":                         #用户名不存在，则让用户重新输入
            print("该用户不存在")
            continue
        elif ret == "wrone":                               #密码错误，则也让用户重新输入
            print("密码错误")
            tmp_list.append(username)                      #密码输错则会将该用户名放入临时列表
            if tmp_list.count(username) == 3:              #如果同一个用户输错三次密码，则锁定该用户
                add_black_list(username)                   #使用放入黑名单函数
                print("该账户已经被锁定!!")
                return "done"
            else:
                continue
        elif ret == "right":                               #用户名密码正确，则显示欢迎信息
            print('''
==========================================================================
*                                                                        *
*                     欢迎进入Breakering的世界                           *
*                          祝您玩的愉快！                                *
*                                                                        *
==========================================================================
 ''')
            return "done"


def register():
    '''
    注册界面
    :return:无返回结果
    '''
    print('''
==========================================================================
*                                                                        *
*                     欢迎注册Breakering世界                             *
*                                                                        *
==========================================================================
    ''')
    while True:
        username = input("Please input your name:")
        passwd = input("Please input your passwd:")
        try:
            customer_dict = json.load(open("customer_dict.json" ,"r"))
            if username in customer_dict.keys():
                print("用户名已经存在，请重新输入!")
                continue
            else:
                customer_dict[username] = passwd
                json.dump(customer_dict,open("customer_dict.json","w"))
                break
        except Exception:
            customer_dict = {}
            customer_dict[username] = passwd
            json.dump(customer_dict, open("customer_dict.json", "w"))
            break


def input_check(customer_input):
    '''
    判断用户选择功能函数
    :param customer_input: 用户选择的对应功能选项
    :return:返回结果
    '''
    if customer_input == "R":                              #如果用户选择注册选项，则进入注册菜单
        register()
    elif customer_input == "L":                            #如果用户选择登陆选项，则进入登陆菜单
        ret = login()
        return ret
    elif customer_input == "Q":                            #如果用户选择退出选项，则退出
        return "quit"
    else:                                                  #输入不规范，则会让用户重新输入
        return "error"


if __name__ == "__main__":                                 # 主程序开始
    while True:
        customer_input = show()
        ret = input_check(customer_input)
        if ret == "quit":
            break
        elif ret == "error":
            print("输入有误，请重新输入！")
            time.sleep(1)                                  # 清屏
            os.system("cls")
            continue
        elif ret == "done":
            break
        else:
            continue

