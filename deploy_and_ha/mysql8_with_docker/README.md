# 主库
> #### 导入镜像　数据文件　及　配置文件
```
mkdir -p /docker/mysql8

cp my3308.cnf /docker/mysql8/

cp -Rf mysql3308 /docker/mysql8/

docker load < /mysql_OPS/deploy_and_ha/mysql8_with_docker/docker_images/mysql8.tar
```
>> 修改　auto.cnf　,　配置文件的server_id , 查看修改是否正常
```
show variables like '%server%'
```
>#### 启动实例
```
docker run -d -p 3308:3308 -v /docker/mysql8/mysql3308:/var/lib/mysql -v /docker/mysql8/my3308.cnf:/etc/my.cnf -e MYSQL_ROOT_PASSWORD=my-secret-pw -t cytopia/mysql-8.0
```
> #### 登陆实例
```
docker exec -it 9747415841a3 bash
mysql -uroot -pmy-secret-pw -h127.0.0.1 -P3308
```
> #### 主库查看 半同步复制状态：
```
show status like '%Rpl_semi_sync_master_status%';
```
> #### 主库启用半同步复制：
```
set global rpl_semi_sync_master_enabled = 1; 
```

# 从库
> #### 导入镜像　数据文件　及　配置文件
```
mkdir -p /docker/mysql8

cp my3308.cnf /docker/mysql8/

cp -Rf mysql3308 /docker/mysql8/

docker load < /mysql_OPS/deploy_and_ha/mysql8_with_docker/docker_images/mysql8.tar
```
>> 修改　auto.cnf　,　配置文件的server_id , 查看修改是否正常
```
show variables like '%server%'
```
>#### 启动实例
```
docker run -d -p 3308:3308 -v /docker/mysql8/mysql3308:/var/lib/mysql -v /docker/mysql8/my3308.cnf:/etc/my.cnf -e MYSQL_ROOT_PASSWORD=my-secret-pw -t cytopia/mysql-8.0
```
> #### 登陆实例
```
docker exec -it 9747415841a3 bash
mysql -uroot -pmy-secret-pw -h127.0.0.1 -P3308
```

>#### 搭建主从
>>主库创建复制用户
```
CREATE USER repl@'10.99.153.%' IDENTIFIED BY 'repl@master';
GRANT FILE,REPLICATION SLAVE ON *.* TO repl@'xx.xx.xxx.%' WITH GRANT OPTION;
```
>>从库change master 
```
CHANGE MASTER TO MASTER_HOST='xx.xx.xxx.xx', MASTER_PORT=3308,MASTER_AUTO_POSITION=1,MASTER_USER='repl',MASTER_PASSWORD='repl@master';
```
>>启动主从
```
start slave ;
```

> #### 从库查看 半同步复制状态：
```
show status like '%Rpl_semi_sync_slave_status%';
```

> #### 从库启用半同步复制：
```
set global rpl_semi_sync_slave_enabled = 1; 
stop slave;
sleep 2;
start slave;
```
