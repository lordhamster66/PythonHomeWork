#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
import json
import os
import time

#customer_dict = {"Breakering":{
#                           "passwd":"666666",
#                           "balance":50000,
#                           "last_buytime":"2017-04-04",
#                           "login_times":0,
#                           "buy_info":{"2017-04-04":
#                                       {"iphone":[6000,1]}}
#                                }
# }

#goods_dict = {"iphone":[6000,50]}
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

def register():
    '''
    注册界面
    :return:无返回结果
    '''
    print('''
==========================================================================
*                                                                        *
*                     欢迎注册Breakering购物商城                         *
*                                                                        *
==========================================================================
    ''')
    while True:
        username = input("请输入您的用户名:")
        passwd = input("请输入您的密码:")
        try:
            customer_dict = json.load(open("customer_dict.json" ,"r"))
            if username in customer_dict:
                print("用户名已经存在，请重新输入!")
                continue
            elif not username.isidentifier():
                print("用户名不合法，请重新输入!")
                continue
            else:
                customer_dict[username] = {}
                customer_dict[username] = {}
                customer_dict[username]["passwd"] = passwd
                customer_dict[username]["balance"] = 0
                customer_dict[username]["last_buytime"] = ""
                customer_dict[username]["login_times"] = 0
                customer_dict[username]["buy_info"] = {}
                json.dump(customer_dict,open("customer_dict.json","w"))
                break
        except Exception:
            customer_dict = {}
            customer_dict[username] = {}
            customer_dict[username]["passwd"] = passwd
            customer_dict[username]["balance"] = 0
            customer_dict[username]["last_buytime"] = ""
            customer_dict[username]["login_times"] = 0
            customer_dict[username]["buy_info"] = {}
            json.dump(customer_dict, open("customer_dict.json", "w"))
            break

def login():
    '''
    登陆函数
    :return: 返回登陆结果
    '''
    customer_dict = json.load(open("customer_dict.json", "r"))
    while True:
        username = input("请输入您的用户名:")
        passwd = input("请输入您的密码:")
        if username in customer_dict:
            if passwd == customer_dict[username]["passwd"]:
                if customer_dict[username]["login_times"] == 0:       #用户第一次登陆则会让用户输入工资
                    while True:
                        balance = input("请输入您的工资：").strip()
                        if balance.isdigit():
                            customer_dict[username]["balance"] = int(balance)
                            customer_dict[username]["login_times"] += 1   #用户每登陆一次，登陆次数都会加1
                            json.dump(customer_dict,open("customer_dict.json","w"))
                            return username
                        else:
                            print("输入有误，请重新输入！")
                            continue
                else:
                    customer_dict[username]["login_times"] += 1
                    json.dump(customer_dict, open("customer_dict.json", "w"))
                    return username
            else:
                print("密码错误，请重新输入！")
                continue
        else:
            print("用户名不存在，请重新输入")
            continue

def main_show(username):
    '''
    购物商城欢迎界面
    :param username: 会员用户名
    :return:
    '''
    os.system('cls')
    customer_dict = json.load(open("customer_dict.json","r"))
    balance = customer_dict[username]["balance"]
    last_buytime = customer_dict[username]["last_buytime"]
    login_times = customer_dict[username]["login_times"]
    print('''
==========================================================================
*                                                                        *
*                     欢迎来到Breakering购物平台                         *
*                                                                        *
==========================================================================
会员:{0}您好! 您的当前余额:{1}元 上次购物时间:{2} 登陆次数:{3}
    '''.format(username,balance,last_buytime,login_times)                                     #显示用户各项信息
          )
    return

def goods_show():
    '''
    商品展示界面
    :return: 返回商品信息
    '''
    goods_dict = json.load(open("goods_dict.json","r"))
    tmp_list = []                                          #商品信息临时存放
    print('商品列表'.center(70, '='))
    print('%-5s  %-10s  %-10s  %-10s'%('编号', '商品名称', '商品单价(元)', '商品数量(个)'))
    for index,good in enumerate(goods_dict):
        print('%-5d  %-15s  %-20d  %-10d'%(index+1,good,goods_dict[good][0],goods_dict[good][1]))
        tmp_list.append(good)
    print(''.center(74, '='))
    print('功能清单：', '\033[31;1mS\033[1m商品列表  ', '\033[31;1mG\033[1m购物选项  ', '\033[31;1mC\033[1m查询历史记录  ',
     '\033[31;1mQ\033[1m退出')
    return tmp_list

