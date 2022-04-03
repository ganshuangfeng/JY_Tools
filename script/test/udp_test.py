# -*- coding: utf-8 -*- 
import os
import os.path
import xdrlib,sys
import xlrd
import types
import time

import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(("127.0.0.1", 9002))
while True:
    receive_data, client_address = server_socket.recvfrom(1024)
    print("client addr: %s , data:%s" % (client_address, receive_data.decode()))
	
	
# 客户端：	
# u = socket(AF_INET, SOCK_DGRAM)	
# u.sendto("falsdkfddddaa",("127.0.0.1",9002))	