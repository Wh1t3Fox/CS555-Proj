#!/usr/bin/env python

import socket
import pickle
from matrix import Matrix
from random import randint
from copy import deepcopy
from graph_tool.all import *


s = socket.socket()
host = '127.0.0.1'
port = 44444
num_rounds = 0

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
                

if __name__ == '__main__':

    g1 = Matrix('g1.txt')   
    g2 = Matrix('g2.txt')
    create_permutation('alpha.txt', len(q2))
    alpha = Matrix('alpha.txt')
    q = deepcopy(g2)
    q.permute(alpha)
    #Need to commit to Q here and create subgraph q'
    
    
    s.connect((host,port))

    #Send the server committed Q
    q_data = ['q', q]
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
                info = [1, alpha, q] 
                
            elif data.find('pi and the subgraph') != -1:
                info = [2, 'pi', 'subgraph']
                
            msg = pickle.dumps(info)            
            s.send(msg)
            
            num_rounds += 1
        except:
            break
            s.close
