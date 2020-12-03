#!/usr/bin/env bash

############################################################
# Effect : recover failure node
# OS environment: For Ubuntu 14.04 LTS Trusty and above
#
# author: zhihao
# creat_time: 2018-7-25
# modify time:
############################################################

help(){
       cat << EOF
Usage:
Options:
    -P  port of instance
    -d  data directory of instance, eg: /data1

    --getpost     get seqno 
EOF
}

while test $# -gt 0
do
    case $1 in
        --getpost)
        status='getpost'
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


function get_fail_node_seqno()
{
    date_time=`date "+%Y%m%d%H%M%S"`

    touch $source_data_dir/mysql$port/wsrep_recovery.$date_time
    chown my$port.mysql $source_data_dir/mysql$port/wsrep_recovery.$date_time

    /usr/sbin/mysqld --defaults-file=$source_data_dir/mysql$port/my"$port"_galera.cnf --log_error="$source_data_dir/mysql$port/wsrep_recovery.$date_time" --pid-file="$source_data_dir/mysql$port/mysql$port.pid" --wsrep_recover

    seqno_num=`grep 'Recovered position' $source_data_dir/mysql$port/wsrep_recovery.$date_time | awk -F ':' '{print $NF}'`
    uuid_num=`grep 'Recovered position' $source_data_dir/mysql$port/wsrep_recovery.$date_time | awk -F ':' '{print $(NF-1)}'`

    echo "uuid: $uuid_num"
    echo "seqno_num: $seqno_num"
}

function main()
{
    if [ $status == 'getpost' ]; then
        get_fail_node_seqno
    fi

}


main

#./recover_node.sh -P 4444 -d /data1 --getpost
