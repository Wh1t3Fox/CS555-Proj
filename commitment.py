import random
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
    parameters:  bitList = 2D list of bits in int/string values, aka the matrix
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




