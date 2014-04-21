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
import hashlib
from commitment import *
from matrix import Matrix
from random import randint
from copy import deepcopy
import threading


g1 = None
g2 = None
committed_q = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 44444

def read_data(sock, buffer_size=4096):
    buff = ''
    while True:
        data = sock.recv(buffer_size)
        if data.endswith("THE END"):
            buff += data[:-7]
            break
        else:
            buff += data
    return buff

def validate_q(q, rands):
    for i in xrange(len(q)):
        for j in xrange(len(q)):
            if not hashlib.sha1(rands[i][j] + committed_q[1][i][j] + str(q[i][j])).hexdigest() == committed_q[0][i][j]:
                return False

def handler(client):
    num_rounds = 0
    while True:
        try:            
            data = read_data(client)
            if not data:
                break
           
            lst = pickle.loads(data)
            
            if lst[0] == 'q':
                global g1
                global g2
                global committed_q
                committed_q, g1, g2= lst[1], lst[2], lst[3]
                num_rounds -= 1

            elif lst[0] == 1:
                alpha, q, rand_val = lst[1], lst[2], lst[3]
                if validate_q(q, rand_val):
                    client.sendall("COMITTED Q DOES NOT MATCH\n")
                    break
                m = deepcopy(g2)
                m.permute(alpha)
                if not m.equals(q):
                    client.sendall("INVALID LOGIN ATTEMPT\n")
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
            
            if num_rounds == 7:
                client.sendall("SUCCESSFUL LOGIN\n")
                client.close()
                break
            else:
                if randint(1,2) == 1:
                    #alpha and the permutation Q
                    msg = 'Please send alpha and Graph Q\n'
                    num_rounds += 1
                else:
                    #pi and the subgraph Q'
                    msg = 'Please send pi and the subgraph\n'
                    num_rounds += 1
                
            client.sendall(msg)
        except Exception,e:
            client.close()
            print str(e)
            break

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
            t = threading.Thread(target=handler, args=[client])
            t.start()
        except:
            break

