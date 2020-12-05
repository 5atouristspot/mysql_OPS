#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
@author: devin
@used: stop instances of mysql-wsrep-5.7.20
"""
import argparse
import time
import json
import os
import getpass
import sys
reload(sys)

log = '/auto_op_stuff/galera_mysqlha/mysqlha.log'

admin_user = 'xxxx'
admin_pwd = 'yyyy'


def write_log(log,log_content):
    os.system('mkdir -p /auto_op_stuff/galera_mysqlha')
    with open(log, 'a+') as log_handle:
        log_handle.write("[{now_time}][{user}]{log_content}\n".format(user=getpass.getuser(), now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
                                         log_content=log_content))



def is_dir_exist_stat(dir_name):
    stat = os.path.exists(dir_name)
    if stat is False:
        status = {"action": "{dir_name} is not exist".format(dir_name=dir_name), "status": "FAIL"}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)


#return True or False
def is_exist_instance(port, data_dir):
    stat = os.popen("ps -ef | grep '/usr/sbin/mysqld --defaults-file={data_dir}/mysql{port}/my{port}_galera.cnf' | grep -v grep | wc -l".format(port=port, data_dir=data_dir)).readlines()[0].split('\n')[0]
    if stat == '1':
        return True
    else:
        return False


#if 0 :not exist ,else exist
def is_master(file_name, modify_content):
    stat = os.popen("grep '{modify_content}' {file_name} | wc -l".format(file_name=file_name, modify_content=modify_content)).readlines()[0].split('\n')[0]

    if stat == '1':
        return True
    else:
        return False


def get_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', type=str, help="port of instance", default='3306')
    parser.add_argument('-d', type=str, help="data directory of instance, eg: /data1", default='/data1')

    args = parser.parse_args()

    return args


def shutdown_instance(admin_user, admin_pwd, port, data_dir):
    is_dir_exist_stat("{data_dir}/mysql{port}".format(port=port, data_dir=data_dir))
    if is_exist_instance(port, data_dir):
        os.system("/usr/bin/mysqladmin -u{admin_user} -p{admin_pwd} -S {data_dir}/mysql{port}/mysql{port}.sock shutdown".format(port=port, data_dir=data_dir, admin_user=admin_user, admin_pwd=admin_pwd))
        status = {"action": "instance {port} stop".format(port=port), "status": "OK"}
        print json.dumps(status)
        write_log(log, status)
    else:
        status = {"action": "instance {port} have stoped, could not stop again".format(port=port), "status": "FAIL"}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)


def stop_instance(admin_user, admin_pwd, port, data_dir):
    file_name = "{data_dir}/mysql{port}/my{port}_galera.cnf".format(port=port, data_dir=data_dir)
    modify_content = "read_only = 0"

    if is_master(file_name, modify_content):
        to_stop = raw_input("this instance is \033[1;33;44m MASTER \033[0m!,do you really want to stop it ?! (yes/no):")
        if to_stop == 'yes':
            shutdown_instance(admin_user, admin_pwd, port, data_dir)
        else:
            status = {"action": " instance {port} stop".format(port=port), "status": "FAIL"}
            print "\033[1;35m  instance {port} not stop \033[0m!".format(port=port)
            write_log(log, status)
            sys.exit(0)
    else:
        shutdown_instance(admin_user, admin_pwd, port, data_dir)



def main():
    arg = get_arg()

    stop_instance(admin_user, admin_pwd, arg.P, arg.d)


if __name__ == '__main__':
    main()
