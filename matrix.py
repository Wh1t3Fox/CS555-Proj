'''
CS555 Project
Zero-Knowledge Subgraph Isomorphism
Members:
    Craig West
    Max DeWees
    David Hersh
    Michael Kouremetis
'''
from random import randint
import os
import hashlib
from copy import deepcopy

class Matrix:

    """
    Initialize the matrix
    """
    def __init__(self, filename=None, size=None):
        self.matrix = []
        if isinstance(filename, int):
            self.create_matrix(filename)
        elif os.path.isfile(filename):
            self.create_from_file(filename)
        elif filename is 'empty':
            self.create_empty_matrix(size)

    """
    Returns a given row
    """
    def __getitem__(self, row):
        return self.matrix[row]

    """
    Define how we set a rows value.
    The value must be a list of strings
    """
    def __setitem__(self, row, values):
        self.matrix[row] = values

    """
    Return the size of the matrix in
    the number of rows
    """
    def __len__(self):
        return len(list(self.matrix))

    """
    Define how the object prints out
    """
    def __repr__(self):
        return '\n'.join([''.join(str(self.matrix[i])) for i in range(len(self.matrix))])

    """
    Creates a matrix, and adds random values
    """
    def create_matrix(self, size):
        #initialize matrix to 0
        for i in xrange(size):
            row = [0 for y in xrange(size)]
            self.matrix.append(row)
        for index, i in enumerate(self.matrix):
            for index2, j in enumerate(i):
                if j is 0:
                    r = randint(0, 1)
                    if r is 1:
                        self.matrix[index][index2] = r
                        self.matrix[index2][index] = r

    """
    Instead of filling with random values,
    fill with zeros
    """
    def create_empty_matrix(self, size):
        for i in xrange(size):
            row = [0 for y in xrange(size)]
            self.matrix.append(row)
  
    """
    Creates a supergraph, and returns top and bottom, which
    refer to the number of rows added to the top and bottom, respectively
    """
    def supergraph(self):
        top = randint(10, 20) #number of rows to be added to the top and
                              #number of elements to be added to the left of
                              #existing lists
        bottom = randint(10, 20) #number of rows to be added to the bottom and
                                 #number of elements to be added to the right of
                                 #existing lists
        newrowlength = len(self.matrix[0]) + top + bottom
        for i in self.matrix: #add elements to old graph rows to make them
                              #new size rows, and initialize to 0
            for x in xrange(top):
                i.insert(x, 0)
            for y in xrange(bottom):
                i.append(0)
        #initialize and add top and bottom rows
        for x in xrange(top):
            row = [0 for y in xrange(newrowlength)]
            self.matrix.insert(x, row)
        for x in xrange(bottom):
            row = [0 for y in xrange(newrowlength)]
            self.matrix.append(row)      
        #set vertex connections (i.e. ones) randomly in added rows,
        #and in newly added elements in old rows
        for x in xrange(top):
            for y in xrange(newrowlength):
                r = randint(0, 1)
                if r is 1:
                    self.matrix[x][y] = r
                    self.matrix[y][x] = r
        for x in xrange(bottom):
            for y in xrange(newrowlength):
                if self.matrix[newrowlength-x-1][y] is not 1:
                    r = randint(0, 1)
                    if r is 1:
                        self.matrix[newrowlength-x-1][y] = r
                        self.matrix[y][newrowlength-x-1] = r
        return top, bottom
       
    """
    Creates an isomorphic graph, returns the isomorphism function in
    dictionary form and the isomorphism graph as a new Matrix object
    """
    def isomorphism(self):
        orig_graph = matrix_to_dict(self)
        isofunction = {}
        new_graph = {}
        temp = range(len(self.matrix))
        #create isomorphism function by pairing each node
        #with a random node. these pairs are put in the dictionary
        #isofunction
        for i in xrange(len(self.matrix)):
            r = randint(0, len(temp)-1)
            isofunction[i] = temp.pop(r)
        #modify orig_graph values (NOT keys) by applying
        #the isomorphism
        for key, value in orig_graph.iteritems():
            for index, i in enumerate(value):
                orig_graph[key][index] = isofunction[i]
        #Apply the isomorphism to the keys in orig_graph,
        #storing the resulting full isomorphism in new_graph
        for key in orig_graph.iterkeys():
            new_graph[isofunction[key]] = orig_graph[key]
        new_matrix = dict_to_matrix(new_graph)
        return isofunction, new_matrix
        
    """
    Permute the current graph with the
    specified permutation matrix
    """
    def applyIsomorphism(self, isofunction):
        orig_graph = matrix_to_dict(self)
        new_graph = {}
        #modify orig_graph values (NOT keys) by applying
        #the isomorphism
        for key, value in orig_graph.iteritems():
            for index, i in enumerate(value):
                for key2 in isofunction.iterkeys():
                    if i is key2:
                        orig_graph[key][index] = isofunction[key2]
                        break
        #Apply the isomorphism to the keys in orig_graph,
        #storing the resulting full isomorphism in new_graph
        for key in orig_graph.iterkeys():
            new_graph[isofunction[key]] = orig_graph[key]
        new_matrix = dict_to_matrix(new_graph)
        return new_matrix

    """
    Creates a matrix from an adjacency matrix file
    """
    def create_from_file(self, filename):
        with open(filename, 'r') as fr:
            for line in fr:
                self.matrix.append([int(i) for i in line.split()])

    """
    Return the values of a given col.
    The input must be a number [0, N-1]
    """
    def get_col(self, col):
        return [i[col] for i in self.matrix]

    """
    Set the values of a given col.
    The input must be a list 
    """
    def set_col(self, col, values):
        for v,m in zip(values, self.matrix):
            m[col] = v

    """
    Check that the current matrix is equal to
    a given one.
    """
    def equals(self, matrix):
        for i in range(len(self.matrix)):
            if self.matrix[i] != matrix[i]:
                return False
        return True

    """
    Write the Matrix to a file
    """
    def write_to_file(self, filename):
        with open(filename, 'w') as fw:
            for i in self.matrix:
                for j in i:
                    if j is 1:
                        fw.write('1 ')
                    elif j is 0:
                        fw.write('0 ')
                    else:
                        fw.write('x ')
                fw.write('\n')

