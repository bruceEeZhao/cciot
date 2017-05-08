# -*- coding:utf-8 -*-
# AUTHOR:   zhao
# EMAIL:   bruce.e.zhao@gmail.com
# FILE:     cciot_tcp.py
# ROLE:     TODO (some explanation)
# CREATED:  2017-05-07 14:49:03
# MODIFIED: 2017-05-07 14:49:05
from socket import socket, AF_INET, SOCK_STREAM
from .message_handle import Message_handle
from ..database import database_handle
from enum import Enum
import threading
import Queue
import time


class Cciot_tcp:

    online_list = {}
    online_addr = {}
    mes_queue = Queue.Queue()

    def __init__(self, ipaddress='127.0.0.1', port=8181):
        '''
        init and band ip
        '''
        self.__ipaddress = (ipaddress, port)
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.bind(self.__ipaddress)
        self.__buffer_size = 1024  # »º³åÇø

    def receive(self):
        # '''
        # accept message from socket,put message into dict£¬then decode
        # '''
        self.__socket.listen(10)
        print('Waiting for connection...')
        while True:
            self.__sock, self.__addr = self.__socket.accept()
            t = threading.Thread(target=self.tcplink)
            t.start()

    def tcplink(self):
        print('Accept new connection from %s:%s...' % self.__addr)
        while True:
            raw_data = self.__sock.recv(self.__buffer_size)
            print(raw_data)
            pym = Message_handle()
            python_mes = pym.decode(raw_data)
            self.resolve(python_mes)
        self.__socket.close()
        print('Connection from %s:%s closed' % addr)

    def close(self):
        self.__socket.close()

    def __del__(self):
        self.close()

    def resolve(self, python_mes):
        if python_mes['M'] == 'checkin':
            self.checkin(python_mes)
        elif python_mes['M'] == 'update':
            self.update(python_mes)
        elif python_mes['M'] == 'login':
            self.login(python_mes)
        elif python_mes['M'] == 'logout':
            self.logout(python_mes)
        elif python_mes['M'] == 'say':
            self.say(python_mes)
        elif python_mes['M'] == 'isOL':
            self.isOL(python_mes)
        elif python_mes['M'] == 'status':
            self.status(python_mes)
        elif python_mes['M'] == 'alert':
            self.alert(python_mes)
        elif python_mes['M'] == 'time':
            self.severtime(python_mes)
        elif python_mes['M'] == 'checkout':
            self.checkout(python_mes)
        else:
            # do nothing, later can add function
            print('no such command')

    def checkin(self, python_mes):
        id = 'D' + python_mes['ID']
        mes = {'M': 'checkinok', 'ID': id, 'T': time.time(), 'NAME': 'zz'}
        # mes2 = {'M': 'login', 'ID': id, 'T': time.time(), 'NAME': 'zz'}
        # print(mes)
        j_mes = Message_handle()
        jmes = j_mes.encode(mes) + "\n"
        if self.accessable(python_mes):
            self.__sock.send(jmes)
        else:
            pass

    def update(self, python_mes):
        print(python_mes['V'])

    def login(self, python_mes):
        pass

    def logout(self, python_mes):
        pass

    def say(self, python_mes):
        print(python_mes['C'])

    def isOL(self, python_mes):
        pass

    def status(self, python_mes):
        pass

    def alert(self, python_mes):
        pass

    def severtime(self, python_mes):
        pass

    def checkout(self, python_mes):
        pass

    def restart(self):
        pass

    def accessable(self, python_mes):
        deviceid = int(python_mes['ID'])
    #    print(deviceid)
        if deviceid in self.online_list:
            return True
        else:
            dat = database_handle.Cciot_database()
            if dat.inquire(deviceid):
                self.online_list[deviceid] = python_mes
                self.online_addr[deviceid] = self.__addr
                return True
            else:
                return False
