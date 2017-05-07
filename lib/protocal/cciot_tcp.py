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
import threading
import Queue


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
            sock, addr = self.__socket.accept()
            t = threading.Thread(target=self.tcplink, args=(sock, addr))
            t.start()

    def tcplink(self, sock, addr):
        print('Accept new connection from %s:%s...;' % addr)
        while True:
            raw_data = sock.recv(self.__buffer_size)
            pym = Message_handle()
            python_mes = pym.decode(raw_data)
            if self.accessable(python_mes, addr):
                self.resolve(python_mes, addr)
            else:  # do nothing
                pass
        self.__socket.close()
        print('Connection from %s:%s closed' % addr)

    def send(self, message, addr):
        '''
        change message to json and send.
        '''
        self.__socket.sendto(message, addr)

    def close(self):
        self.__socket.close()

    def __del__(self):
        self.close()

    def resolve(self, python_mes, addr):
        if python_mes['M'] == 'checkin':
            self.checkin(python_mes, addr)
        elif python_mes['M'] == 'update':
            self.update(python_mes, addr)
        elif python_mes['M'] == 'login':
            self.login(python_mes, addr)
        elif python_mes['M'] == 'logout':
            self.logout(python_mes, addr)
        elif python_mes['M'] == 'say':
            self.to_other(python_mes)
        elif python_mes['M'] == 'isOL':
            self.isOL(python_mes, addr)
        elif python_mes['M'] == 'status':
            self.status(python_mes, addr)
        elif python_mes['M'] == 'alert':
            self.alert(python_mes, addr)
        elif python_mes['M'] == 'time':
            self.severtime(python_mes, addr)
        elif python_mes['M'] == 'checkout':
            self.checkout(python_mes, addr)
        else:
            # do nothing, later can add function
            print('no such command')

    def checkin(self, python_mes, addr):
        pass

    def update(self, python_mes, addr):
        print(python_mes['V'])

    def login(self, python_mes, addr):
        pass

    def logout(self, python_mes, addr):
        pass

    def say(self, python_mes, addr):
        pass

    def isOL(self, python_mes, addr):
        pass

    def status(self, python_mes, addr):
        pass

    def alert(self, python_mes, addr):
        pass

    def severtime(self, python_mes, addr):
        pass

    def checkout(self, python_mes, addr):
        pass

    def to_other(self, python_mes):
        toid = python_mes['toID']
        if toid in online_list:
            self.send(message, addr)
        else:
            pass

    def restart(self):
        pass

    def accessable(self, python_mes, addr):
        deviceid = python_mes['ID']
    #    print(deviceid)
        if deviceid in self.online_list:
            return True
        else:
            dat = database_handle.Cciot_database()
            if dat.inquire(deviceid):
                self.online_list[deviceid] = python_mes
                self.online_addr[deviceid] = addr
                return True
            else:
                return False
