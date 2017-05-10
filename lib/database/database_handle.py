# -*- coding:utf-8 -*-
# AUTHOR:   zhao
# EMAIL:   bruce.e.zhao@gmail.com
# FILE:     database_handle.py
# ROLE:     TODO (some explanation)
# CREATED:  2017-04-20 12:00:07
# MODIFIED: 2017-04-20 12:00:10
import MySQLdb


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

    def deldata(self):
        '''
        delete data from database
        '''
        pass

    def update(self):
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

    def close(self):
        self.__coon.close()
