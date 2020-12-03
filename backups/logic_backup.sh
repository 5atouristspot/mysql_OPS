#!/usr/bin/env bash

############################################################
# Effect : logic backup
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
EOF
}


while test $# -gt 0
do
    case $1 in
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


log='/auto_op_stuff/galera_mysqlha/logic_backup.log'

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
    date_time=`date "+%Y_%m_%d-%H:%M:%S"`
    ip_source=`ifconfig eth0 | grep 'inet addr' | sed 's/^.*addr://g' |sed 's/  Bcast:.*$//g'`

    backup_log=`mysqldump -u$admin_user -p$admin_pwd -S $source_data_dir/mysql$port/mysql$port.sock $databases | gzip | sshpass -pP@ssw0rd ssh -p 22 root@$dest_ip "cat > $dest_dir/\"$ip_source\"_\"$port\"_\"$date_time\".sql.gz"`

    echo -e "step.2 ====> logic backup \033[32m succ \033[0m \n"
    echo "step.2 ====> logic backup succ" >> $log

}



function main()
{
    print_date
    mk_log

    backup
}

main


#./xxx.sh -P 4444 -d /data1 -D zhihao -dest_ip 10.20.4.138 -dest_dir /backup
