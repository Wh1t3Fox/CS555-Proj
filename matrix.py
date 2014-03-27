
class Matrix:

    def __init__(self, filename):
        self.matrix = []
        self.create_from_file(filename)

        #self.matrix = [['0' for i in xrange(cols)] for j in xrange(rows)]

    def create_from_file(self, filename):
        with open(filename, 'r') as fr:
            for line in fr:
                self.matrix.append([i for i in line.split()])

    def set_item(self, row, col, value):
        self.matrix[row-1][col-1] = str(value)

    def get_item(self, row, col):
        return self.matrix[row-1][col-1]

    def get_row(self, row):
        return ' '.join(self.matrix[row-1])

    def get_col(self, col):
        return '\n'.join([i[col-1] for i in self.matrix])

    def __repr__(self):
        return '\n'.join([' '.join(self.matrix[i]) for i in range(len(self.matrix))])