"""
Converts a matrix object into a dictionary
"""
def matrix_to_dict(m):
    graphdict = {}
    for index, i in enumerate(m):
        x = []
        for index2, j in enumerate(i):
            if j is 1:
                x.append(index2)
        graphdict[index] = x
    return graphdict

"""
Converts a dictionary into a matrix
"""
def dict_to_matrix(new_graph):
    new_matrix = Matrix('empty', len(new_graph))
    for key, value in new_graph.iteritems():
        for i in value:
            new_matrix[key][i]=1    
    return new_matrix
    
"""
Converts a dictionary into a matrix,
also fills with 'x' when node doesn't exist.
Used with subgraph Q prime
"""
def dict_to_matrix_x(new_graph, size):
    new_matrix = Matrix('empty', len(new_graph))
    for key, value in new_graph.iteritems():
        if not value:
            new_matrix.set_col(key, ['x' for y in range(size)])
            new_matrix[key] = ['x' for y in range(size)]
        else:
            for i in value:
                new_matrix[key][i]=1
    return new_matrix

"""
Creates Q Prime, given the Q Matrix, 
the isomorphism function between G2 and Q, and 
the number of nodes that were added between Q and 
Q Prime
"""
def qPrime(q, g2qiso, top, bottom):
    qp = matrix_to_dict(q)
    todelete = []
    for x in xrange(top):
        todelete.append(g2qiso[x])
    for x in xrange(bottom):
        todelete.append(g2qiso[len(g2qiso)-x-1])
    for key, value in qp.iteritems():
        qp[key] = [x for x in value if x not in todelete]
    for x in todelete:
        qp[x] = []
    return qp

"""
Given phi (isomorphism between G1 and G prime), 
alpha (isomorphism between G2 and Q), and the nodes that were added
between Q and Q prime, generate the pi isomorphism function
to give to the verifier
"""
def genPi(phi, alpha, top, bottom):
    phi = deepcopy(phi)
    alphaPrime = deepcopy(alpha)
    pi = {}
    for x in xrange(top):
        del alphaPrime[x]
    for x in xrange(bottom):
        del alphaPrime[len(alphaPrime)+top-1]
    for key in phi.iterkeys():
        phi[key] = phi[key] + top
    for key in phi.iterkeys():
        pi[key] = alphaPrime[phi[key]]
    return pi

"""
Takes G1 and pi as arguments, returns Q' for verifier to use
"""
def translate(dic, iso, size):
    copy = {}
    for v, k in iso.iteritems():
        copy[k] = dic[v]
    for k, v in copy.iteritems():
        copy[k] = sorted([iso[x] for x in v])
    l = range(size)
    for x in l:
        if x not in copy:
            copy[x] = []
    return copy
