#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
import json
import os

def show():
    '''
    开始界面
    :return:
    '''
    print('''======================================================
*                                                    *
*               欢迎访问地区查询系统                 *
*                                                    *
======================================================''')

def branch(things):
    '''
    分行显示函数
    :param things: 想要分行显示的内容
    :return: 无返回结果
    '''
    count = 0
    limit = 3                                              #限制每行打印元素个数
    for i in things:
        if count % limit == 0 and count != 0:              #超过限制个数会另起一行
            print('\n%s' % i, end=''.center(10," "))
            count += 1
        else:                                              #其余情况包括第一次正常打印
            print(i, end=''.center(10," "))
            count += 1


if __name__ == "__main__":
    china_dict = json.load(open("china_dict.js", 'r'))
    tmp_list = []                                          #临时列表，用来存循环打印的地区字典
    while True:
        os.system("cls")                                   #清屏
        show()                                             #开始展示界面
        show_list = []                                     #展示列表
        diqu_list = []                                     #每个地区存放列表
        for index,keys in enumerate(china_dict):
            show_list.append("%s、%s"%(index+1,keys))      #将期望打印的内容放入展示列表
            diqu_list.append(keys)
        branch(show_list)                                  #分行打印
        print("\n======================================================")
        print("功能清单： \033[31;1mR\033[1m返回上级  \033[31;1mB\033[1m退出")
        choose = input("请选择你想查询的地区:").strip()              #用户输入
        if choose == "B":
            break
        if choose == "R":
            if len(tmp_list) == 0:                         #临时列表为空，继续打印本次字典内容
                continue
            else:
                china_dict = tmp_list[-1]
                tmp_list.pop()
                continue
        if len(choose) == 0:
            continue
        elif choose in china_dict.keys():                  #用户输入地区采用此种处理方式
            tmp_list.append(china_dict)                    #将本次字典放入临时列表中
            china_dict = china_dict[choose]
            continue
        elif choose.isdigit() and int(choose) >0 and int(choose) <= len(diqu_list):#用户输入数字，采用此种处理方式
            tmp_list.append(china_dict)
            china_dict = china_dict[diqu_list[int(choose)-1]]
        else:
            continue

