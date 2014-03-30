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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 44444

#Create a permutation matrix file
def create_permutation(filename, size):
    s = set()
    tmp = []
    while len(set(tmp)) != size:
        tmp.append(randint(0, size-1))
    order = [x for x in tmp if x not in s and not s.add(x)]
    with open(filename, 'w') as fw:
        for i in range(size):
            for j in range(size):
                if order[i] == j:
                    fw.write('1 ')
                else:
                    fw.write('0 ')
            fw.write('\n')

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

    g1 = Matrix('g1.txt')
    g2 = Matrix('g2.txt')
    create_permutation('alpha.txt', len(g2))
    alpha = Matrix('alpha.txt')
    q = deepcopy(g2)
    q.permute(alpha)
    #Need to commit to Q here and create subgraph q'

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
