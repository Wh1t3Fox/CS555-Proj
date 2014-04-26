#!/usr/bin/env python

##import sys
##import socket
##import pickle
##import random
from matrix import *
##from commitment import *
from copy import deepcopy
##import hashlib

def genQprime(phi, alpha, top, bottom):
    phi = deepcopy(phi)
    #alpha = deepcopy(alpha)
    alphaPrime = deepcopy(alpha)
    qPrime = {}
    for x in xrange(top):
        del alphaPrime[x]
    for x in xrange(bottom):
        del alphaPrime[len(alphaPrime)+top-1]
    for key in phi.iterkeys():
        phi[key] = phi[key] + top
    for key in phi.iterkeys():
        qPrime[key] = alphaPrime[phi[key]]
    # right now, have dictionary representation
    # of q prime, need to create matrix
    return qPrime

g1 = Matrix(250)
g1.write_to_file('g1-300.txt')
phi, gprime = g1.isomorphism()
gprime.write_to_file('gprime-300.txt')
g2 = deepcopy(gprime)
top, bottom = g2.supergraph()
g2.write_to_file('g2-300.txt')

alpha, q = g2.isomorphism()
q.write_to_file('q-300.txt')
pi = genQprime(phi, alpha, top, bottom)

g1dic = matrix_to_dict(g1)

print "g1"
#print g1
print ""

print "G prime"
#print gprime
print ""

print "phi"
#print phi
print ""

print "G2"
#print g2
print ""

print "alpha"
#print alpha
print ""

print "q"
#print q
print ""


qP = translate(g1dic, pi, len(g2))

print "Q prime, from G1"
qPm = dict_to_matrix_x(qP, len(g2))
qPm.write_to_file('qPrime-g1.txt')
#print qPm
print ""

print "Q prime, from Q"
qPr = qPrime(q, phi, alpha, top, bottom)
qPrM = dict_to_matrix_x(qPr, len(q))
qPrM.write_to_file('qPrime-q.txt')
#print qPrM

print "Q prime dictionary, from G1"
print qP
print ""

print "Q prime dictionary, from Q"
print qPr
print ""

print "Are the two Q Primes the same?"
print qPm.equals(qPrM)

print "Are the two Q prime dictionaries the same?"
print (qP == qPr)


##g1 = Matrix(3)
##phi, gprime = g1.isomorphism()
##
##g2 = deepcopy(gprime)
##top, bottom = g2.supergraph()
##
##alpha, q = g2.isomorphism()
##pi = genQprime(phi, alpha, top, bottom)
##
##print "g1"
##print g1
##print ""
##
##print "G prime"
##print gprime
##print ""
##
##print "phi"
##print phi
##print ""
##
##print "G2"
##print g2
##print ""
##
##print "alpha"
##print alpha
##print ""
##
##print "q"
##print q
##print ""

##q_again = g2.applyIsomorphism(alpha)
##print "q equals q", q.equals(q_again)
##
##print "pi (potentially)"
##print pi
##print ""
##
##gP = g1.applySubIsomorphism(pi, len(g2))
##print gP

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
