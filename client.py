#!/usr/bin/env python

import socket
from matrix import Matrix
from graph_tool.all import *

s = socket.socket()
host = '127.0.0.1'
port = 44444
s.connect((host,port))

while True:
    try:
        data = s.recv(1024)
        print data    
    
        info = raw_input("Text to send: ")
        s.send(info)
    except:
        break
        s.close
