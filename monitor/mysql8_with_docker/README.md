# mysql8 半同步复制　主从监控
>#### 监控server端
>>导入镜像
```
docker load < /mysql_OPS/deploy_and_ha/mysql8_with_docker/docker_images/grafana.tar
docker load < /mysql_OPS/deploy_and_ha/mysql8_with_docker/docker_images/prometheus.tar
docker load < /mysql_OPS/deploy_and_ha/mysql8_with_docker/docker_images/pushgateway.tar

```
>>监控机创建网络环境
```
docker network create mysql-monitor
```
>>上传docker-compose 到监控机server
```
cp /mysql_OPS/monitor/mysql8_with_docker/docker-compose /usr/local/bin/ && chmod +x /usr/local/bin/docker-compose
```

>>删除grafana 文件夹下数据

```
rm -rf Grafana/*
```
>> 启动监控
```
docker-compose -f ./docker-compose.yaml -p mysql-monitor up -d
```
>> 停止监控
```
docker-compose -f ./docker-compose.yaml -p mysql-monitor down
```

>#### 监控client端
>>导入镜像
```
docker load < /mysql_OPS/deploy_and_ha/mysql8_with_docker/docker_images/mysqld-exporter.tar
```
>>监控clinet执行
```
docker run -d --restart=always  --name mysql-exporter-dev -p 9104:9104   -e DATA_SOURCE_NAME="root:my-secret-pw@(xx.xx.xxx.xx:3308)/"   prom/mysqld-exporter
docker run -d --restart=always  --name mysql-exporter-dev -p 9104:9104   -e DATA_SOURCE_NAME="root:my-secret-pw@(yy.yy.yyy.yy:3308)/"   prom/mysqld-exporter
```

