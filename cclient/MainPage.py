# -*- coding: gb2312 -*-
from tkinter import *
from view import *  # 菜单栏对应的各个子页面
import threading


class MainPage(object):
    def __init__(self, s, master=None):
        self.sock = s
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (450, 500))  # 设置窗口大小
        self.createPage()

    def createPage(self):
        Label(self.root, text='message:').grid(row=0, sticky=W, padx=5, pady=5)
        self.r_frame = Frame(self.root)
        self.r_frame.grid(row=1, sticky=W)
        self.r_text = Text(self.r_frame, width=60, height=20)
        self.r_sbar = Scrollbar(self.r_frame, command=self.r_text.yview,
                                orient=VERTICAL)
        self.r_text.config(yscrollcommand=self.r_sbar.set)
        self.r_text.bind("<KeyPress>", lambda e: 'break')
        self.r_text.pack(side=LEFT, fill=BOTH)
        self.r_sbar.pack(side=RIGHT, fill=Y)

        Label(self.root, text='command:').grid(row=4, sticky=W, padx=5, pady=5)
        # type text
        self.t_frame = Frame(self.root)
        self.t_frame.grid(row=4, sticky=W)
        self.t_text = Text(self.t_frame, width=60, height=8)
        self.t_sbar = Scrollbar(self.t_frame, command=self.t_text.yview,
                                orient=VERTICAL)
        self.t_text.config(yscrollcommand=self.t_sbar.set)
        self.t_text.pack(side=LEFT, fill=BOTH)
        self.t_sbar.pack(side=RIGHT, fill=Y)

        self.t_text.bind('<Return>', self.send_chat)

        t = threading.Thread(target=self.recvthread)
        t.start()

    def send_chat(self):
        data = self.t_text.get(1.0, 'end').strip().encode('utf-8')
        self.r_text.insert('end', 'command:' + data + '\n')
        self.sock.send(data)
        self.t_text.delete(1.0, 'end')
        return 'break'

    def recvthread(self):
        while True:
            buf = self.sock.recv(1024)
            if not buf:
                break
            self.r_text.insert('end', 'recv:' + buf.decode() + '\n')
            # self.sock.close()
