### (1)作业名称：SELECT版FTP

### (2)作者：赵晋彪

### (3)博客地址：
   <http://www.cnblogs.com/breakering/p/6979559.html>
   <http://www.cnblogs.com/breakering/p/6979584.html>

### (4)作业需求：

1. 使用SELECT或SELECTORS模块实现并发简单版FTP
2. 允许多用户并发上传下载文件


### (5)本次作业实现的需求：

1. 使用SELECT或SELECTORS模块实现并发简单版FTP
   1. 使用了SELECTORS模块实现
2. 允许多用户并发上传下载文件
   2. 不同用户可以同时登陆，同时上传文件至家目录，同时从家目录下载文件，上传
   下载均有进度条提示

### (6)测试：
**测试账号：**
1. 用户名:Breakering 密码:123
2. 用户名:profhua 密码:123

* 到SelectFTPServer的bin目录下启动start_ftp_server.py，即可启动服务端，
到SelectFTPClient下启动select_ftp_client.py，即可启动客户端，可启动多个客户端
* 注：
    * 上传文件需要文件绝对路径  eg: put D:\mylog.log
    * 下载文件只能下载用户家目录下文件只需写上文件名即可
    eg: get realtek_wlan_0630_64_1111.exe



### (7)备注：
windows测试没有问题，不支持断点续传及磁盘配额等操作