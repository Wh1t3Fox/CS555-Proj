#!/usr/bin/env python

import socket

s = socket.socket()
host = '127.0.0.1'
port = 44444
s.connect((host,port))

print s.recv(1024)
s.close
