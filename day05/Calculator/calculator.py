#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
该计算器思路：
    1、递归寻找表达式中只含有 数字和运算符的表达式，并计算结果
    2、由于整数计算会忽略小数，所有的数字都认为是浮点型操作，以此来保留小数
使用技术：
    1、正则表达式
    2、递归
请计算表达式： 1 - 2 * ( (60-30 +(-40.0/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )
"""

import re


def jj_ys(new_str):
    '''加减运算函数'''
    new_str = new_str.replace('--','+')
    new_str = new_str.replace('+-', '-')
    new_str = new_str.replace('-+', '-')
    new_str = new_str.replace('++', '+')
    print("新的运算公式：", new_str)
    jj_neirong = re.split('\-|\+', new_str)
    fuhao = re.findall('\-|\+', new_str)
    jj_result = 0
    for index, i in enumerate(jj_neirong):
        if index == 0 and i is not '':
            jj_result = float(i)
        elif i is '':
            jj_result = 0
        elif fuhao[index - 1] is "-":
            jj_result -= float(i)
        elif fuhao[index - 1] is "+":
            jj_result += float(i)
        else:
            print("错误！")
    print("加减运算结果：", jj_result)
    return jj_result


def chengchu(cc_ys):
    '''乘除运算函数'''
    print("乘除运算内容:", cc_ys)
    cc_neirong = re.split('\*|\/', cc_ys)
    cc_fuhao = re.findall('\*|\/', cc_ys)
    cc_result = 1
    for index, i in enumerate(cc_neirong):
        if index == 0 and i is not '':
            cc_result = float(i)
        elif i is '':
            cc_result = 0
        elif cc_fuhao[index - 1] is "/":
            cc_result /= float(i)
        elif cc_fuhao[index - 1] is "*":
            cc_result *= float(i)
        else:
            print("错误！")
    return cc_result


def nei_kuohao_handle(nei_kuohao):
    '''括号内运算函数'''
    cc = re.findall("[^-+]+", nei_kuohao)  # 找出不是“+”和“-”的字符串
    jj = re.findall("(?<!\*|\/)([-+]+)",nei_kuohao)  # 找出连接乘除运算的加减符号
    print("处理前乘除运算内容：",cc)
    cc1 = []
    cc2 = []
    cc3 = []
    for index, i in enumerate(cc):
        i = i.strip()
        if i.endswith("*") or i.endswith("/"):
            cc1.append(i+('-'+cc[index+1]))
            cc2.append(index+1)
        else:
            cc1.append(i)
    for index1 in cc2:
        cc3.append(cc1[index1])
    for item in cc3:
        cc1.remove(item)
    print("处理后乘除运算内容：", cc1)
    print("加减符号：", jj)
    new_l = []
    for index, cc_ys in enumerate(cc1):
        cc_ys_jg = str(chengchu(cc_ys))
        print("乘除运算结果：", cc_ys_jg)
        try:
            if nei_kuohao.startswith("-"):
                 new_l.append(jj[index] + cc_ys_jg)
            elif len(jj) > 1 :
                new_l.append(cc_ys_jg + jj[index])
            else:
                new_l.append(cc_ys_jg + jj[index])
        except:
            new_l.append(cc_ys_jg)
    print("乘除运算处理后内容：", new_l)
    new_str = ""
    for i1 in new_l:
        new_str += i1
    jj_jieguo = jj_ys(new_str)
    return jj_jieguo


def zhu(gongshi):
    print("处理前公式内容：", gongshi)
    gongshi = gongshi.replace(" ", "")
    gongshi = gongshi.replace("（", "(")
    gongshi = gongshi.replace("）", ")")
    if re.search("\([^()]+\)", gongshi):
        nei_kuohao = re.search("\([^()]+\)", gongshi)  # 找到公式最里层括号
        nei_kuohao_neirong = nei_kuohao.group().strip("()")  # 去除括号只保留括号里内容
        print("最里层括号内容：", nei_kuohao_neirong)
        nei_kuohao_jieguo=nei_kuohao_handle(nei_kuohao_neirong)  # 括号内容处理
        gongshi = re.sub("\([^()]+\)", str(nei_kuohao_jieguo), gongshi, 1)  # 用处理结果替代括号内容
        print("最里层括号运算结果：", nei_kuohao_jieguo)
        print("替换后公式：", gongshi)
        return zhu(gongshi)  # 递归直到找不到括号为止
    else:
        nei_kuohao_jieguo=nei_kuohao_handle(gongshi)
        print("最后结果:",nei_kuohao_jieguo)

if __name__ == "__main__":
    gongshi = "-1 - 2 *((-60+30+(-40/5)*(-9-2*-5/30-7/3*99/4*2998+10/-568/14))-(-4*-3)/(16-3*2))+3"
    a = zhu(gongshi)
# 1 - 2 * ( (60-30 +(-40.0/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )

