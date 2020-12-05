# galera-mysql5.7 部署

> #### mysqlwsrepha_init_service.py　初始化wsrepmysql服务器
```
chmod +x ./mysqlwsrepha_init_service.py && ./mysqlwsrepha_init_service.py
```

> #### mysqlwsrepha_init_instance.py 初始化wsrepmysql实例

```
usage: mysqlwsrepha_init_instance.py [-h] [--first] [--notfirst]
                                     [--donor DONOR] [-P P] [-d D]
optional arguments:
  -h, --help     show this help message and exit
  --first        modify instance to first node of cluster
  --notfirst     modify instance to joiner node of cluster
  --donor DONOR  the node ip have in cluster, eg
                 :10.10.4.111,10.20.4.112
  -P P           port of instance
  -d D           data directory of instance, eg: /data1
```
>> 初始化集群中的第一个实例：
```
chmod +x ./mysqlwsrepha_init_service.py && ./mysqlwsrepha_init_service.py -P [port] -d [datadir] --first
```
>>初始化集群中的第2至第n个实例：
```
chmod +x ./mysqlwsrepha_init_service.py && ./mysqlwsrepha_init_service.py -P [port] -d [datadir] --donor [ip1] --notfirst
```


> #### mysqlwsrepha_start.py 启动实例
```
usage: mysqlwsrepha_start.py [-h] [--init] [-P P] [-d D]
optional arguments:
  -h, --help  show this help message and exit
  --init      first time to start this instance
  -P P        port of instance
  -d D        data directory of instance, eg: /data1
```
>> 初始化实例：

```
chmod +x ./mysqlwsrepha_start.py && ./mysqlwsrepha_start.py -P [port] --init
```
>>正常启动已经初始化后的实例：
```

chmod +x ./mysqlwsrepha_start.py && ./mysqlwsrepha_start.py -P [port] 
```


> #### mysqlwsrepha_stop.py 关闭实例,会提示是否真的要关闭实例，如果真的要关闭，输入yes后关闭
```
chmod +x ./mysqlwsrepha_stop.py && ./mysqlwsrepha_stop.py -P [port]
```

> #### mysqlwsrepha_login.py 登录实例
```
chmod +x ./mysqlwsrepha_login.py && ./mysqlwsrepha_login.py -P [port]
```

> #### 寻找宕机节点的最后复制位置点

```
Usage:
Options:
    -P  port of instance
    -d  data directory of instance, eg: /data1

    --getpost     get seqno
```
>> 寻找位置点
```
./recover_node.sh -P xxxx -d /data1 --getpost
```

