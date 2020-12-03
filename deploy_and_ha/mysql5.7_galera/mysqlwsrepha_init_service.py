#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Created on 2018-05-13

@author: zhihao
@used: init service of mysql-wsrep 5.7.20
"""


import time
import json
import os
import sys
reload(sys)


log = '/auto_op_stuff/galera_mysqlha/mysqlwsrepha_init_service_{now_time}.log'.format(now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))


def write_log(log,log_content):
    os.system('mkdir -p /auto_op_stuff/galera_mysqlha')
    with open(log, 'a+') as log_handle:
        log_handle.write("[{now_time}]{log_content}\n".format(now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
                                         log_content=log_content))


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


# if 0 :not exist ,else exist
def package_exist_stat(package_name):
    stat = os.popen("dpkg -l | grep {package_name} | grep -v grep | wc -l".format(package_name=package_name)).readlines()[0].split('\n')[0]
    if stat == '0':
        status = {"action": "install {package_name}".format(package_name=package_name), "status": "FAIL"}
        print json.dumps(status)
        write_log(log, status)
        sys.exit(0)
    else:
        status = {"action": "install {package_name}".format(package_name=package_name), "status": "OK"}
        print json.dumps(status)
        write_log(log, status)


def install_dependents():
    os.system("apt-get install python-software-properties")
    os.system("apt-get install software-properties-common")
    os.system("apt-key adv --keyserver keyserver.ubuntu.com --recv BC19DDBA")
    #source
    os.system("echo 'deb http://releases.galeracluster.com/mysql-wsrep-5.7.20-25.13/ubuntu trusty main' >> /etc/apt/sources.list.d/galera.list")
    os.system("echo 'deb http://releases.galeracluster.com/galera-3/ubuntu trusty main' >> /etc/apt/sources.list.d/galera.list")
    #pref
    os.system("echo 'Package: *' >> /etc/apt/preferences.d/galera.pref")
    os.system("echo 'Pin: origin releases.galeracluster.com' >> /etc/apt/preferences.d/galera.pref")
    os.system("echo 'Pin-Priority: 1001' >> /etc/apt/preferences.d/galera.pref")
    os.system("apt-get update")

    #get galera3 mysql-wsrep-5.7
    os.system("apt-get install galera-3 galera-arbitrator-3 mysql-wsrep-5.7")

    # os.system("dpkg -l | grep xauth | grep -v grep | wc -l")
    package_exist_stat('galera-3')
    package_exist_stat('galera-arbitrator-3')
    package_exist_stat('mysql-wsrep-5.7')
    package_exist_stat('mysql-wsrep-client-5.7')
    package_exist_stat('mysql-wsrep-common-5.7')
    package_exist_stat('mysql-wsrep-server-5.7')


def add_user_group(user, group):
    #adduser = 'adduser {user}'.format(user=user)
    #os.system(adduser)
    groupadd = 'groupadd {group}'.format(group=group)
    user_in_group = 'useradd -g {group} {user}'.format(user=user, group=group)

    os.system(groupadd)
    os.system(user_in_group)

    user_group_exist_stat('mysql', 'mysql')


def make_mysql_dir(data_dir):
    os.system("mkdir -p {data_dir}".format(data_dir=data_dir))
    dir_exist_stat("{data_dir}".format(data_dir=data_dir))


def main():
    install_dependents()
    add_user_group('mysql', 'mysql')
    make_mysql_dir('/data1')


if __name__ == '__main__':
    main()
