### (1)作业名称：RbbitMQ之RPC

### (2)作者：赵晋彪

### (3)博客地址：
   <http://www.cnblogs.com/breakering/p/7041215.html>

### (4)作业需求：

可以对指定机器异步的执行多个命令
例子：
* run "df -h" --hosts 192.168.3.55 10.4.3.4
* task id: 45334
* check_task 45334
注意，每执行一条命令，即立刻生成一个任务ID,不需等待结果返回，通过命令check_task TASK_ID来得到任务结果



### (5)本次作业实现的需求：

1. 执行命令无需等待，且可以对多台机器执行命令，执行一条命令即生成一个任务ID；
2. 通过任务ID获取任务结果，同一个任务ID可对应多台机器；
3. 可以通过task_info获取已经生成的任务ID，及对应的命令内容和主机地址

### (6)测试：

* 到RPC_Server的bin目录下启动start_rpc_server.py，即可启动一个服务器，将start_rpc_server.py
中实例化的参数改为"server2",即模拟启动了第二台服务器，RabbitMQ地址在RPC_Server的conf下的settings
文件中修改;
* 到RPC_Client下启动rpc_client.py，即可启动客户端，rpc_client.py中变量RABBITMQ_IP可以修改RabbitMQ地址，
host_to_queue变量为主机地址对应RPC队列，此种设计可以很方便的为主机起名字,也就是可以通过主机名字来执行命令




### (7)备注：
任务ID对应的任务结果存在服务器端，也就是服务器端不关闭，任务结果永远存在，后期可以考虑设计从
客户端删除任务结果及任务ID，或者考虑将任务结果存入数据库，方便以后进行排查