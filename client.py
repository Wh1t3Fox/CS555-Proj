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
import random
import time
from matrix import Matrix
from commitment import *
from copy import deepcopy

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 44444

if sys.version_info.major != 2:
    print('Must use python v2')
    sys.exit()

s.connect((host,port))

g1 = Matrix('new',5)
g1.write_to_file('g1.txt')

isofunction, gprime = g1.isomorphism()

g2 = deepcopy(gprime)
g2.create_supergraph()
g2.write_to_file('g2.txt')

while True:
    try:
        #this whole thing needs to be changed
        alpha = Matrix(len(g2))
        q = deepcopy(g2)
        q.permute(alpha)

        #Need to commit to Q here and create subgraph q'
        ret = bitCommit_HASH_SHA1_list_bo(q, 128)  # ret = [commitments, Random 1, Random 2]
        commitment = [] # this is the actual commitment
        commitment.append(ret[0])  # ret[0] is a matrix of  H(Random 1, Random 2, bit) values
        commitment.append(ret[2])  # ret[2] is the matrix of Random 2 's

        #Send the server committed Q, g1, and g2
        q_data = ['q', commitment, g1, g2]
        txt = pickle.dumps(q_data)
        s.sendall(txt)
        s.sendall("THE END")

        r = s.recv(1024).split('\n')
        data = r[len(r)-2]
        print(data)
        print("")

        if data.find('INVALID LOGIN ATTEMPT') != -1:
            break
        elif data.find('SUCCESSFUL LOGIN') != -1:
            break

        raw_input("Press enter to continue...")

        if data.find('alpha and Graph Q') != -1:
           #for verification send ret[1] so the server can then check the commitment
           info = [1, alpha, q, ret[1]]
           msg = pickle.dumps(info)
           s.sendall(msg)
           s.sendall("THE END")

        elif data.find('pi and the subgraph') != -1:
            info = [2, 'pi', 'subgraph']
            msg = pickle.dumps(info)
            s.sendall(msg)
            s.sendall("THE END")

    except Exception as e:
        print(str(e))
        break
        s.close
