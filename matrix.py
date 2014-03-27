
class Matrix:

    def __init__(self, filename):
        self.matrix = []
        self.create_from_file(filename)

        #self.matrix = [['0' for i in xrange(cols)] for j in xrange(rows)]

    def create_from_file(self, filename):
        with open(filename, 'r') as fr:
            for line in fr:
                self.matrix.append([i for i in line.split()])

    def get_col(self, col):
        return [i[col] for i in self.matrix]

    def set_col(self, col, values):
        for v,m in zip(values, self.matrix):
            m[col] = v
            
    def rotate_cw(self):
        self.matrix = [self.get_col(i)[::-1] for i in range(len(self.matrix))]
        
    def rotate_ccw(self):
        self.matrix = [self.get_col(i) for i in range(len(self.matrix)-1, -1, -1)]
        
    def rotate_180(self):
        self.matrix = [i[::-1] for i in self.matrix[::-1]]

    def __repr__(self):
        return '\n'.join([' '.join(self.matrix[i]) for i in range(len(self.matrix))])
        
    def __getitem__(self, row):
        return self.matrix[row]
    
    def __setitem__(self, row, values):
        self.matrix[row] = values
        
    def __len__(self):
        return len(list(self.matrix))
