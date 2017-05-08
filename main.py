from lib.protocal import cciot_tcp

p = cciot_tcp.Cciot_tcp('192.168.191.1', 8181)
p.receive()
