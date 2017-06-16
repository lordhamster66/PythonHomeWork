#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
import sys,os,time
def analysis(input_sql):
    '''
    解析函数，用来解析用户输入的sql语句
    :param input_sql: 用户输入的sql语句
    :return:
    '''
    # insert into staff_table (name,age,phone,dept,enroll_date) values (Breakering,23,18006812784,IT,2017-04-15)
    if input_sql.startswith("insert"):
        try:
            table = input_sql[input_sql.index("o") + 1:input_sql.index("(")].strip()  # 解析创建语句的表格
            rules = input_sql[input_sql.index("(") + 1:input_sql.index(")")].strip()  # 解析创建语句对应的相关信息
            info = input_sql[input_sql.rfind("(") + 1:input_sql.rfind(")")].strip()  # 解析创建语句的创建信息
            return myinsert(table, rules, info)
        except Exception as e:
            print(e)
            return
    #UPDATE staff_table SET dept="Market" WHERE dept = "IT"
    if input_sql.startswith("update") or input_sql.startswith("UPDATE"):
        input_sql = input_sql.replace("UPDATE", "update")
        input_sql = input_sql.replace("SET", "set")
        input_sql = input_sql.replace("WHERE", "where")
        try:
            table = input_sql.replace("update","").split("set")[0].strip()             #解析修改语句所修改的表格
            info = input_sql.split("set")[1].split("where")[0].strip()                 #解析修改语句要修改的信息
            condition = input_sql.split("where")[1].strip()                            #解析修改语句的修改条件
            return myupdate(table,info,condition)
        except Exception as e:
            print(e)
            return

    input_sql = input_sql.lower()
    #select name,age from staff_table where age > 22
    if input_sql.startswith("select"):
        try:
            info = input_sql.replace("select","").strip().split("from")[0].strip()    #解析查询语句的查询信息
            table = input_sql.split("from")[1].split("where")[0].strip()              #解析查询语句的查询表格
            condition = input_sql.split("where")[1].strip()                           #解析查询语句的查询条件
            return myselect(info,table,condition)
        except Exception as e:
            print(e)
            return
    #4
    if input_sql.isdigit():
        index = int(input_sql)                                                     #删除只用输入员工id
        return mydelete(index)
    else:
        print("\033[31;1m您的输入有误，请检查后再输入！\033[0m")
        return

def copy_file():
    '''
    备份函数
    :return: 无返回值
    '''
    date = time.strftime('%Y%m%d%H%M%S')
    copy_file_name = "staff_table-%s"%date
    with open("staff_table","r",encoding="utf-8") as f1 \
        ,open(os.path.join("table_copy",copy_file_name),"w", encoding="utf-8") as f2:
        for line in f1:
            f2.write(line)
    print("表格%s备份完毕"%copy_file_name)
    time.sleep(1)

def progress_bar():
    '''
    进度条显示
    :return:
    '''
    for i in range(10):
        sys.stdout.write("=")
        sys.stdout.flush()
        time.sleep(0.1)

def condition_change(condition):
    '''
    用户输入条件修改函数，目的使程序能够识别此条件
    :param condition: 用户输入的条件
    :return: 返回修改后的条件
    '''
    if "=" in condition:                                   #如果条件里面有=，则改为==，这样eval就可以解析了
        condition = condition.replace("=", "==")
    if "like" in condition:                                #将like改为in成员测试写法
        key,value = condition.split("like")
        condition = "%s in %s"%(value.strip(),key.strip())
    return condition

def myselect(info,table,condition):
    '''
    查询函数
    :param info: 要查询的信息
    :param table: 要查询的表
    :param condition: 要查询的条件
    :return:
    '''
    table_title = ["staff_id","name","age","phone","dept","enroll_date"]
    if info == "*":                                        #如果是查询所有信息则打印所有表头
        print("%-10s %-10s %-5s %-15s %-10s %-10s"%
            (table_title[0],table_title[1],table_title[2],table_title[3],table_title[4],table_title[5]))
        print("".center(65, "-"))
    if info != "*":
        info_list = info.split(",")
        info_check = []
        for i in info_list:                                #测试查询信息是否都在表头里面
            if i in table_title:info_check.append(1)
            else:info_check.append(0)
        if all(info_check):
            for index,ziduan in enumerate(info_list):
                if index < len(info_list)-1:print(ziduan,end="".center(15," "))
                else:print(ziduan)
            print("".center(65, "-"))
        else:
            print("\033[31;1m请检查你所查询的信息\033[0m")
            return
    condition = condition_change(condition)                #将用户输入的条件变为此程序可识别的条件
    with open(table,"r",encoding="utf-8") as f:
        count = 0                                          #记录查到的个数
        for line in f:
            l = line.strip().split(",")
            #将每行各个位置的值取上对应的名称
            staff_id,name,age,phone,dept,enroll_date = \
            int(l[0]),l[1].lower(),int(l[2]),int(l[3]),l[4].lower(),l[5]
            # l = staff_id,name,age,phone,dept,enroll_date
            if info == "*":
                if eval(condition):
                    count += 1                              #每查到一次个数加1
                    print("%-10s %-10s %-5s %-15s %-10s %-10s"%(int(l[0]),l[1],int(l[2]),int(l[3]),l[4],l[5]))
            elif info != "*":
                if eval(condition):
                    count += 1                              #每查到一次个数加1
                    for index,i in enumerate(info_list):
                        if index < len(info_list)-1:print("%s"%l[table_title.index(i)],end="".center(15," "))
                        else:print("%s"%l[table_title.index(i)])
        print("".center(65, "-"))
        print("".center(52," "),"\033[31;1m共计条数：%s\033[0m"%count)

