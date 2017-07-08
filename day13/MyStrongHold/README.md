### (1)作业名称：堡垒机


### (2)作者：赵晋彪


### (3)博客地址：
   <http://www.cnblogs.com/breakering/p/7128221.html>


### (4)作业需求：

* 所有的用户操作日志要保留在数据库中
* 每个用户登录堡垒机后，只需要选择具体要访问的设置，就连接上了，不需要再输入目标机器的访问密码
* 允许用户对不同的目标设备有不同的访问权限，例:
    * 对10.0.2.34 有mysql 用户的权限
    * 对192.168.3.22 有root用户的权限
    * 对172.33.24.55 没任何权限
* 分组管理，即可以对设置进行分组，允许用户访问某组机器，但对组里的不同机器依然有不同的访问权限


### (5)本次作业实现的需求：

1. 用户操作日志均保留在数据库中
2. 用户登陆堡垒机之后，可以选择已经分组的主机或者未分组的主机，然后选择主机编号直接连接主机
3. 每个用户对不同的主机的访问权限均不相同
4. 具备分组功能


### (6)测试：
1) 运行测试环境： Linux Centos6.4 x64, 先安装必备环境pip3 install -r requirements.txt
2) 编辑.bashrc 文件, 使用户进入系统后直接运行堡垒机程序 并且无法退出
   vim .bashrc
   # .bashrc
   python3 /root/Breakering/PythonStudy/day13/start_mystronghold.py
   logout
3) conf/settings.py 文件设置数据库信息
4) 根据resources/tables模板文件创建数据库数据
5) 管理员运行/bin/init_system.py可初始化数据库和表格
6) 运行/bin/start_mystronghold.py即可使用堡垒机

堡垒机测试账号：
1. 用户名:breakering 密码:123
2. 用户名:profhua 密码:456
3. 用户名:wolf 密码:789


### (7)备注：
初始化数据库会清空日志，注意备份,
windows未做日志处理，请在linux下使用,
ssh公钥认证未处理.