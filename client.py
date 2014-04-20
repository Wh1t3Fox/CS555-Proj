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

#DFS on an adjacency matrix
def dfs(matrix, start_node):
    graph = {}
    stack = []
    visited = set()

    for line,row in enumerate(matrix):
        for col,value in enumerate(row):
            try:
                graph[line]
                if value == '1':
                    graph[line].append(col)
            except:
                graph[line] = []

    visited.add(start_node)
    stack.append(start_node)
    while len(stack) > 0:
        current = stack.pop()
        print current,
        for c_node in graph[current]:
            if c_node not in visited:
                stack.append(c_node)
                visited.add(c_node)



if __name__ == '__main__':
    if sys.version_info.major != 2:
        print('Must use python v2')
        sys.exit()
    
    s.connect((host,port))
    
    g1 = Matrix('new',5)
            
    gprime = deepcopy(g1)
    beta = Matrix(len(g1))
    gprime.permute(beta)
            
    g2 = Matrix('new',5) #temporary placeholder
    
    while True:
        try:
            alpha = Matrix(len(g2))
            q = deepcopy(g2)
            q.permute(alpha)
     
            #Need to commit to Q here and create subgraph q'
            ret = bitCommit_HASH_SHA1_list_bo(q, 128)  # ret = [commitments, Random 1, Random 2] 
            commitment = [] # this is the actual commitment 
            commitment.append(ret[0])  # ret[0] is a matrix of  H(Random 1, Random 2, bit) values
            commitment.append(ret[2])  # ret[2] is the matrix of Random 2 's
        
            #Send the server committed Q and g1, g2
            q_data = ['q', commitment, g1, g2]
            txt = pickle.dumps(q_data)
            s.send(txt)

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
                s.send(msg)

            elif data.find('pi and the subgraph') != -1:
                info = [2, 'pi', 'subgraph']
                msg = pickle.dumps(info)
                s.send(msg)

        except Exception,e:
            print str(e)
            break
            s.close
