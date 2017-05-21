from tkinter import *
from LoginPage import *
import socket


IP = "192.168.43.203"
PORT = 8181
addr = (IP, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(addr)

root = Tk()
root.title('cclient')
LoginPage(s, root)
root.mainloop()
