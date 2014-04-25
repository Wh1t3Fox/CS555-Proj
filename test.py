#!/usr/bin/env python

##import sys
##import socket
##import pickle
##import random
from matrix import Matrix
##from commitment import *
from copy import deepcopy
##import hashlib

g1 = Matrix(5)
phi, gprime = g1.isomorphism()

g2 = deepcopy(gprime)
top, bottom = g2.supergraph()

print phi


##g1 = Matrix('new', 5)
##g1.write_to_file('g1.txt') #this will be sent to Victor
##alpha = Matrix(len(g1))
##gprime = deepcopy(g1)
##gprime.permute(alpha)
##
##g2 = Matrix('new', 5) #this is only a placeholder, because
###we need to create supergraph of gprime to get g2
##beta = Matrix(len(g2))
##q = deepcopy(g2)
##q.permute(beta)    
##
##
###Need to commit to Q here and create subgraph q'
##ret = bitCommit_HASH_SHA1_list_bo(q, 128)  # ret = [commitments, Random 1, Random 2] 
##commitment = [] # this is the actual commitment 
##commitment.append(ret[0])  # ret[0] is a matrix of  H(Random 1, Random 2, bit) values
##commitment.append(ret[2]) #ret[2] is the matrix of Random 2 's
##    
###send "committment" variable to commit
###then later for verfifier to confirm commitment, send "ret" variable
##
##print ret[0][0][0]
##print ""
##print ret[1][0][0]
##print ""
##print ret[2][0][0]
##print ""
##
##print hashlib.sha1(ret[1][0][0] +ret[2][0][0] + str(q[0][0])).hexdigest()
##
##for i,j in zip(commitment[1], ret[2]):
##    print i == j
##print ""
##
##for i in xrange(len(q)):
##    for j in xrange(len(q)):
##       print hashlib.sha1(ret[1][i][j] + commitment[1][i][j] + str(q[i][j])).hexdigest() == commitment[0][i][j]
##    
##   
