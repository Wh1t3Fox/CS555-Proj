#!/usr/bin/env python

import socket
import pickle
from matrix import Matrix
from random import randint
import thread

g1 = Matrix('g1.txt')
g2 = Matrix('g2.txt')

def handler(client, addr):
    while True:
        try:
            data = client.recv(1024)
            matrix = pickle.loads(data)
            if randint(1,2) == 1:
                #alpha and the permutation Q
                msg = 'Please send alpha and Graph Q'
            else:
                #pi and the subgraph Q'
                msg = 'Please send pi and the subgraph'
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

