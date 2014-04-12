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
    Creates a matrix
    """
    def create_matrix(self, size):
        for i in range(size):
            row = [0 for y in range(size)]
            self.matrix.append(row)
        for index, i in enumerate(self.matrix):
            for index2, j in enumerate(i):
                if j is 0:
                    r = randint(0, 1)
                    if r is 1:
                        self.matrix[index][index2] = r
                        self.matrix[index2][index] = r

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
    The input must be a list of strings
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
                        fw.write('1 ')
                    else:
                        fw.write('0 ')
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
                    r.append('1')
                else:
                    r.append('0')
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



'''
parameters: random1List = 2D list of random values in int/string values - use random.getrandbits() as uses mersenne twister
            random2List = 2D list of random values in int/string values - use random.getrandbits() as uses mersenne twister
            bitList = 2D list of bits in int/string values aka the matrix
'''            
    def bitCommit_HASH_SHA1_list( random1List, random2List, bitList ):
        commitments = []
        for idx, row in enumerate(bitList):  #iterating through row of matrix
            rowOut=[]
            for idx1, val in enumerate(row): #iterating through col of matrix
                rowOut.append(hashlib.sha1(str(random1List[idx][idx1]) + str(random2List[idx][idx1]) + str(bitList[idx][idx1])).hexdigest())
            commitments.append(rowOut) 
        return commitments
        
'''
Commitment function follows the scheme: H(Random-1, Random-2, Bit), Random-2
This function is a non-interactive scheme, Alice creates both randoms, does not wait for Bob to send randoms
parameters:  bitList = 2D list of bits in int/string values
             randSize = in bits, the size of the random values used for the committment
Note: the Matrix passed must be of form row size = column size ; or else function will blow up
'''
    def bitCommit_HASH_SHA1_list_bo(bitList, randSize):
        randMatrix1= getRandMatrix(len(bitList), randSize)
        randMatrix2=getRandMatrix(len(bitList), randSize)
        commitments = []
        for idx, row in enumerate(bitList):  #iterating through row of matrix
            rowOut=[]
            for idx1, val in enumerate(row): #iterating through col of matrix
                rowOut.append(hashlib.sha1(str(randMatrix1[idx][idx1]) + str(randMatrix2[idx][idx1]) + str(val)).hexdigest())
            commitments.append(rowOut) 
        out = []
        out.append(commitments)
        out.append(randMatrix1)
        out.append(randMatrix2)
        return out    # returns [commitments, 1st set of randoms, 2nd set of randoms] - a bit commit to send would be
                      # [commitments, 1st set of randoms]  OR [commitments, 2nd set of randoms]
    
        
'''
returns a 2D matrix of random value for the bit committment, this function is called by bitCommit_HASH_SHA1_list_bo()
parameters: size = row size(or column size) or matrix will be commiting to
            randValueSize = the size(in bits) of the random values used in the committment
'''
    def getRandMatrix(size, randValueSize):
        random.seed() #getting the random generator going
        rand= []
        for i in range(size):
            row = []
            for j in range(size):
                row. append(str(random.getrandbits(randValueSize))) 
            rand.append(row)
        return rand




