(1)作业名称：员工信息表修改程序
(2)作者：赵晋彪
(3)博客地址：http://www.cnblogs.com/breakering/p/6718049.html
(4)作业需求：
        1.可进行模糊查询，语法至少支持下面3种:
        　　select name,age from staff_table where age > 22
        　　select  * from staff_table where dept = "IT"
            select  * from staff_table where enroll_date like "2013"
            查到的信息，打印后，最后面还要显示查到的条数
        2.可创建新员工纪录，以phone做唯一键，staff_id需自增
        3.可删除指定员工信息纪录，输入员工id，即可删除
        4.可修改员工信息，语法如下:
        　　UPDATE staff_table SET dept="Market" WHERE where dept = "IT"
         注意：以上需求，要充分使用函数，请尽你的最大限度来减少重复代码

(5)本次作业实现的需求：
        1.三种语法均支持，并且可以写and条件，例如：select name,age,dept from staff_table where age > 22 and dept = "HR"；
        查询的条数在下方会有显示；
        2.可以创建新的员工记录，语法：insert into staff_table (name,age,phone,dept,enroll_date) values (Breakering,23,18006812784,IT,2017-04-15)；
        3.输入员工ID，即可删除记录；
        4.支持题目要求update语法

(6)测试：运行like_sql.py即可执行程序，like语法只能单独使用
        1.查询：
               select name,age from staff_table where age > 22
               select name,age from staff_table where age < 40
               select name,age,dept from staff_table where age > 22 and dept = "HR"
               select * from staff_table where staff_id > 0
               select * from staff_table where age > 22 or staff_id > 0
               select  * from staff_table where dept = "IT"
               select  * from staff_table where enroll_date like "2013"

        2.创建：
               insert into staff_table (name,age,phone,dept,enroll_date) values (Breakering,23,18006812784,IT,2017-04-15)

        3.删除：
                4
                5

        4.修改：
                UPDATE staff_table SET dept="Market" WHERE dept = "IT"

(7)备注：select * from staff_table 没实现，可以用select * from staff_table where staff_id > 0代替，
         like语法只能单独使用，创建、删除和修改语法只支持一种，而且没有语法检测功能，只能适应一个staff_table表格。
         原因：一开始框架设计不够合理，逻辑不够清晰
