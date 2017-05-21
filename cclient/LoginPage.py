# -*- coding: gb2312 -*-

from tkinter import *
from tkinter.messagebox import *
from MainPage import *
from RegisterPage import *


class LoginPage(object):
    def __init__(self, s, master=None):
        self.sock = s
        self.root = master
        self.root.geometry('%dx%d' % (300, 180))
        self.username = StringVar()
        self.password = StringVar()
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='account: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(
            row=1, column=1, stick=E)
        Label(self.page, text='passwd: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password,
              show='*').grid(row=2, column=1, stick=E)
        Button(self.page, text='login', command=self.loginCheck).grid(
            row=3, stick=W, pady=10)
        Button(self.page, text='register', command=self.register).grid(
            row=3, column=1, stick=E)

    def loginCheck(self):
        name = self.username.get()
        passwd = self.password.get()
        name = 'U' + name
        sensordata = {'M': 'login', 'ID': name, "PWD": passwd}
        strdata = json.dumps(sensordata) + "\n"
        self.sock.send(strdata.encode())
        ret = self.sock.recv(1024)
        online = (json.loads(ret.decode()))['ONLINE']
        if online == 'True':
            self.page.destroy()
            MainPage(self.sock, self.root)
        else:
            showinfo(title='error', message='account or passwd error！')

    def register(self):
        self.page.destroy()
        RegisterPage(self.sock, self.root)
        # self.page.wait_window(pw)
