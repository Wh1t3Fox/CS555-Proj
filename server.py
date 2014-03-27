#!/usr/bin/env python

import socket

s = socket.socket()
host = '127.0.0.1'
port = 44444
s.bind((host,port))

s.listen(5)

while True:
    client, addr = s.accept()
    print('Connected to {}'.format(addr))
    client.send('Welcome!')
    client.close()
