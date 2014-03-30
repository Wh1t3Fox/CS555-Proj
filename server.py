#!/usr/bin/env python2
'''
CS555 Project
Zero-Knowledge Subgraph Isomorphism
Members:
    Craig West
    Max DeWees
    David Hersh
    Michael Kouremetis
'''

import sys
import socket
import pickle
from matrix import Matrix
from random import randint
from copy import deepcopy
import threading

g1 = Matrix('g1.txt')
g2 = Matrix('g2.txt')
committed_q = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 44444

t = None

def handler(client):
    num_rounds = 0
    while True:
        try:

            data = client.recv(1024)
            if not data:
                break

            lst = pickle.loads(data)

            if lst[0] == 'q':
                global committed_q
                committed_q = lst[1]

            elif lst[0] == 1:
                #insert checking committed q here
                alpha, q = lst[1], lst[2]
                m = deepcopy(g2)
                m.permute(alpha)
                if not m.equals(q):
                    client.send("INVALID LOGIN ATTEMPT")
                    break

            elif lst[0] == 2:
                print(lst)
                #insert checking committed q here
                #pi, subgraph = lst[1], lst[2]
                #m = deepcopy(g1)
                #m.permute(pi)
                #if not m.equals(subgraph):
                #   client.send("INVALID LOGIN ATTEMPT")
                #   break

            if randint(1,2) == 1:
                #alpha and the permutation Q
                msg = 'Please send alpha and Graph Q'
            else:
                #pi and the subgraph Q'
                msg = 'Please send pi and the subgraph'

            if num_rounds == 100:
                client.send("SUCCESSFUL LOGIN")
                break

            client.send(msg)
            num_rounds += 1

        except:
            client.close()

if __name__ == '__main__':
    if sys.version_info.major != 2:
        print('Must use python v2')
        sys.exit()

    s.bind((host,port))
    s.listen(5)

    while True:
        try:
            client, addr = s.accept()
            print('Connected to {}'.format(addr))
            client.send('Please Login!')
            t = threading.Thread(target=handler, args=[client])
            t.start()
        except:
            break

