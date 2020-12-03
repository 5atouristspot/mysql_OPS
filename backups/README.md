# mysql备份相关脚本

#### galera_mysql 


> #### install_xtrabackup.py 安装prcona 工具

```
chmod +x ./install_xtrabackup.py && ./install_xtrabackup.py
```

>#### physics_backup.sh 物理备份
```
Usage:
Options:
    -P  port of instance
    -d  data directory of instance, eg: /data1
    -D  backup databases, eg: mysql sys
    -dest_ip  dest ip of backup file, eg: 127.0.0.1
    -dest_dir  dest dir of backup file, eg: /backup
    --full    full backup
    --base    base backup of inc
    --inc     inc backup
```
>>全量备份：
```
chmod +x ./physics_backup.sh && ./physics_backup.sh -P [port] -d [datadir] -dest_ip [dest ip] -dest_dir [dest datadir] --full
```
>>增量基底备份：
```
chmod +x ./physics_backup.sh && ./physics_backup.sh -P [port] -d [datadir] -dest_ip [dest ip] -dest_dir [dest datadir] --base
```
>>增量备份：
```
chmod +x ./physics_backup.sh && ./physics_backup.sh -P [port] -d [datadir] -dest_ip [dest ip] -dest_dir [dest datadir] --inc
```


>#### physics_restore.py 物理备份还原
>>全量备份还原为集群中的第一个实例：
```
chmod +x ./physics_restore.py && ./physics_restore.py --backupfile xx.xx.x.xx_xxxx_2018_05_25-07_46_56.tar.gz -P xxxx -d /data1 --first
```
>>全量备份还原为集群中的非第一个实例：
```
chmod +x ./physics_restore.py && ./physics_restore.py  --backupfile xx.xx.x.xx_xxxx_2018_05_25-07_46_56.tar.gz --donor xx.xx.x.xx -P 4444 -d /data1 --notfirst
```
>>增量备份还原为集群中的第一个实例：
```
chmod +x ./physics_restore.py && ./physics_restore.py --backupfile 2018-05-30_11-47-17.tar.gz --datetime 2018_05_30 --endtime 2018_05_30-12_06_42 -P xxxx -d /data1 --inc --first
```
>>增量备份还原为集群中的非第一个实例：
```
chmod +x ./physics_restore.py && ./physics_restore.py --backupfile 2018-05-30_11-47-17.tar.gz --datetime 2018_05_30 --endtime 2018_05_30-12_06_42 --donor xx.xx.x.xx -P 4444 -d /data1 --inc --notfirst
```

>#### logic_backup.sh 逻辑备份
```
Usage:
Options:
    -P  port of instance
    -d  data directory of instance, eg: /data1
    -D  backup databases, eg: mysql sys
    -dest_ip  dest ip of backup file, eg: 127.0.0.1
    -dest_dir  dest dir of backup file, eg: /backup
```
>>全量备份：
```
chmod +x ./logic_backup.sh && ./logic_backup.sh -P 4444 -d /data1 -D zhihao -dest_ip xx.xx.x.xx -dest_dir /backup
```

>#### 备份计划任务
> #全量物理备份, 每天夜里 23:05 分执行
```
5 23 * * * cd /auto_op_stuff/galera_mysqlha && nohup ./physics_backup.sh -P xxxx -d /data1 -dest_ip xx.xx.x.xx -dest_dir /backup --full &
```

> #全量物理基底备份, 每天夜里 00:05 分执行
```
5 0 * * * cd /auto_op_stuff/galera_mysqlha && nohup ./physics_backup.sh -P xxxx -d /data1 -dest_ip xx.xx.x.xx -dest_dir /backup --base &
```

> #增量物理备份,每小时的第35分钟执行一次
```
35 */1 * * * cd /auto_op_stuff/galera_mysqlha && nohup ./physics_backup.sh -P xxxx -d /data1 -dest_ip xx.xx.x.xx -dest_dir /backup --inc &
```

> #### 写入crontab,重启生效
```
crontab -e
service cron restart
```
