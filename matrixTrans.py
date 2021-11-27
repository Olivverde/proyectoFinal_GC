from lib import *
from math import sin, cos

def mulMatrix(A, B):
    ABmatrix = []
    for i in range(len(A)):
        aux_matrix = []
        for j in range(len(B[0])):
            currentRes = 0
            columnB = [row[j] for row in B]
            rowA = A[i]
            for k in range(len(rowA)):
                currentRes += A[i][k] * columnB[k]

            aux_matrix.append(currentRes)
        ABmatrix.append(aux_matrix)

    return ABmatrix

def translateMatrix(point):
    translate = V3(*point)
    
    translationMatrix = [
        [1, 0, 0, translate.x],
        [0, 1, 0, translate.y],
        [0, 0, 1, translate.z],
        [0, 0, 0, 1],
    ]

    return translationMatrix

# Rotation
def rotationMatrix(point):
    rotate = V3(*point)

    a = rotate.x
    rotateX = [
        [1, 0, 0, 0],
        [0, cos(a), -sin(a), 0],
        [0, sin(a), cos(a), 0],
        [0, 0, 0, 1],
    ]

    b = rotate.y
    rotateY = [
        [cos(b), 0, sin(b), 0],
        [0, 1, 0, 0],
        [-sin(b), 0, cos(b), 0],
        [0, 0, 0, 1],
    ]

    c = rotate.z
    rotateZ = [
        [cos(c), -sin(c), 0, 0],
        [sin(c), cos(c), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

    return mulMatrix(rotateX, mulMatrix(rotateY, rotateZ))


# Scale
def scaleMatrix(point):
    scale = V3(*point)

    scaleMatrix = [
        [scale.x, 0, 0, 0],
        [0, scale.y, 0, 0],
        [0, 0, scale.z, 0],
        [0, 0, 0, 1],
    ]

    return scaleMatrix
