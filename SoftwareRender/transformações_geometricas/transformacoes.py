import numpy as np
import math as mt

# Transformação de translação para objetos 3D
def translacao(dx, dy, dz):
    return np.array([[1, 0, 0, dx],
                     [0, 1, 0, dy],
                     [0, 0, 1, dz],
                     [0, 0, 0, 1]])

# Transformação de escala para objetos 3D
def escala(sx, sy, sz):
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])
    
# Transformação de rotação em torno do eixo X
def rotacao_x(theta):
    return np.array([[1, 0, 0, 0],
                     [0, mt.cos(theta), -mt.sin(theta), 0],
                     [0, mt.sin(theta), mt.cos(theta), 0],
                     [0, 0, 0, 1]])
    
# Transformação de rotação em torno do eixo Y
def rotacao_y(theta):
    return np.array([[mt.cos(theta), 0, mt.sin(theta), 0],
                     [0, 1, 0, 0],
                     [-mt.sin(theta), 0, mt.cos(theta), 0],
                     [0, 0, 0, 1]])
    
# Transformação de rotação em torno do eixo Z
def rotacao_z(theta):
    return np.array([[mt.cos(theta), -mt.sin(theta), 0, 0],
                     [mt.sin(theta), mt.cos(theta), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])
    