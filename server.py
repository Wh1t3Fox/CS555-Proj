#!/usr/bin/env python

import socket
from matrix import Matrix
from random import randint
import thread

def handler(client, addr):
    while True:
        try:
            data = client.recv(1024)
            if data.find('QUIT') != -1:
                break
            
            if randint(1,2) == 1:
                #alpha and the permutation Q
                pass
            else:
                #pi and the subgraph Q'
                pass
        
            msg = 'echoed:...{}'.format(data)
            client.send(msg)
        except:
            client.close()

s = socket.socket()
host = '127.0.0.1'
port = 44444
s.bind((host,port))

s.listen(5)

while True:
    try:
        client, addr = s.accept()
        print('Connected to {}'.format(addr))
        client.send('Welcome!')
        t = thread.start_new_thread(handler, (client, addr))
    except:
        break

