
class Matrix:

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows

        self.matrix = [['0' for i in xrange(cols)] for j in xrange(rows)]

    def set_item(self, row, col, value):
        self.matrix[row-1][col-1] = str(value)

    def get_item(self, row, col):
        return self.matrix[row-1][col-1]

    def __repr__(self):
        return '\n'.join([' '.join(self.matrix[i]) for i in range(self.rows)])
