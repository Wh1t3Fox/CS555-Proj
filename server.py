#!/usr/bin/env python

import socket
from matrix import Matrix
from random import randint

s = socket.socket()
host = '127.0.0.1'
port = 44444
s.bind((host,port))

s.listen(5)

while True:
    client, addr = s.accept()
    print('Connected to {}'.format(addr))
    client.send('Welcome!')

    if randint(1,2) == 2:
        #alpha and the permutation Q
        pass
    else:
        #pi and the subgraph Q'
        pass

    client.close()
