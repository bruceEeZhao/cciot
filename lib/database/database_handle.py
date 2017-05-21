# -*- coding:utf-8 -*-
# AUTHOR:   zhao
# EMAIL:   bruce.e.zhao@gmail.com
# FILE:     database_handle.py
# ROLE:     TODO (some explanation)
# CREATED:  2017-04-20 12:00:07
# MODIFIED: 2017-04-20 12:00:10
import MySQLdb
import hashlib


class Cciot_database:

    def __init__(self, host='localhost', user='root', passwd='tzb',
                 db='CCIOT', port=3306):
        try:
            self.__coon = MySQLdb.connect(host, user, passwd, db, port)
        except MySQLdb.Error:
            print('can not connect database')

    def insertdata(self):
        '''
        insertdata into database
        '''
        pass

    def adduser(self, python_mes):
        cur = self.__coon.cursor()
        sql = "select * from IotUser"
        total = cur.execute(sql)
        uid = total + 1
        apikey = hashlib.md5(str(uid)).hexdigest()[0:6]
        sql = "insert into IotUser values(%d, '%s', '%s', '%s', '%s', 0, 0, null, null)" % (
            total + 1, python_mes['NAME'], apikey, python_mes['PWD'],
            python_mes['EMAIL'])
        cur.execute(sql)
        self.__coon.commit()
        return uid, apikey

    def deldata(self):
        '''
        delete data from database
        '''
        pass

    def update_user(self, id_num, off_time, ip):
        cur = self.__coon.cursor()
        sql = "update IotUser set U_lasttime = '%s', U_lastip = '%s' \
               where U_id = %d " % (off_time, ip, id_num)
        cur.execute(sql)
        self.__coon.commit()

    def update_device(self, did):
        '''
        update new data into database
        '''
        pass

    def inquire_device(self, python_mes):
        '''
        search data which profit
        '''
        deviceid = int(python_mes['ID'])
        apikey = python_mes['K']
        cur = self.__coon.cursor()
        sql = "select * from IotDevice  \
               where D_id=%d and D_apikey= '%s' " % (deviceid, apikey)
        cur.execute(sql)
        return cur.fetchone()

    def inquire_user(self, python_mes):
        if((python_mes['ID'][1:]).isdigit() is False):
            return False
        userid = int(python_mes['ID'][1:])
        passwd = python_mes['PWD']
        cur = self.__coon.cursor()
        sql = sql = "select * from IotUser  \
               where U_id=%d and U_passwd= '%s' " % (userid, passwd)
        cur.execute(sql)
        return cur.fetchone()

    def close(self):
        self.__coon.close()