def myinsert(table,rules,info):
    '''
    创建函数
    :param table: 表名
    :param rules: 字段
    :param info: 字段对应信息
    :return:
    '''
    str_ziduan = ["name","age","phone","dept","enroll_date"]     #字段对照表
    value = [None,None,None,None,None]                           #字段对应值填写表
    rules_list = rules.split(",")                                #用户输入字段
    info_list = info.split(",")                                  #用户输入字段所对应信息
    for index,i in enumerate(rules_list):
        if i == str_ziduan[str_ziduan.index(i)]:
            value[str_ziduan.index(i)] = info_list[index]        #将用户输入信息填入字段对应值里
    with open(table,"r+",encoding="utf-8") as f:
        index_list = []                                          #用来临时存储staff_id
        for line in f:
            l = line.strip().split(",")
            index_list.append(int(l[0]))
        progress_bar()
        f.write("\n%s,%s,%s,%s,%s,%s"%(index_list[-1]+1,value[0],value[1],value[2],value[3],value[4]))
        print("\033[31;1m信息添加成功！\033[0m")

def mydelete(index):
    '''
    删除函数
    :param index: 要删除的staff_id
    :return: 无返回值
    '''
    del_flag = False
    staff_id_list = []
    with open("staff_table","r",encoding="utf-8") as f:
        for line in f:
            l = line.strip().split(",")
            staff_id_list.append(l[0])
    with open("staff_table","r",encoding="utf-8") as f,\
         open("staff_table.new","w",encoding="utf-8") as f2:
        for line in f:
            l = line.strip().split(",")
            if index == int(staff_id_list[-1]) and l[0] == staff_id_list[-2]:f2.write(line.strip())
            elif int(l[0]) == int(index):
                del_flag = True
                continue
            elif l[0] == staff_id_list[-1]:f2.write(line.strip())
            else:f2.write(line)
    if del_flag:
        copy_file()
        os.remove("staff_table")
        os.rename("staff_table.new","staff_table")
        progress_bar()
        print("\033[31;1m记录删除成功！\033[0m")
        return
    else:
        os.remove("staff_table.new")
        print("\033[31;1m要删除的记录并不存在！\033[0m")
        return

def myupdate(table,info,condition):
    '''
    修改函数
    :param table: 表名
    :param info: 要修改的信息
    :param condition: 条件
    :return:
    '''
    ziduan = info.split("=")[0].strip()
    value = info.split("=")[1].strip().replace('"',"")
    table_ziduan = ["staff_id","name","age","phone","dept","enroll_date"]
    condition = condition_change(condition)                #将用户输入的条件变为此程序可识别的条件
    with open(table,"r",encoding="utf-8") as f,\
         open("%s.new"%table,"w",encoding="utf-8") as f2:
        for line in f:
            l = line.split(",")
            # 将每行各个位置的值取上对应的名称
            staff_id,name,age,phone,dept,enroll_date = int(l[0]),l[1],int(l[2]),int(l[3]),l[4],l[5]
            table_value = [staff_id,name,age,phone,dept,enroll_date]
            if eval(condition):
                table_value[table_ziduan.index(ziduan)] = value
                line = "%s,%s,%s,%s,%s,%s"%\
               (table_value[0],table_value[1],table_value[2],table_value[3],table_value[4],table_value[5])
            f2.write(line)
    copy_file()
    os.remove("staff_table")
    os.rename("staff_table.new", "staff_table")
    progress_bar()
    print("\033[31;1m记录修改成功！\033[0m")
    return

if __name__ == "__main__":                                 #程序开始执行
    input_sql = input("请输入您的SQL语句：").strip()
    analysis(input_sql)
