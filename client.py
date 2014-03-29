#!/usr/bin/env python

import socket
import pickle
from matrix import Matrix
from random import randint
from graph_tool.all import *


s = socket.socket()
host = '127.0.0.1'
port = 44444
alpha = None
pi = None
num_rounds = 0

#Create a permutation matrix file
def create_permutation(filename, size):
    s = set()
    tmp = []
    while len(set(tmp)) != size:
        tmp.append(randint(0, size-1))
    order = [x for x in tmp if x not in s and not s.add(x)]
    with open(filename, 'w') as fw:
        for  i in range(size):
            for j in range(size):
                if order[i] == j:
                    fw.write('1 ')
                else:
                    fw.write('0 ')
            fw.write('\n')

#Create a matrix file from a graph
def create_matrix(filename, graph):
    with open(filename, 'w') as fw:
        for i in range(graph.num_vertices()):
            for j in range(graph.num_vertices()):
                if graph.edge(i, j):
                    fw.write('1 ')
                else:
                    fw.write('0 ')
            fw.write('\n')

#Create a graph from a matrix
def create_graph(matrix, graph):
    graph.add_vertex(len(matrix))
    for line, row in enumerate(matrix):
        for pos, item in enumerate(row):
            if item == str(1) and not graph.edge(pos, line):
                graph.add_edge(line, pos)
                
                
                

if __name__ == '__main__':
    s.connect((host,port))

    m = Matrix('g2.txt')
    info = ['q', m]
    txt = pickle.dumps(info)
    s.send(txt)
    while True:
        try:
            if num_rounds == 100:
                break
                
            data = s.recv(1024)
            print data    
            
            raw_input("Press enter to continue...")
            
            if data.find('alpha and Graph Q') != -1:
                info = [1, 'a', 'q'] 
                
            elif data.find('pi and the subgraph') != -1:
                info = [2, 'pi', 'subgraph']
                
            msg = pickle.dumps(info)            
            s.send(msg)
            
            num_rounds += 1
        except:
            break
            s.close
