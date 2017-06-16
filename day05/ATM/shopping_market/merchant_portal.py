#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
import json
import os

# goods_dict = {"iphone":[6000,50]}


def goods_show():
    '''
    商品展示界面
    :return: 返回商品信息
    '''
    goods_dict = json.load(open("goods_dict.jsonon","r"))
    tmp_list = []                                          # 商品信息临时存放
    print('商品列表'.center(70, '='))
    print('%-5s  %-10s  %-10s  %-10s'%('编号', '商品名称', '商品单价(元)', '商品数量(个)'))
    for index,good in enumerate(goods_dict):
        print('%-5d  %-15s  %-20d  %-10d'%(index+1,good,goods_dict[good][0],goods_dict[good][1]))
        tmp_list.append(good)
    print(''.center(74, '='))
    print('功能清单：', '\033[31;1mA\033[1m增加商品  ', '\033[31;1mD\033[1m删除商品  ', '\033[31;1mC\033[1m修改商品信息  ',
     '\033[31;1mQ\033[1m退出')
    return tmp_list

def add_goods():
    '''
    增加商品功能
    :return: 无返回结果
    '''
    goods_dict = json.load(open("goods_dict.jsonon", "r"))
    while True:
        good_name = input("请输入要添加的商品名称：").strip()
        good_price = input("请输入要添加的商品价格：").strip()
        good_num = input("请输入要添加的商品数量：").strip()
        if good_name in goods_dict:
            print("该商品已存在，您可以使用修改功能对其进行修改！")
            return
        elif good_price.isdigit() and good_num.isdigit():
            goods_dict[good_name] = [int(good_price),int(good_num)]
            json.dump(goods_dict,open("goods_dict.jsonon", "w"))
            print("\033[31;1m%s\033[0m添加成功！"%good_name)
            return
        else:
            print("商品价格或者商品数量输入有误！")
            continue

def delete_goods(goods_list):
    '''
    删除商品功能
    :param goods_list: 临时商品列表
    :return: 无返回结果
    '''
    goods_dict = json.load(open("goods_dict.jsonon", "r"))
    while True:
        choose = input("请选择想要删除的商品：").strip()
        if choose in goods_dict:
            del goods_dict[choose]
            json.dump(goods_dict, open("goods_dict.jsonon", "w"))
            print("\033[31;1m%s\033[0m删除成功！"%choose)
            return
        elif choose.isdigit() and int(choose)>0 and int(choose)<=len(goods_list):
            del goods_dict[goods_list[int(choose)-1]]
            json.dump(goods_dict, open("goods_dict.jsonon", "w"))
            print("\033[31;1m%s\033[0m删除成功！" % goods_list[int(choose)-1])
            return
        else:
            print("输入有误，或者要删除的商品不存在！")
            continue

def change_goods(goods_list):
    '''
    修改商品功能
    :param goods_list:  临时商品列表
    :return: 无返回结果
    '''
    goods_dict = json.load(open("goods_dict.jsonon", "r"))
    while True:
        choose = input("请输入您想修改的商品编号：").strip()
        if choose.isdigit() and int(choose)>0 and int(choose)<=len(goods_list):
            change_name = input("请输入新的商品名称：").strip()
            change_price = input("请输入新的商品价格：").strip()
            change_num = input("请输入新的商品数量：").strip()
            if change_name == goods_list[int(choose)-1] and change_price.isdigit() and change_num.isdigit():
                goods_dict[change_name] = [int(change_price),int(change_num)]
                json.dump(goods_dict, open("goods_dict.jsonon", "w"))
                print("\033[31;1m%s\033[0m修改成功！" % goods_list[int(choose) - 1])
                return
            elif change_name != goods_list[int(choose)-1] and change_price.isdigit() and change_num.isdigit():
                goods_dict[change_name] = [int(change_price), int(change_num)]
                del goods_dict[goods_list[int(choose) - 1]]
                json.dump(goods_dict, open("goods_dict.jsonon", "w"))
                print("\033[31;1m%s\033[0m修改成功！新名称为\033[31;1m%s\033[0m" % (goods_list[int(choose) - 1],change_name))
                return
            else:
                print("输入有误，请重新输入！")
                continue
        else:
            print("您的输入有误，请重新输入！")
            continue

if __name__ == "__main__":
    while True:
        goods_list = goods_show()
        choose = input("请输入功能选项：").strip()
        if choose == "A":                                  #增加商品功能
            add_goods()
        elif choose == "D":                                #删除商品功能
            delete_goods(goods_list)
        elif choose == "C":                                #修改商品功能
            change_goods(goods_list)
        elif choose == "Q":                                #退出
            break
        else:
            print("输入不规范，请重新输入！")
            continue
