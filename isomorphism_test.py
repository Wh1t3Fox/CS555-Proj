import random
from matrix import Matrix

def createMatrixListFromFile(fileName):
	l = [] # original matrix as a 2-d list
	with open(fileName, 'r') as f:
		for line in f:
			line = line.rstrip()
			row = line.split(" ")
			l.append(row)
		return l
		
def createStrList(matrix):
	strList = " " # important that this starts with leading whitespace
	for valx, x in enumerate(matrix):
		for valy, y in enumerate(x):
			if(y=='1'):
				strValx = str(valx+1)
				strValy = str(valy+1)
				strList += strValx + " " + strValy + " "
	return strList

def genPermutationList(matrix):
	indices = [] # a list of the numbers to randomly generate the isomorphism
	maximum = len(matrix)
	while(maximum > len(indices)):
		o = random.randint(1, maximum)
		o = o % (maximum + 1)
		if(o not in indices):
			indices.append(o)
	return indices
	
def transformStrList(matrix, strList):
	tempMax = len(matrix)+1
	m = 0
	while(m <= len(matrix)):
		if(m==0):
			a = " " + str(indices.pop()) + " "
			b = " " + str(tempMax) + " "
			strList=strList.replace(a, b)	
		elif(m==len(matrix)):
			b = a
			a = " " + str(tempMax) + " "
			strList=strList.replace(a, b)
		else:
			b = a
			a = " " + str(indices.pop()) + " "
			strList=strList.replace(a, b)
		m=m+1
	return strList
	
def createPermutationMatrix(strList, matrix):
	newMatrix = []
	for a in range(0, len(matrix)):
		temprow = []
		for b in range(0, len(matrix)):
			temprow.append('0')
		newMatrix.append(temprow)
	last = 0
	while(len(strList)>1):
		first = -1
		first = strList.find(" ", first+1)
		last = strList.find(" ", first+1)
		i = strList[first:last]
		i = int(i) - 1
		first = last
		last = strList.find(" ", first+1)
		j = strList[first:last]
		j = int(j) - 1
		newMatrix[i][j] = '1'
		strList = strList[last:]
	return newMatrix
	
def writeNewMatrix(newMatrix, fileName):
	f = open(fileName, 'w').close() # clear the old file
	f = open(fileName, 'a')

	for a in newMatrix:
		for b in a:
			f.write(b + " ")
		f.write("\n")
	f.close()
	
def createSupergraph(matrix, levels):
	for x in matrix:
		for y in range(0, levels):
			x.insert(0, '0')

	row = []
	for x in range(0, len(matrix[-1])):
		row.append('0')
	
	for x in range(0, levels):
		matrix.insert(0, row)

	#generate random adjacencies
	p = random.randint(3, len(matrix[-1]))
	for x in range (0, p):
		i = random.randint(1, 100)
		i = i % levels
		j = random.randint(1, 100)
		j = j % len(matrix[-1])
		#print "i", i
		#print "j", j
		#matrix[i][j] = '1'
		#matrix[j][i] = '1'
	
	return matrix 
	
g1 = Matrix("filename", 90) #creates g1 of size 90
g1fn = "g1-90.txt"
g1.write_to_file(g1fn)
originalMatrix = createMatrixListFromFile(g1fn)
strList = createStrList(originalMatrix) #strList is a long string of each node and its connections
indices = genPermutationList(originalMatrix) #indices is now a random permutation of numbers 1 through n
strList = transformStrList(originalMatrix, strList)

# the isomorphism has now been applied to strList
# now the new matrix needs to be created 
newMatrix = createPermutationMatrix(strList, originalMatrix)
# and written to file
writeNewMatrix(newMatrix, "gprime-90.txt")
#create supergraph g2 from gprime
levels = random.randint(10, 20)
g2 = createSupergraph(newMatrix, levels)
writeNewMatrix(g2, "g2-90.txt")