#!/usr/bin/env bash

############################################################
# Effect : physics backup
# OS environment: For Ubuntu 14.04 LTS Trusty and above
#
# author: zhihao
# creat_time: 2018-5-25
# modify time:
############################################################

help(){
       cat << EOF
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
EOF
}


while test $# -gt 0
do
    case $1 in
        --base)
        backup_status='base'
        shift
        ;;
        --inc)
        backup_status='inc'
        shift
        ;;
        --full)
        backup_status='full'
        shift
        ;;
        -P)
        port=$2
        shift
        ;;
        -d)
        source_data_dir=$2
        shift
        ;;
        -D)
        databases=$2
        shift
        ;;
        -src_ip)
        src_ip=$2
        shift
        ;;
        -dest_ip)
        dest_ip=$2
        shift
        ;;
        -dest_dir)
        dest_dir=$2
        shift
        ;;
        --help)
        help
        exit 0
        ;;
        *)
        echo >&2 "Invalid argument: $1"
        exit 0
        ;;
    esac
     shift
done

admin_user='tfadmin'
admin_pwd='tfkj_secret'

log='/auto_op_stuff/galera_mysqlha/physics_backup.log'


function mk_log()
{
    touch $log

    if [ -f $log ]; then
        echo -e "step.1 ====> $log make \033[32m succ \033[0m \n"
        echo "step.1 ====> $log make succ" >> $log
    else
        echo -e "step.1 ====> $log make \033[31m fail \033[0m \n"
        echo "step.1 ====> $log make fail" >> $log
        exit 0
    fi
}

function print_date()
{
    echo '-------------------'`date`'---------------------' >> $log
}


function backup()
{
    date_time=`date "+%Y_%m_%d-%H_%M_%S"`
    
    if [ $src_ip == '' ]; then
        ip_source=`ifconfig eth0 | grep 'inet addr' | sed 's/^.*addr://g' |sed 's/  Bcast:.*$//g'`
    else
       ip_source=$src_ip
    fi
    
    #backup_log=`/usr/bin/innobackupex --defaults-file=$source_data_dir/mysql$port/my"$port"_galera.cnf --user=$admin_user --password=$admin_pwd --slave-info --databases=$databases --stream=tar $dest_dir | gzip | sshpass -pP@ssw0rd ssh -p 22 root@$dest_ip "cat > $dest_dir/\"$ip_source\"_\"$port\"_\"$date_time\".tar.gz"`
    backup_log=`/usr/bin/innobackupex --defaults-file=$source_data_dir/mysql$port/my"$port"_galera.cnf --kill-long-queries-timeout=10 --user=$admin_user --password=$admin_pwd --parallel=3 --stream=tar $dest_dir | gzip | sshpass -pP@ssw0rd ssh -p 22 root@$dest_ip "cat > $dest_dir/\"$ip_source\"_\"$port\"_\"$date_time\".tar.gz"`

    echo -e "step.2 ====> physics backup \033[32m succ \033[0m \n"
    echo "step.2 ====> physics backup succ" >> $log

}

function backup_inc_base()
{
    date_time=`date "+%Y_%m_%d-%H_%M_%S"`
    date_day=`date "+%Y_%m_%d"`

    mkdir -p $dest_dir/inc_base/$port

    base_backup_log=`/usr/bin/innobackupex --defaults-file=$source_data_dir/mysql$port/my"$port"_galera.cnf --kill-long-queries-timeout=10 --user=$admin_user --password=$admin_pwd --parallel=3 $dest_dir/inc_base/$port`

    base_backup_name=`ls -l $dest_dir/inc_base/$port |awk '/^d/ {print $NF}'| tail -1`

    cd $dest_dir/inc_base/$port && tar zcvf ./"$base_backup_name".tar.gz  ./$base_backup_name

    sshpass -pP@ssw0rd ssh -p 22 root@$dest_ip "( mkdir -p $dest_dir/inc/$port/$date_day/inc_base )"

    sshpass -pP@ssw0rd scp $dest_dir/inc_base/$port/"$base_backup_name".tar.gz root@$dest_ip:$dest_dir/inc/$port/$date_day/inc_base
}

function purge_old_backup_inc_base()
{
    base_backup_name=`ls -l $dest_dir/inc_base/$port |awk '/^d/ {print $NF}'| tail -1`

    purge_dir=`ls -l $dest_dir/inc_base/$port |awk '/^d/ {print $NF}' | grep -v $base_backup_name | xargs`

    cd $dest_dir/inc_base/$port && rm -rf $purge_dir
    cd $dest_dir/inc_base/$port && rm -rf ./*.tar.gz
}

function backup_inc()
{
    date_time=`date "+%Y_%m_%d-%H_%M_%S"`
    date_day=`date "+%Y_%m_%d"`

    base_backup_name=`ls -l $dest_dir/inc_base/$port |awk '/^d/ {print $NF}'| tail -1`

    inc_backup_log=`/usr/bin/innobackupex --defaults-file=$source_data_dir/mysql$port/my"$port"_galera.cnf --kill-long-queries-timeout=10 --user=$admin_user --password=$admin_pwd --parallel=3 --incremental-basedir=$dest_dir/inc_base/$port/$base_backup_name --incremental --stream=xbstream $dest_dir | sshpass -pP@ssw0rd ssh -p 22 root@$dest_ip "mkdir -p $dest_dir/inc/$port/$date_day/$date_time && xbstream -x -C $dest_dir/inc/$port/$date_day/$date_time"`
}


function main()
{
    print_date
    mk_log

    if [ $backup_status == 'full' ]; then
        backup
    fi

    if [ $backup_status == 'base' ]; then
        #purge_old_backup_inc_base
        backup_inc_base
        purge_old_backup_inc_base
        
    fi

    if [ $backup_status == 'inc' ]; then
        backup_inc
    fi
}

main

##./yyyy.sh -P 4444 -src_ip 192.168.0.87 -d /data1 -dest_ip 10.20.4.138 -dest_dir /backup --full

#./yyyy.sh -P 4444 -d /data1 -dest_ip 10.20.4.138 -dest_dir /backup --base
#./yyyy.sh -P 4444 -d /data1 -dest_ip 10.20.4.138 -dest_dir /backup --inc
