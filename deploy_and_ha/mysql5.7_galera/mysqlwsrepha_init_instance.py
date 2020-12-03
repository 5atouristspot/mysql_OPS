#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Created on 2018-05-13

@author: zhihao
@used: init instances of mysql-wsrep-5.7.20
"""
import argparse
import time
import json
import os
import sys
reload(sys)

log = '/auto_op_stuff/galera_mysqlha/mysqlwsrepha_init_instance_{now_time}.log'.format(now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))


def write_log(log,log_content):
    os.system('mkdir -p /auto_op_stuff/galera_mysqlha')
    with open(log, 'a+') as log_handle:
        log_handle.write("[{now_time}]{log_content}\n".format(now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
                                         log_content=log_content))


# if 0 :not exist ,else exist
def dir_exist_stat(dir_name):
    stat = os.path.exists(dir_name)

    if stat is not True:
        status = {"action": "make directories {dir_name}".format(dir_name=dir_name), "status": "FAIL"}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)
    else:
        status = {"action": "make directories {dir_name}".format(dir_name=dir_name), "status": "OK"}
        print json.dumps(status)
        write_log(log, status)


#if 0 :not exist ,else exist
def user_group_exist_stat(user_name,group_name):
    #group
    group_stat = os.popen("grep {group_name}: /etc/group | wc -l".format(group_name=group_name)).readlines()[0].split('\n')[0]
    #user
    user_stat = os.popen("grep {user_name}: /etc/passwd | wc -l".format(user_name=user_name)).readlines()[0].split('\n')[0]

    if group_stat == '0':
        status = {"action": "add group {group_name}".format(group_name=group_name), "status": "FAIL"}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)
    else:
        status = {"action": "add group {group_name}".format(group_name=group_name), "status": "OK"}
        print json.dumps(status)
        write_log(log, status)

    if user_stat == '0':
        status = {"action": "add user {user_name}".format(user_name=user_name), "status": "FAIL"}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)
    else:
        status = {"action": "add user {user_name}".format(user_name=user_name), "status": "OK"}
        print json.dumps(status)
        write_log(log, status)


# if 0 :not exist ,else exist
def file_exist_stat(file_name):
    stat = os.path.isfile(file_name)

    if stat is not True:
        status = {"action": "install/get {file_name}".format(file_name=file_name), "status": "FAIL"}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)
    else:
        status = {"action": "install/get {file_name}".format(file_name=file_name), "status": "OK"}
        print json.dumps(status)
        write_log(log, status)


#if 0 :not exist ,else exist
def content_stat(file_name,modify_content):
    stat = os.popen("grep '{modify_content}' {file_name} | wc -l".format(file_name=file_name, modify_content=modify_content)).readlines()[0].split('\n')[0]

    if stat == '0':
        status = {"action": "modify {file_name} -> {modify_content}".format(file_name=file_name, modify_content=modify_content), "status": "FAIL"}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)
    else:
        status = {"action": "modify {file_name} -> {modify_content}".format(file_name=file_name, modify_content=modify_content), "status": "OK"}
        print json.dumps(status)
        write_log(log, status)


def make_data_dir(dir_name, port):
    if os.path.exists("{dir_name}/mysql{port}".format(dir_name=dir_name, port=port)) is False:
        os.system("mkdir -p {dir_name}/mysql{port}".format(dir_name=dir_name, port=port))
        os.system("chown -R my{port}:mysql {dir_name}/mysql{port}/".format(dir_name=dir_name, port=port))

        dir_exist_stat("{dir_name}/mysql{port}".format(dir_name=dir_name, port=port))
    else:
        status = {"ERROR": "{dir_name}/mysql{port} have exist , Prevent data coverage,could not make it! ".format(port=port, dir_name=dir_name)}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)


def add_user(user, group):
    #adduser = 'adduser {user}'.format(user=user)
    #os.system(adduser)
    user_in_group = 'useradd -g {group} {user}'.format(user=user, group=group)
    os.system(user_in_group)

    user_group_exist_stat(user, group)


def modify_mysql_conf(port):
    #make conf
    #os.system("cp /auto_op_stuff/galera_mysqlha/my3307_galera.cnf /auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(port=port))
    file_exist_stat("/auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(port=port))
    #modify server-id
    ip_tail = os.popen("ifconfig eth0 | grep 'inet addr' | sed 's/^.*addr://g' |sed 's/  Bcast:.*$//g'|awk -F '.' '{print $3 $4}'").readlines()[0].split('\n')[0]
    new_serverid = ip_tail + port
    os.system("sed -i 's/server-id = 3307/server-id = {new_serverid}/g' /auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(port=port, new_serverid=new_serverid))
    os.system("sed -i 's/3307/{port}/g' /auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(port=port))

    content_stat("/auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(port=port), "server-id = {new_serverid}".format(new_serverid=new_serverid))


def modify_wsrep_conf(port):
    #ifconfig eth0 | grep 'inet addr' | sed 's/^.*addr://g' |sed 's/  Bcast:.*$//g'
    local_ip = os.popen("ifconfig eth0 | grep 'inet addr' | sed 's/^.*addr://g' |sed 's/  Bcast:.*$//g'").readlines()[0].split('\n')[0]
    os.system("sed -i 's/127.0.0.1/{local_ip}/g' /auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(port=port, local_ip=local_ip))

    base_port = str(int(port)+1000)
    recv_port = str(int(port)+2000)
    sst_receive = str(int(port)+3000)
    os.system("sed -i 's/5567/{base_port}/g' /auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(port=port,base_port=base_port))
    os.system("sed -i 's/5568/{recv_port}/g' /auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(port=port,recv_port=recv_port))
    os.system("sed -i 's/5569/{sst_receive}/g' /auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(port=port,sst_receive=sst_receive))
    os.system("sed -i 's/wsrep_cluster_name=galera/wsrep_cluster_name=galera{port}/g' "
              "/auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(port=port))

    ip_tail = os.popen("ifconfig eth0 | grep 'inet addr' | sed 's/^.*addr://g' |sed 's/  Bcast:.*$//g'|awk -F '.' '{print $3 $4}'").readlines()[0].split('\n')[0]
    new_uuid_tail = ip_tail + port
    os.system("sed -i 's/wsrep_node_name=galera/wsrep_node_name=galera{new_uuid_tail}/g' "
              "/auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(new_uuid_tail=new_uuid_tail,port=port))


def modify_auto_cnf(port, data_dir):
    ip_tail = os.popen("ifconfig eth0 | grep 'inet addr' | sed 's/^.*addr://g' |sed 's/  Bcast:.*$//g'|awk -F '.' '{print $3 $4}'").readlines()[0].split('\n')[0]
    new_uuid_tail = ip_tail + port
    if len(new_uuid_tail) == 7:
        new_uuid_tail = '0' + new_uuid_tail

    old_uuid = os.popen("grep server-uuid {data_dir}/mysql{port}/auto.cnf".format(data_dir=data_dir, port=port)).readlines()[0].split('\n')[0]
    old_uuid_tail = old_uuid[-8:]

    os.system("sed -i 's/{old_uuid_tail}/{new_uuid_tail}/g' {data_dir}/mysql{port}/auto.cnf".format(old_uuid_tail=old_uuid_tail, new_uuid_tail=new_uuid_tail, data_dir=data_dir, port=port))

    content_stat("{data_dir}/mysql{port}/auto.cnf".format(data_dir=data_dir, port=port), "{new_uuid_tail}".format(new_uuid_tail=new_uuid_tail))


def init_instance(port, data_dir):
    os.system("/usr/sbin/mysqld --defaults-file=/auto_op_stuff/galera_mysqlha/my{port}_galera.cnf --basedir=/usr --initialize-insecure".format(port=port))
    time.sleep(10)
    file_exist_stat("{data_dir}/mysql{port}/auto.cnf".format(data_dir=data_dir, port=port))


def move_cnf_to_datadir(port, data_dir):
    # backup conf
    os.system("cp /auto_op_stuff/galera_mysqlha/my{port}_galera.cnf /auto_op_stuff/galera_mysqlha/my{port}_galera.cnf.{now_time}".format(port=port, now_time=time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))))

    os.system("mv /auto_op_stuff/galera_mysqlha/my{port}_galera.cnf {data_dir}/mysql{port}/".format(port=port, data_dir=data_dir))

    file_exist_stat("{data_dir}/mysql{port}/my{port}_galera.cnf".format(data_dir=data_dir, port=port))


def get_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", help="modify instance to first node of cluster",
                        action="store_true")
    parser.add_argument("--notfirst", help="modify instance to joiner node of cluster",
                        action="store_true")
    parser.add_argument('--donor', type=str, help="the node ip have in cluster, eg :10.20.4.138:5567,10.20.4.139:5567", default='3306')
    parser.add_argument('-P', type=str, help="port of instance", default='3307')
    parser.add_argument('-d', type=str, help="data directory of instance, eg: /data1", default='/data1')

    args = parser.parse_args()

    return args


def main():
    arg = get_arg()

    if arg.first:
        add_user("my{port}".format(port=arg.P), "mysql")
        make_data_dir(arg.d, arg.P)
        os.system(
            "cp /auto_op_stuff/galera_mysqlha/my3307_galera.cnf /auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(
                port=arg.P))
        modify_mysql_conf(arg.P)
        modify_wsrep_conf(arg.P)
        init_instance(arg.P, arg.d)
        move_cnf_to_datadir(arg.P, arg.d)
        #modify_auto_cnf(arg.P, arg.d)

    elif arg.notfirst:
        add_user("my{port}".format(port=arg.P), "mysql")
        make_data_dir(arg.d, arg.P)
        os.system(
            "cp /auto_op_stuff/galera_mysqlha/my3307_galera.cnf /auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(
                port=arg.P))
        os.system("sed -i 's/wsrep_cluster_address=gcomm:\/\//wsrep_cluster_address=gcomm:\/\/{cluster_ip}/g' "
                  "/auto_op_stuff/galera_mysqlha/my{port}_galera.cnf".format(port=arg.P,cluster_ip=arg.donor))
        modify_mysql_conf(arg.P)
        modify_wsrep_conf(arg.P)
        init_instance(arg.P, arg.d)
        move_cnf_to_datadir(arg.P, arg.d)
        #modify_auto_cnf(arg.P, arg.d)
    else:
        status = {"ERROR": "must point to first node or notfirst ,please input -h"}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)


if __name__ == '__main__':
    main()
