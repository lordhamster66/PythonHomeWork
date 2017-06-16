(1)作业名称：修改haproxy配置文件
(2)作者：赵晋彪
(3)博客地址：http://www.cnblogs.com/breakering/p/6684414.html
(4)作业需求：
        1. 根据用户输入输出对应的backend下的server信息
        2. 可添加backend 和sever信息
        3. 可修改backend 和sever信息
        4. 可删除backend 和sever信息
        5. 操作配置文件前进行备份
        6 添加server信息时，如果ip已经存在则修改;如果backend不存在则创建；若信息与已有信息重复则不操作
        配置文件 参考 http://www.cnblogs.com/alex3714/articles/5717620.html

(5)本次作业实现的需求：
        1.可查询对应backend下的信息，输入有误会提示重新输入；
        2.可添加backend和server信息，backend存在则判断server,server存在且信息相同则不修改，否则修改，backend不存在则创建；
        3.添加修改功能一起实现，原则：存在且信息相同不修改，存在信息不相同则修改，不存在则创建；
        4.删除server信息时只会删除对应backend下的server信息，其他backend下相同的server信息不会删除，server信息有误不会删除；
        5.每次增加，删除和修改都会进行备份，备份文件名字末尾会追加时间信息，统一存放在copy_file文件夹内；
        6.在2，3中已经实现。

(6)测试：
        运行conf_haproxy.py进入程序主界面，
        查询可输入：www.oldboy.org，www.oldboy.com，www.oldboy.cn测试
        新建添加可输入：{"backend": "www.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 3000}}
                        {"backend": "www.oldboy.com","record":{"server": "100.1.7.9","weight": 20,"maxconn": 3000}}
                        {"backend": "www.oldboy.cn","record":{"server": "100.1.7.9","weight": 20,"maxconn": 3000}}
        删除可输入：    {"backend": "www.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 3000}}
                        {"backend": "www.oldboy.com","record":{"server": "100.1.7.9","weight": 20,"maxconn": 3000}}
                        {"backend": "www.oldboy.cn","record":{"server": "100.1.7.9","weight": 20,"maxconn": 3000}}
        每次操作都有提醒功能

(7)备注：只能在当前路径下运行代码，rule.txt是一些输入规范提示,如果backend下只有一条信息，那么在删除这条信息后，该backend
        也会被删除