def shopping(username,goods_list,tmp_buy_dict):
    '''
    购物选项
    :param username: 用户名
    :param goods_list: 商品临时列表
    :param tmp_buy_dict: 临时购买信息存储
    :return:
    '''
    goods_dict = json.load(open("goods_dict.json", "r"))
    customer_dict = json.load(open("customer_dict.json", "r"))
    count = 0
    while True:
        if count != 0:                                     #用户输入过一次之后会询问用户是否继续购买
            exit_or_not = input("请问您需要继续购买吗？[Y/N]").strip()
            if exit_or_not == "Y":
                pass
            elif exit_or_not == "N":
                return tmp_buy_dict                        #用户选择不继续购买，则返回购买信息
            else:
                print("您的输入有误，请重新输入！")
                continue
        index = input("请输入商品编号：").strip()
        num = input("请输入您想购买的数量：").strip()
        count = 1
        if index.isdigit() and int(index)>0 and int(index)<=len(goods_list):
            good = goods_list[int(index)-1]                                        #商品名称
            good_num = goods_dict[good][1]                                         #商品的剩余数量
            if num.isdigit():
                if int(num) <= good_num:
                    total_price = goods_dict[good][0]*int(num)                     #所购买商品的总价格
                    if customer_dict[username]["balance"] < total_price:           #用户余额小于购买商品总价格
                        print("对不起，您的余额不足！")
                        continue
                    else:
                        date = time.strftime("%Y-%m-%d",time.localtime())           #购买日期
                        customer_dict[username]["last_buytime"] = date
                        customer_dict[username]["balance"] -= total_price           #余额更新
                        goods_dict[good][1] -= int(num)                             #商品剩余数量更新
                        if date in customer_dict[username]["buy_info"]:             #同一日期购买
                            if good in customer_dict[username]["buy_info"][date]:   #商品已购买过
                                customer_dict[username]["buy_info"][date][good][1] += int(num)   #商品数量增加
                            else:
                                customer_dict[username]["buy_info"][date][good] = [goods_dict[good][0],int(num)]  #商品没有购买过则创建一个列表
                        else:
                            customer_dict[username]["buy_info"][date] ={}
                            customer_dict[username]["buy_info"][date][good] = [goods_dict[good][0],int(num)]
                        print("您购买了\033[31;1m%d\033[0m件\033[31;1m%s\033[0m,总价格\033[31;1m%d\033[0m,您的余额\033[31;1m%d\033[0m"
                               %(int(num),good,total_price,customer_dict[username]["balance"]))    #每次购买信息提示
                        if good in tmp_buy_dict:                                     #用于退出时打印本次购买商品信息
                            tmp_buy_dict[good][1] += int(num)
                        else:
                            tmp_buy_dict[good] = [goods_dict[good][0],int(num)]
                        json.dump(customer_dict, open("customer_dict.json", "w"))
                        json.dump(goods_dict, open("goods_dict.json", "w"))
                else:
                    print("对不起，商品库存不足！")
                    continue
            else:
                print("对不起，您的输入有误，请重新输入！")
                continue
        else:
            print("商品编号输入有误，请重新输入！")
            continue

def view(username):
    '''
    查询历史记录选项
    :param username: 用户名
    :return: 无返回结果
    '''
    customer_dict = json.load(open("customer_dict.json", "r"))
    info = customer_dict[username]["buy_info"]
    all_price = 0                                          #用来计算总共的花费
    print('历史记录'.center(70, '='))
    print('%-8s  %-5s  %-10s  %-10s %-10s' % ('日期', '编号', '商品名称', '已购买数量(个)','总计价格(元)'))
    for date in info:
        for index,good in enumerate(info[date]):
            price = info[date][good][0]*info[date][good][1]
            all_price += price
            print('%-10s  %-10s  %-10s  %-15s %-10s'%(date,index+1,good,info[date][good][1],price))
    print(''.center(74, '='))
    print("总计",''.center(45, ' '),"\033[31;1m%d元\033[0m"%all_price)
    print(''.center(74, '='))
    while True:
        choose = input("是否返回商品列表界面[Y/N]:")
        if choose == "Y":
            return
        elif choose == "N":
            continue
        else:
            print("输入有误，请重新输入！")
            continue

def customer_quit(username,tmp_buy_dict):
    '''
    退出时打印信息
    :param username: 用户名
    :param tmp_buy_dict: 临时购买信息
    :return: 无返回结果
    '''
    customer_dict = json.load(open("customer_dict.json", "r"))
    balance = customer_dict[username]["balance"]
    if len(tmp_buy_dict) == 0:
        print("亲爱的用户，您本次未购买任何商品，您的当前余额为：\033[31;1m%s元\033[0m"%balance)
    else:
        all_price = 0  # 用来计算总共的花费
        msg = "%s本次消费记录"%username
        print(msg.center(70, '='))
        print('%-5s  %-10s  %-10s %-10s' % ('编号', '商品名称', '本次购买数量(个)', '总计价格(元)'))
        for index,good in enumerate(tmp_buy_dict):
            price = tmp_buy_dict[good][0]*tmp_buy_dict[good][1]
            all_price += price
            print('%-8s  %-20s  %-10s %-10s' %(index+1,good,tmp_buy_dict[good][1],price))
        print(''.center(74, '='))
        print("总计", ''.center(35, ' '), "\033[31;1m%d元\033[0m" % all_price)
        print("您的当前余额", ''.center(35, ' '), "\033[31;1m%d元\033[0m" % balance)
        print(''.center(74, '='))

if  __name__ == "__main__":                                #主程序入口
    exit_flag = False
    tmp_buy_dict = {}                                      #临时购买信息存储
    while not exit_flag:
        ret = show()
        if ret == "R":                                     #注册选项
            register()
            continue
        elif ret == "L":                                   #登陆选项
            login_ret = login()
            username = login_ret
            while True:
                main_show(username)                        #显示欢迎界面，及用户基础信息
                goods_list = goods_show()                  #商品展示
                option = input("请问您目前想要做什么？").strip()
                if option == "S":                          #商品列表展示
                    continue
                elif option == "G":                        #购物选项
                    tmp_buy_dict = shopping(username,goods_list,tmp_buy_dict)
                elif option == "C":                        #查询历史消费记录
                    view(username)
                elif option == "Q":                        #退出选项
                    exit_flag = True
                    customer_quit(username,tmp_buy_dict)
                    break
                else:
                    print("输入错误，请重新输入！")
                    continue
        elif ret == "Q":
            break
        else:
            print("您的输入有误，请重新输入！")
            continue










