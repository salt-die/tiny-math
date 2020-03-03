"""
Recursive determinant implementation. Matrix should be a list of lists of floats/ints.
"""
def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]

    return sum(e * cofactor(0, j, matrix) for j, e in enumerate(matrix[0]))

def cofactor(i, j, matrix):
    return (-1)**(i + j) * determinant(minor(i, j, matrix))

def minor(i, j, matrix):
    return [[e for m, e in enumerate(row) if m != j] for n, row in enumerate(matrix) if n != i]