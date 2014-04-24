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
from copy import deepcopy #this is only here for testing

class Matrix:

    """
    Initalize the matrix
    """
    def __init__(self, filename=None, size=None):
        self.matrix = []
        if isinstance(filename, int):
            self.create_permutation(filename)
        elif os.path.isfile(filename):
            self.create_from_file(filename)
        elif filename is 'empty':
            self.create_empty_matrix(size)
        else: #this method of calling create_matrix is ugly, but works
            self.create_matrix(size)

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

    def create_empty_matrix(self, size):
        for i in xrange(size):
            row = [0 for y in xrange(size)]
            self.matrix.append(row)
            
    """
    Creates a supergraph
    NEEDS TO BE MODIFIED TO RETURN TOP AND BOTTOM
    """

    def create_supergraph(self):
        top = randint(1, 2) #number of rows to be added to the top and
                            #number of elements to be added to the front of
                            #existing lists
        bottom = randint(1, 2) #number of rows to be added to the bottom and
                               #number of elements to be added to the back of
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
        
    """
    Creates an isomorphic graph, returns the isomorphism function in
    dictionary form and the isomorphism graph as a new Matrix object
    """
    def isomorphism(self):
        orig_graph = {}
        isofunction = {}
        new_graph = {}
        temp = range(len(self.matrix))
        #fill orig_graph dictionary with nodes as keys and
        #lists of the nodes they are connected to as the values
        for index, i in enumerate(self.matrix):
            x = []
            for index2, j in enumerate(i):
                if j is 1:
                    x.append(index2)
            orig_graph[index] = x
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
                for key2 in isofunction.iterkeys():
                    if i is key2:
                        orig_graph[key][index] = isofunction[key2]
                        break
        #Apply the isomorphism to the keys in orig_graph,
        #storing the resulting full isomorphism in new_graph
        for key in orig_graph.iterkeys():
            for key2 in isofunction.iterkeys():
                if key is key2:
                    new_graph[isofunction[key2]] = orig_graph[key]
                    break
        #Turn new_graph dictionary into Matrix object, and
        #return the new matrix
        new_matrix = Matrix('empty', len(self.matrix))
        for key, value in new_graph.iteritems():
            for i in value:
                new_matrix[key][i]=1
        return isofunction, new_matrix
    
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
    Rotate the current matrix 90 degrees CW
    """
    def rotate_cw(self):
        self.matrix = [self.get_col(i)[::-1] for i in range(len(self.matrix))]

    """
    Rotate the current matrix 90 degrees CCW
    """
    def rotate_ccw(self):
        self.matrix = [self.get_col(i) for i in range(len(self.matrix)-1, -1, -1)]

    """
    Rotate the current matrix 180 degrees
    """
    def rotate_180(self):
        self.matrix = [i[::-1] for i in self.matrix[::-1]]

    """
    Permute the currect graph with the
    specified permutation matrix
    """
    def permute(self, matrix):
        order = [pos for row in matrix for pos,item in enumerate(row) if item is 1]
        tmp = self.matrix
        self.matrix = [tmp[i] for i in order]

    """
    Create matrix file that is the permutation
    between the current matrix and a given matrix
    """
    def get_permutation(self, matrix, filename):
        order = [pos for i in self.matrix for pos,j in enumerate(matrix) if i == j]
        with open(filename, 'w') as fw:
            for i in range(size):
                for j in range(size):
                    if order[i] == j:
                        fw.write(1)
                    else:
                        fw.write(0)
                fw.write('\n')

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
    Create a permutation matrix
    """
    def create_permutation(self, size):
        s = set()
        t = []
        while len(set(t)) != size:
            t.append(randint(0, size-1))
        order = [x for x in t if x not in s and not s.add(x)]
        for i in range(size):
            r = []
            for j in range(size):
                if order[i] == j:
                    r.append(1)
                else:
                    r.append(0)
            self.matrix.append(r)
    """
    Write the Matrix to a file
    """
    def write_to_file(self, filename):
        with open(filename, 'w') as fw:
            for i in self.matrix:
                for j in i:
                    if j is 1:
                        fw.write('1 ')
                    else:
                        fw.write('0 ')
                fw.write('\n')

