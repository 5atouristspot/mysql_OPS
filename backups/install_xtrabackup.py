#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""

@author: devin
@used: install percona-xtrabackup-24
"""


import time
import json
import os
import sys
reload(sys)


def package_exist_stat(package_name):
    stat = os.popen("dpkg -l | grep {package_name} | grep -v grep | wc -l".format(package_name=package_name)).readlines()[0].split('\n')[0]
    if stat == '0':
        status = {"action": "install {package_name}".format(package_name=package_name), "status": "FAIL"}
        print json.dumps(status)
        sys.exit(0)
    else:
        status = {"action": "install {package_name}".format(package_name=package_name), "status": "OK"}
        print json.dumps(status)


def install_xtrabackup():
    os.system("cd /auto_op_stuff/galera_mysqlha && wget https://repo.percona.com/apt/percona-release_0.1-4.$(lsb_release -sc)_all.deb")
    os.system("dpkg -i /auto_op_stuff/galera_mysqlha/percona-release_0.1-4.$(lsb_release -sc)_all.deb")
    os.system("apt-get update")
    os.system("apt-get install percona-xtrabackup-24 -y")

    package_exist_stat('percona-release')
    package_exist_stat('percona-xtrabackup-24')


def main():
    install_xtrabackup()


if __name__ == '__main__':
    main()
