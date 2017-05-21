# -*- coding: gb2312 -*-

from tkinter import *
from tkinter.messagebox import *
import json
import LoginPage
from imp import reload


class RegisterPage(object):
    def __init__(self, s, master=None):
        self.sock = s
        self.root = master  # 定义内部变量root
        self.name = StringVar()
        self.passwd1 = StringVar()
        self.passwd2 = StringVar()
        self.email = StringVar()
        self.root.geometry('%dx%d' % (600, 400))  # 设置窗口大小
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)
        self.page.pack()

        Label(self.page).grid(row=0, stick=W, pady=10)
        Label(self.page, text='name: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.name).grid(
            row=1, column=1, stick=E)

        Label(self.page, text='passwd1: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.passwd1,
              show='*').grid(row=2, column=1, stick=E)

        Label(self.page, text='passwd2: ').grid(row=3, stick=W, pady=10)
        Entry(self.page, textvariable=self.passwd2,
              show='*').grid(row=3, column=1, stick=E)

        Label(self.page, text='email: ').grid(row=4, stick=W, pady=10)
        Entry(self.page, textvariable=self.email).grid(
            row=4, column=1, stick=E)

        Button(self.page, text='back', command=self.back).grid(
            row=6, stick=W, pady=10)

        Button(self.page, text='commit', command=self.commit).grid(
            row=6, column=1, stick=E, pady=10)

    def back(self):
        self.page.destroy()
        reload(LoginPage)
        LoginPage.LoginPage(self.sock, self.root)

    def commit(self):
        flag = False
        passwd1 = self.passwd1.get()
        passwd2 = self.passwd2.get()
        email = self.email.get()
        name = self.name.get()
        if name == '':
            showinfo(title='error', message='name cant be empty')
        if passwd1 == passwd2:
            passwdstatus = self.ProcessPassword(passwd1)
            if passwdstatus is False:
                showinfo(title='error', message='Passwords should be composed\
                of uppercase letters, lowercase letters, and numbers,\
                no less than 8 digits')
            else:
                emailstatus = self.ProcessMail(email)
                if emailstatus is True:
                    flag = True
                else:
                    showinfo(title='error', message='email error')
        else:
            showinfo(title='error', message='two passwords are not euqal')

        if flag is True:  # send message to server
            self.regist()

    def ProcessMail(self, inputMail):
        isMatch = bool(re.match(
            r"[a-zA-Z0-9]+\@+[a-zA-Z0-9]+\.+[a-zA-Z]", inputMail, re.VERBOSE))
        return isMatch

    def ProcessPassword(self, inputPassword):
        isMatch = bool(re.match(r"[a-zA-Z0-9]{8}", inputPassword, flags=0))

        if isMatch:
            type = [False, False, False]
            for i in range(0, 8):
                temp = inputPassword[i]
                if ord(temp) >= ord('0') and ord(temp) <= ord('9'):
                    type[0] = True
                elif ord(temp) >= ord('a') and ord(temp) <= ord('z'):
                    type[1] = True
                elif ord(temp) >= ord('A') and ord(temp) <= ord('Z'):
                    type[2] = True
            for i in type:
                if i is False:
                    isMatch = False
                    break

        if isMatch:
            for i in range(0, 7):
                temp = inputPassword[i]
                for j in range(i + 1, 8):
                    if inputPassword[j] == temp:
                        isMatch = False
                        break
        return isMatch

    def regist(self):
        name = self.name.get()
        passwd = self.passwd1.get()
        email = self.email.get()
        sensordata = {"M": "register", "NAME": name,
                      "PWD": passwd, "EMAIL": email}
        strdata = json.dumps(sensordata) + "\n"
        self.sock.send(strdata.encode())
        ret = self.sock.recv(1024)
        uid = (json.loads(ret.decode()))['ID']
        showinfo(title='mes', message='this id as your login id:%s' % uid)
