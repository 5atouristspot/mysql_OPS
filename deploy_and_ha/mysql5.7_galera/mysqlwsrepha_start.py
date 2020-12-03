#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Created on 2018-05-13

@author: zhihao
@used: start instances of mysql-wsrep-5.7.20
"""
import argparse
import time
import json
import os
import getpass
import sys
reload(sys)


log = '/auto_op_stuff/galera_mysqlha/mysqlha.log'

admin_user = 'tfadmin'
admin_pwd = 'tfkj_secret'


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


def start_instance(port, data_dir):
    if is_exist_instance(port, data_dir) is False:
        is_dir_exist_stat("{data_dir}/mysql{port}".format(data_dir=data_dir, port=port))
        #ip_tail = os.popen("ifconfig eth0 | grep 'inet addr' | sed 's/^.*addr://g' |sed 's/  Bcast:.*$//g'|awk -F '.' '{print $3 $4}'").readlines()[0].split('\n')[0]
        #new_uuid_tail = ip_tail + port
        #os.system("sed -i 's/wsrep_node_name=galera[1-9]*/wsrep_node_name=galera{new_uuid_tail}/g' "
        #          "{data_dir}/mysql{port}/my{port}_galera.cnf".format(new_uuid_tail=new_uuid_tail,port=port,data_dir=data_dir))
        os.system("/usr/bin/mysqld_safe --defaults-file={data_dir}/mysql{port}/my{port}_galera.cnf &".format(data_dir=data_dir, port=port))
        status = {"action": "start instance {port}".format(port=port), "status": "OK"}
        print json.dumps(status)
        write_log(log, status)
    elif is_exist_instance(port, data_dir) is True:
        status = {"action": "start instance {port}, this instance have started".format(port=port), "status": "FAIL"}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)


def init_admin_user(port, data_dir, admin_user, admin_pwd):
    #init_admin_stat = os.system("/usr/local/mysql5720/bin/mysqladmin -u{admin_user} -p password {admin_pwd} -S {data_dir}/mysql{port}/mysql{port}.sock".format(port=port, data_dir=data_dir, admin_user=admin_user, admin_pwd=admin_pwd))
    init_root_stat = os.system("/usr/bin/mysqladmin -uroot -p password {admin_pwd} -S {data_dir}/mysql{port}/mysql{port}.sock".format(port=port, data_dir=data_dir, admin_user=admin_user, admin_pwd=admin_pwd))
    if init_root_stat == 0:
        status = {"action": "instance {port}, init root user".format(port=port), "status": "OK"}
        print json.dumps(status)
        write_log(log, status)
    else:
        status = {"action": "instance {port}, init root user".format(port=port), "status": "FAIL"}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)

    init_admin_stat = os.system("mysql -uroot -p{admin_pwd} -S {data_dir}/mysql{port}/mysql{port}.sock "
                                "-e\"CREATE USER {admin_user}@127.0.0.1 IDENTIFIED BY \'{admin_pwd}\';"
                                "GRANT ALL PRIVILEGES ON *.* TO {admin_user}@127.0.0.1 WITH GRANT OPTION;"
                                "GRANT PROXY ON \'\'@\'\' TO {admin_user}@127.0.0.1 WITH GRANT OPTION;"
                                "DROP USER root@localhost;"
                                "flush privileges;\"".format(port=port, data_dir=data_dir, admin_user=admin_user, admin_pwd=admin_pwd))

    init_admin_stat = os.system("mysql -uroot -p{admin_pwd} -S {data_dir}/mysql{port}/mysql{port}.sock "
                                "-e\"CREATE USER {admin_user}@localhost IDENTIFIED BY \'{admin_pwd}\';"
                                "GRANT ALL PRIVILEGES ON *.* TO {admin_user}@localhost WITH GRANT OPTION;"
                                "GRANT PROXY ON \'\'@\'\' TO {admin_user}@localhost WITH GRANT OPTION;"
                                "DROP USER root@localhost;"
                                "flush privileges;\"".format(port=port, data_dir=data_dir, admin_user=admin_user, admin_pwd=admin_pwd))

    '''
    init_admin_stat = os.system("mysql -uroot -p{admin_pwd} -S {data_dir}/mysql{port}/mysql{port}.sock "
                                "-e\"CREATE USER {admin_user}@localhost IDENTIFIED BY \'{admin_pwd}\';"
                                "GRANT ALL PRIVILEGES ON *.* TO {admin_user}@localhost WITH GRANT OPTION;"
                                "GRANT PROXY ON \'\'@\'\' TO {admin_user}@localhost WITH GRANT OPTION;"
                                "REVOKE ALL PRIVILEGES ON *.* FROM root@localhost; REVOKE PROXY ON \'\'@\'\' FROM root@localhost;"
                                "flush privileges;\"".format(port=port, data_dir=data_dir, admin_user=admin_user, admin_pwd=admin_pwd))
    '''
    if init_admin_stat == 0:
        status = {"action": "instance {port}, init tfadmin user,revoke root".format(port=port), "status": "OK"}
        print json.dumps(status)
        write_log(log, status)
    else:
        status = {"action": "instance {port}, init tfadmin user,revoke root".format(port=port), "status": "FAIL"}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)


def get_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="first time to start this instance",
                        action="store_true")
    parser.add_argument('-P', type=str, help="port of instance", default='3307')
    parser.add_argument('-d', type=str, help="data directory of instance, eg: /data1", default='/data1')

    args = parser.parse_args()

    return args


def main():
    arg = get_arg()

    if arg.init:
        start_instance(arg.P, arg.d)
        time.sleep(100)
        init_admin_user(arg.P, arg.d, admin_user, admin_pwd)
    else:
        start_instance(arg.P, arg.d)


if __name__ == '__main__':
    main()
