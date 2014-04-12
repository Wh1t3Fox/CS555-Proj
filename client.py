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
from matrix import bitCommit_HASH_SHA1_list_bo
from matrix import getRandMatrix
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

    g1 = Matrix('new', 5)
    g1.write_to_file('g1.txt') #this will be sent to Victor
    alpha = Matrix(len(g1))
    gprime = deepcopy(g1)
    gprime.permute(alpha)
    g2 = Matrix('new', 5) #this is only a placeholder, because
    #we need to create supergraph of gprime to get g2
    beta = Matrix(len(g2))
    q = deepcopy(g2)
    q.permute(beta)
    
    #Need to commit to Q here and create subgraph q'
    ret = bitCommit_HASH_SHA1_list_bo(q, 128)  # ret = [commitments, Random 1, Random 2] 
    commitment = [] # this is the actual commitment 
    commitment.append(ret[0])  # ret[0] is a matrix of  H(Random 1, Random 2, bit) values
    commitment.append(ret[2]) #ret[2] is the matrix of Random 2 's
    
    #send "committment" variable to commit
    #then later for verfifier to confirm commitment, send "ret" variable
    
    #Send the server committed Q
    q_data = ['q', q]
    txt = pickle.dumps(q_data)

    s.connect((host,port))

    s.send(txt)

    while True:
        try:

            data = s.recv(1024)
            print(data)
            print("")

            if data.find('INVALID LOGIN ATTEMPT') != -1:
                break
            elif data.find('SUCCESSFUL LOGIN') != -1:
                break

            raw_input("Press enter to continue...")

            if data.find('alpha and Graph Q') != -1:
                info = [1, alpha, q]
                msg = pickle.dumps(info)
                s.send(msg)

            elif data.find('pi and the subgraph') != -1:
                info = [2, 'pi', 'subgraph']
                msg = pickle.dumps(info)
                s.send(msg)

        except:
            break
            s.close
