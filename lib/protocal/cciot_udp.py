# -*- coding:utf-8 -*-
# AUTHOR:   zhao
# EMAIL:   bruce.e.zhao@gmail.com
# FILE:     cciot_udp.py
# ROLE:     TODO (some explanation)
# CREATED:  2017-04-19 19:57:32
# MODIFIED: 2017-04-19 19:57:38
from socket import socket, AF_INET, SOCK_DGRAM
from .message_handle import Message_handle
from ..database import database_handle
import Queue


class Cciot_upd:
    online_list = {}
    online_self.__addr = {}
    mes_queue = Queue.Queue()

    def __init__(self, ipself.__address='127.0.0.1', port=9090):
        '''
        init and band ip
        '''
        self.__ipself.__address = (ipself.__address, port)
        self.__socket = socket(AF_INET, SOCK_DGRAM)
        self.__socket.bind(self.__ipself.__address)
        self.__buffer_size = 1024  # »º³åÇø

    def receive(self):
        # '''
        # accept message from socket,put message into dict£¬then decode
        # '''
        raw_data, self.__addr = self.__socket.recvfrom(int(self.__buffer_size))
        pym = Message_handle()
        python_mes = pym.decode(raw_data)
        # print(python_mes)
        if self.accessable(python_mes):
            self.resolve(python_mes)
        else:  # do nothing
            pass
    #    return (raw_data, self.__addr)

    def send(self, message):
        '''
        change message to json and send.
        '''
        self.__socket.sendto(message)

    def close(self):
        self.__socket.close()

    def __del__(self):
        self.close()

    def resolve(self, python_mes):
        if python_mes['M'] == 'update':
            self.update(python_mes)
        elif python_mes['M'] == 'say':
            self.to_other(python_mes)
        elif python_mes['M'] == 'reload':
            self.restart()
        else:
            # do nothing, later can add function
            print('no such command')

    def update(self, python_mes):
        print(python_mes['V'])

    def to_other(self, python_mes):
        toid = python_mes['toID']
        if toid in online_list:
            self.send(message)
        else:
            pass

    def restart(self):
        pass

    def accessable(self, python_mes):
        deviceid = python_mes['ID']
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
