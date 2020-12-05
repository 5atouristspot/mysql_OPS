#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
@author: devin
@used: login instances of mysql 5.7.20
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


#return True or False
def is_exist_instance(port, data_dir):
    stat = os.popen("ps -ef | grep '/usr/sbin/mysqld --defaults-file={data_dir}/mysql{port}/my{port}_galera.cnf' | grep -v grep | wc -l".format(port=port, data_dir=data_dir)).readlines()[0].split('\n')[0]
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


def login_instance(admin_user, admin_pwd, port, data_dir):
    if is_exist_instance(port, data_dir):
        os.system("mysql -u{admin_user} -p{admin_pwd} -S {data_dir}/mysql{port}/mysql{port}.sock".format(port=port, data_dir=data_dir, admin_pwd=admin_pwd, admin_user=admin_user))
        #os.system("mysql -u{admin_user} -p{admin_pwd} -h127.0.0.1 -P{port}".format(port=port, admin_pwd=admin_pwd, admin_user=admin_user))
    else:
        status = {"action": "instance {port} have stoped or not exist, could not login".format(port=port), "status": "FAIL"}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)


def main():
    arg = get_arg()

    login_instance(admin_user, admin_pwd, arg.P, arg.d)

if __name__ == '__main__':
    main()



