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
import time
from commitment import *
from matrix import *
from random import randint
from copy import deepcopy
import threading


g1 = None
g2 = None
committed_q = None

#Create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 44444

#Read data from the client until the end of the byte stream
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

#Validate the commitment of Q
def validate_q(q, rands):
    for i in xrange(len(q)):
        for j in xrange(len(q)):
            if q[i][j] == 'x':
                pass
            elif not hashlib.sha1(rands[i][j] + committed_q[1][i][j] + str(q[i][j])).hexdigest() == committed_q[0][i][j]:
                return False

#Handler for the thread
def handler(client):
    num_rounds = 1
    while True:
        try:
            #Store the data received
            data = read_data(client)
            #if there is no data exit
            if not data:
                break

            #Conver the byte stream back into a list
            lst = pickle.loads(data)

            #If we are receiving q save the commitment
            #also store G1 and G2
            if lst[0] == 'q':
                global g1
                global g2
                global committed_q
                committed_q, g1, g2= lst[1], lst[2], lst[3]
                num_rounds -= 1

            #If receiving alpha and Q
            #store the values of alpha, q, and the random values to validate the commitment
            elif lst[0] == 1:
                print("RECEIVED ALPHA")
                alpha, q, rand_val = lst[1], lst[2], lst[3]
                #validate the graph q with the commitment
                if validate_q(q, rand_val):
                    client.sendall("COMITTED Q DOES NOT MATCH\n")
                    break
                m = deepcopy(g2)
                new_q = m.applyIsomorphism(alpha)
                #check to make sure g2 + alpha = Q
                if not new_q.equals(q):
                    client.sendall("INVALID LOGIN ATTEMPT\n")
                    break

            #If receiving pi and Q'
            elif lst[0] == 2:
                print("RECEIVED PI")
                pi, subgraph, rand_val = lst[1], lst[2], lst[3]
                g1dic = matrix_to_dict(g1)
                qP = translate(g1dic, pi, len(g2))
                qPm = dict_to_matrix_x(qP, len(g2))
                if validate_q(subgraph, rand_val):
                    client.sendall("COMITTED Q DOES NOT MATCH\n")
                    break
                if not qPm.equals(subgraph):
                   client.send("INVALID LOGIN ATTEMPT")
                   break

            #After x num of successful rounds exit
            if num_rounds >= 7:
                print("LOGGED IN")
                client.sendall("SUCCESSFUL LOGIN\n")
                time.sleep(2)
                client.close()
                break
            else:
                #Randomly request either, alpha and Q or pi and Q'
                if randint(1,2) == 1:
                    #alpha and the permutation Q
                    msg = 'Please send alpha and Graph Q\n'
                else:
                    #pi and the subgraph Q'
                    msg = 'Please send pi and the subgraph\n'
                num_rounds += 1

            #send the information to the server
            client.sendall(msg)

        #print out any error
        except Exception as e:
            client.close()
            print(str(e))
            break

if __name__ == '__main__':
    #Exit if using Python 3.x
    if sys.version_info.major != 2:
        print('Must use python v2')
        sys.exit()

    #Create a socket listener
    s.bind((host,port))
    s.listen(5)


    while True:
        try:
            client, addr = s.accept()
            print('Connected to {}'.format(addr))

            #Create a thread for each user that connects
            t = threading.Thread(target=handler, args=[client])
            t.start()
        except:
            break

