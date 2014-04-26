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
import argparse
from matrix import *
from commitment import *
from copy import deepcopy

host = '127.0.0.1'
port = 44444
arguments = False

#Exit if using Python 3.x
if sys.version_info.major != 2:
    print('Must use python v2')
    sys.exit()

#Get the arguments from the command line
parser = argparse.ArgumentParser()
parser.add_argument('-g1','--graph1', help='Name of the adjacency matrix file for G1', required=False)
parser.add_argument('-g2','--graph2', help='Name of the adjacency matrix file for G2', required=False)
parser.add_argument('-s','--subgraph', help='Name of the adjacency matrix file for the subgraph', required=False)
parser.add_argument('-i','--isomorphism', help='Name of the adjacency matrix file for the isomorphism', required=False)
args = vars(parser.parse_args())

#If no arguments where supplied, generate our own graphs
if all(i is None for i in [v for k,v in args.iteritems()]):
    g1 = Matrix(5)
    #g1.write_to_file('g1.txt')

    phi, gprime = g1.isomorphism()

    g2 = deepcopy(gprime)
    top, bottom = g2.supergraph()
    #g2.write_to_file('g2.txt')

#Use the paramaters given for the protocol
elif all(i is not None for i in [v for k,v in args.iteritems()]):
    arguments = True
    #Need to finish this section here
    g1 = Matrix(args['graph1'])
    #g1.write_to_file('g1.txt')

    gprime = Matrix(args['subgraph'])
    phi = matrix_to_dict(Matrix(args['isomorphism']))

    g2 = Matrix(args['graph2'])
    #g2.write_to_file('g2.txt')

#If G1 and G2 were given but not all the arguments exit
elif not all(i is None for i in [args['graph1'], args['graph2']]):
    print('NP-Hard Problem You Will NOT Succeed....Good Luck....')
    sys.exit(1)
#Exit if there are not enough parameters
else:
    print('[-] NOT ENOUGH PARAMETERS')
    sys.exit(1)

#Create the socket and connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

#This represents each round of the protocol
while True:
    try:
        #Create the isomorphism alpha and the graph Q
        #this whole thing needs to be changed
        alpha, q = g2.isomorphism()
        pi = genPi(phi, alpha, top, bottom)
        qPr = qPrime(q, phi, alpha, top, bottom)
        qPrM = dict_to_matrix_x(qPr, len(q))
        
        #Need to commit to Q here and create subgraph q'
        #Create a commitment of the graph Q#
        ret = bitCommit_HASH_SHA1_list_bo(q, 128)  # ret = [commitments, Random 1, Random 2]
        commitment = [] # this is the actual commitment
        commitment.append(ret[0])  # ret[0] is a matrix of  H(Random 1, Random 2, bit) values
        commitment.append(ret[2])  # ret[2] is the matrix of Random 2 's

        #Send the server committed Q, g1, and g2
        q_data = ['q', commitment, g1, g2]
        txt = pickle.dumps(q_data)
        s.sendall(txt)
        s.sendall("THE END")

        #Get data from the server
        r = s.recv(1024).split('\n')
        data = r[len(r)-2]
        print(data)
        print("")

        #Exit if the protocol fails or succeeds
        if data.find('INVALID LOGIN ATTEMPT') != -1:
            break
        elif data.find('SUCCESSFUL LOGIN') != -1:
            break

        #Just a pause between each round
        raw_input("Press enter to continue...")

        #Send the server alpha and Q
        if data.find('alpha and Graph Q') != -1:
           #for verification send ret[1] so the server can then check the commitment
           info = [1, alpha, q, ret[1]]
           msg = pickle.dumps(info)
           s.sendall(msg)
           s.sendall("THE END")

       #Send the server pi and Q'
        elif data.find('pi and the subgraph') != -1:
            info = [2, pi, qPrM, ret[1]]
            msg = pickle.dumps(info)
            s.sendall(msg)
            s.sendall("THE END")

    #Print out any errors
    except Exception as e:
        print(str(e))
        break
        s.close
