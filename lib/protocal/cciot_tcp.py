# -*- coding:utf-8 -*-
# AUTHOR:   zhao
# EMAIL:   bruce.e.zhao@gmail.com
# FILE:     cciot_tcp.py
# ROLE:     TODO (some explanation)
# CREATED:  2017-05-07 14:49:03
# MODIFIED: 2017-05-07 14:49:05
# from socket import socket, AF_INET, SOCK_STREAM
from .message_handle import Message_handle
from ..database import database_handle
from enum import Enum
import threading
import Queue
import time
import sys
import socket

online_list_device = {}   # id:[sock, addr, devicename]
online_list_user = {}
mes_queue = Queue.Queue()
mutex = threading.Lock()


class Cciot_tcp:

    def __init__(self, ipaddress='127.0.0.1', port=8181):
        '''
        init and band ip
        '''
        self.__ipaddress = (ipaddress, port)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind(self.__ipaddress)
        self.__buffer_size = 1024  # »º³åÇø

    def receive(self):
        '''
        accept message from socket,put message into dict£¬then decode
        '''
        self.__socket.listen(10)
        print('Waiting for connection...')
        while True:
            self.__sock, self.__addr = self.__socket.accept()
            t = threading.Thread(target=self.tcplink)
            t.start()

    def tcplink(self):
        print('Accept new connection from %s:%s...' % self.__addr)
        # while True:
        # try:
        while True:
                # self.__sock.settimeout(60)
            raw_data = self.__sock.recv(self.__buffer_size)
            # print(raw_data)
            pym = Message_handle()
            python_mes = pym.decode(raw_data)
            if python_mes:
                self.resolve(python_mes)
            else:
                pass
        # except socket.timeout:
        #    print('time out')
        #    print('Connection from %s:%s closed' % self.__addr)
        #    self.__socket.close()

    def close(self):
        self.__socket.close()

    def __del__(self):
        self.__socket.close()

    def resolve(self, python_mes):
        function_dict = {'checkin': self.checkin, 'update': self.update,
                         'login': self.login, 'logout': self.logout,
                         'say': self.say, 'isOL': self.isOL,
                         'status': self.status, 'alert': self.alert,
                         'time': self.severtime, 'checkout': self.checkout,
                         'signalsay': self.signalsay,
                         'register': self.register,    # user register
                         }
        r = python_mes['M']
        if r not in function_dict:
            # do nothing, later can add function
            print('no such command')
        else:
            function_dict[r](python_mes)

    def checkin(self, python_mes):
        if self.accessable(python_mes):
            name = online_list_device[int(python_mes['ID'])][2]
            deviceid = 'D' + python_mes['ID']
            mes = {'M': 'checkinok', 'ID': deviceid, 'T': time.time(),
                   'NAME': name}
            j_mes = Message_handle()
            jmes = j_mes.encode(mes) + "\n"
            try:
                self.__sock.send(jmes)
            except socket.error, e:
                online_list_device.pop(int(python_mes['ID']))
                print("error sending data:%s" % e)
        else:
            pass

    def update(self, python_mes):
        pass

    def login(self, python_mes):  # not scitified, need to rewrite
        mes = {}
        if self.ifonline(python_mes['ID']):
            pwd = python_mes['PWD']
            uid = int(python_mes['ID'][1:])
            if pwd == online_list_user[uid][3]:
                mes['ONLINE'] = 'True'
            else:
                mes['ONLINE'] = 'False'
        else:
            dat = database_handle.Cciot_database()
            user = dat.inquire_user(python_mes)
            dat.close()
            if user:
                sock = self.__sock
                addr = self.__addr
                user_name = user[1]
                user_id = user[0]
                user_pwd = user[3]
                online_list_user[user_id] = [sock, addr, user_name, user_pwd]
                mes['ONLINE'] = 'True'
            else:
                mes['ONLINE'] = 'False'
        mes['M'] = 'login'
        j_mes = Message_handle()
        jmes = j_mes.encode(mes) + "\n"
        try:
            self.__sock.send(jmes)
        except socket.error, e:
            print("error sending data:%s" % e)

    def logout(self, python_mes):
        pass

    def signalsay(self, python_mes):
        '''
        different from the protocal of bigiot, add toid
        '''
        temp = python_mes['toID']
        if self.ifonline(python_mes['ID']) and self.ifonline(temp):
            toid_type = python_mes['toID'][0:1]
            toid = int(python_mes['toID'][1:])
            fromid_type = python_mes['ID'][0:1]
            fromid = int(python_mes['ID'][1:])
            if 'SIGN' in python_mes:
                mes = {'M': 'say', 'ID': python_mes['ID'],
                       'NAME': online_list_device[fromid][2],
                       'C': python_mes['C'], 'SIGN': python_mes['SIGN'],
                       'T': time.time()}
            else:
                mes = {'M': 'say', 'ID': python_mes['ID'],
                       'NAME': online_list_device[fromid][2],
                       'C': python_mes['C'], 'T': time.time()}
            j_mes = Message_handle()
            jmes = j_mes.encode(mes) + "\n"
            if(toid_type == 'D'):
                if toid in online_list_device:
                    sock = online_list_device[toid][0]
                    try:
                        sock.send(jmes)
                    except socket.error, e:
                        online_list_device.pop(toid)
                        print("error sending data:%s" % e)
                else:
                    pass
            elif (toid_type == 'U'):
                if toid in online_list_user:
                    sock = online_list_user[toid][0]
                    try:
                        sock.send(jmes)
                    except socket.error, e:
                        online_list_user.pop(toid)
                        print("error sending data:%s" % e)
                else:  # not online
                    pass
            else:
                pass

    def say(self, python_mes):   # send mesage to all charactor
        if self.ifonline(python_mes['ID']):
            fromid_type = python_mes['ID'][0:1]
            fromid = int(python_mes['ID'][1:])
            if 'SIGN' in python_mes:
                mes = {'M': 'say', 'ID': python_mes['ID'],
                       'C': python_mes['C'], 'SIGN': python_mes['SIGN'],
                       'T': time.time()}
            else:
                mes = {'M': 'say', 'ID': python_mes['ID'],
                       'C': python_mes['C'], 'T': time.time()}
            j_mes = Message_handle()
            jmes = j_mes.encode(mes) + "\n"
            for toid in online_list_device.keys():
                if toid != fromid:
                    sock = online_list_device[toid][0]
                    try:
                        sock.send(jmes)
                    except socket.error, e:
                        online_list_device.pop(toid)
                        print("error sending data:%s" % e)
            for toid in online_list_user.keys():
                if toid != fromid:
                    sock = online_list_user[toid][0]
                    try:
                        sock.send(jmes)
                    except socket.error, e:
                        online_list_user.pop(toid)
                        print("error sending data:%s" % e)

    def isOL(self, python_mes):
        R = {}
        for equ_id in python_mes['ID']:
            if self.ifonline(equ_id):
                R[equ_id] = 1
            else:
                R[equ_id] = 0
        mes = {'M': 'isOL', 'R': R, 'T': time.time()}
        j_mes = Message_handle()
        jmes = j_mes.encode(mes) + "\n"
        try:
            self.__sock.send(jmes)
        except socket.error, e:
            print("error sending data:%s" % e)

    def status(self, python_mes):
        pass

    def alert(self, python_mes):
        pass

    def severtime(self, python_mes):
        form = python_mes['F']
        mes = {'M': 'time'}
        if form == 'stamp':
            mes['T'] = time.time()
        elif form == 'Y-m-d':
            mes['T'] = time.strftime("%Y-%m-%d", time.localtime())
        elif form == 'Y.m.d':
            mes['T'] = time.strftime("%Y.%m.%d", time.localtime())
        elif form == 'Y-m-d H:i:s':
            mes['T'] = time.strftime("%Y-%m-%d %X", time.localtime())
        j_mes = Message_handle()
        jmes = j_mes.encode(mes) + "\n"
        try:
            self.__sock.send(jmes)
        except socket.error, e:
            print("error sending data:%s" % e)

    def checkout(self, python_mes):
        deviceid = int(python_mes['ID'])
        if self.ifonline(python_mes['ID']):
            mes1 = {'M': 'checkout', 'IP': self.__addr[0], 'T': time.time()}
            sock = online_list_device[deviceid][0]
            j_mes = Message_handle()
            jmes = j_mes.encode(mes) + "\n"
            try:
                sock.send(jmes)
            except socket.error, e:
                print("error sending data:%s" % e)
            online_list_device.pop(deviceid)
            # then send to request equment
            mes = {'M': 'checkout', 'ID': python_mes['ID'], 'T': time.time()}
            j_mes = Message_handle()
            jmes = j_mes.encode(mes) + "\n"
            try:
                self.__sock.send(jmes)
            except socket.error, e:
                print("error sending data:%s" % e)

    def register(self, python_mes):
        dat = database_handle.Cciot_database()
        userid, apikey = dat.adduser(python_mes)
        mes = {'M': 'regist', 'ID': userid, 'K': apikey}
        j_mes = Message_handle()
        jmes = j_mes.encode(mes) + "\n"
        try:
            self.__sock.send(jmes)
        except socket.error, e:
            print("error sending data:%s" % e)
        dat.close()

    def accessable(self, python_mes):
        deviceid = int(python_mes['ID'])
        if deviceid in online_list_device:
            sock = self.__sock
            addr = self.__addr
            device_name = online_list_device[deviceid][2]
            online_list_device[deviceid] = [sock, addr, device_name]
            return True
        else:
            dat = database_handle.Cciot_database()
            device = dat.inquire_device(python_mes)
            if device:
                sock = self.__sock
                addr = self.__addr
                device_name = device[1]
                online_list_device[deviceid] = [sock, addr, device_name]
                dat.close()
                return True
            else:
                dat.close()
                return False

    def ifonline(self, equment_id):
        id_type = equment_id[0:1]
        if((equment_id[1:]).isdigit() is False):
            return False
        id_num = int(equment_id[1:])
        if(id_type == 'U'):
            if id_num in online_list_user:
                return True
            else:
                return False
        elif(id_type == 'D'):
            if id_num in online_list_device:
                return True
            else:
                return False
        else:
            return False

    def equ_offline(self, equment_id):
        id_type = equment_id[0:1]
        id_num = int(equment_id[1:])
        if(id_type == 'U'):
            user_offline(equment_id)
        elif(id_type == 'D'):
            dev_offline(equment_id)
        else:
            pass

    def user_offline(self, equment_id):
        id_type = equment_id[0:1]
        id_num = int(equment_id[1:])
        off_time = time.strftime("%Y-%m-%d %X", time.localtime())
        ip = online_list_user[id_num][1][0]
        mutex.acquire()
        dat = database_handle.Cciot_database()
        dat.update_user(id_num, off_time, ip)
        dat.close()
        online_list_user.pop(id_num)
        mutex.release()

    def dev_offline(self, equment_id):
        id_type = equment_id[0:1]
        id_num = int(equment_id[1:])
        mutex.acquire()
        online_list_device.pop(id_num)
        mutex.release()
