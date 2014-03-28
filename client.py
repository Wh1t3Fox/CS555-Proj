#!/usr/bin/env python

import socket
import pickle
from matrix import Matrix
from graph_tool.all import *


s = socket.socket()
host = '127.0.0.1'
port = 44444
alpha = None
pi = None
num_rounds = 0


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
