#!/usr/bin/env bash

############################################################
# Effect : drop physics backup file
# OS environment: For Ubuntu 14.04 LTS Trusty and above
#
# author: devin
# modify time:
############################################################

help(){
       cat << EOF
Usage:
Options:
    -P  port of instance
    -t  restore how many days
    -d  dest dir of backup file, eg: /backup

    --full    full backup
    --inc     inc backup
EOF
}

while test $# -gt 0
do
    case $1 in
        --inc)
        drop_backup_status='inc'
        shift
        ;;
        --full)
        drop_backup_status='full'
        shift
        ;;
        -P)
        port=$2
        shift
        ;;
        -d)
        dest_dir=$2
        shift
        ;;
        -t)
        restore_days=$2
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

log='/auto_op_stuff/galera_mysqlha/drop_physics_backup.log'

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


function drop_inc_backup_file()
{
    all_days=`ls -tl $dest_dir/inc/$port | wc -l`

    drop_days=`expr $all_days - $restore_days - 1`

    if [[ $drop_days -gt 0 ]]; then
        drop_file_name=`ls -tl $dest_dir/inc/$port |awk '/^d/ {print $NF}' | tail -n $drop_days | xargs`

        echo "step.2 ====> drop inc backup:" $port $drop_file_name >> $log 
        echo "step.2 ====> drop inc backup:" $port $drop_file_name
    
        cd $dest_dir/inc/$port && rm -rf $drop_file_name
    fi
}

function drop_full_backup_file()
{
    
    all_days=`ls -tl $dest_dir | grep $port | grep tar | grep -v grep | wc -l`

    drop_days=`expr $all_days - $restore_days`

    if [[ $drop_days -gt 0 ]]; then
        drop_file_name=`ls -tl $dest_dir | grep $port | grep -v grep |awk '{print $NF}' | tail -n $drop_days | xargs`

        echo "step.2 ====> drop full backup:" $port $drop_file_name >> $log 
        echo "step.2 ====> drop full backup:" $port $drop_file_name
    
        cd $dest_dir && rm -rf $drop_file_name
    fi
}


function main()
{
    print_date
    mk_log

    if [ $drop_backup_status == 'full' ]; then
        drop_full_backup_file
    fi

    if [ $drop_backup_status == 'inc' ]; then
        drop_inc_backup_file
    fi
}

main

#./yyy.sh -P 4444 -d /backup -t 7 --inc
#./yyy.sh -P 4444 -d /backup -t 7 --full

