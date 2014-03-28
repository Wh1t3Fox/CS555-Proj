#!/usr/bin/env python

import socket
import pickle
from matrix import Matrix
from graph_tool.all import *

s = socket.socket()
host = '127.0.0.1'
port = 44444
s.connect((host,port))

m = Matrix('g2.txt')
txt = pickle.dumps(m)
while True:
    try:
        data = s.recv(1024)
        print data    
        
        info = raw_input("Enter to continue: ")
        s.send(txt)
    except:
        break
        s.close
