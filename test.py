#!/usr/bin/env python

##import sys
##import socket
##import pickle
##import random
from matrix import *
##from commitment import *
from copy import deepcopy
##import hashlib



g1 = Matrix(103)
#g1.write_to_file('g1-300.txt')
phi, gprime = g1.isomorphism()
#gprime.write_to_file('gprime-300.txt')
g2 = deepcopy(gprime)
top, bottom = g2.supergraph()
#g2.write_to_file('g2-300.txt')

alpha, q = g2.isomorphism()
#q.write_to_file('q-300.txt')
pi = genPi(phi, alpha, top, bottom)

g1dic = matrix_to_dict(g1)
qP = translate(g1dic, pi, len(g2))


qPm = dict_to_matrix_x(qP, len(g2))
#qPm.write_to_file('qPrime-g1.txt')

qPr = qPrime(q, phi, alpha, top, bottom)
qPrM = dict_to_matrix_x(qPr, len(q))
for col, y in enumerate(qPrM[0]):
    if y is 'x':
        qPrM.set_col(col, ['x' for y in range(len(qPrM))])
        
#print "g1"
#print g1
#print ""

#print "G prime"
#print gprime
#print ""

#print "phi"
#print phi
#print ""

#print "G2"
#print g2
#print ""

#print "alpha"
#print alpha
#print ""

#print "q"
#print q
#print ""

#print "Q prime, from G1"
#print qPm
#print ""

#print "Qprime, from Q"
#print qPrM
#print ""

#print "Q prime dictionary, from G1"
#print qP
#print ""

#print "Q prime dictionary, from Q"
#print qPr
#print ""

print "Are the two Q Primes the same?"
print qPm.equals(qPrM)

print "Are the two Q prime dictionaries the same?"
print (qP == qPr)
