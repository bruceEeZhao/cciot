from tkinter import *
from tkinter.messagebox import *


class InputFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.itemName = StringVar()
        self.importPrice = StringVar()
        self.sellPrice = StringVar()
        self.deductPrice = StringVar()
        self.createPage()

    def createPage(self):
        Label(self).grid(row=0, stick=W, pady=10)
        Label(self, text='mdname: ').grid(row=1, stick=W, pady=10)
        Entry(self, textvariable=self.itemName).grid(
            row=1, column=1, stick=E)
        Label(self, text='jinjia /$: ').grid(row=2, stick=W, pady=10)
        Entry(self, textvariable=self.importPrice).grid(
            row=2, column=1, stick=E)
        Label(self, text='shoujia /$: ').grid(row=3, stick=W, pady=10)
        Entry(self, textvariable=self.sellPrice).grid(
            row=3, column=1, stick=E)
        Label(self, text='youhui /$: ').grid(row=4, stick=W, pady=10)
        Entry(self, textvariable=self.deductPrice).grid(
            row=4, column=1, stick=E)
        Button(self, text='luru').grid(row=6, column=1, stick=E, pady=10)


class QueryFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.itemName = StringVar()
        self.createPage()

    def createPage(self):
        Label(self, text='chaxun').pack()


class CountFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.createPage()

    def createPage(self):
        Label(self, text='tongji').pack()


class AboutFrame(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.createPage()

    def createPage(self):
        Label(self, text='about').pack()
