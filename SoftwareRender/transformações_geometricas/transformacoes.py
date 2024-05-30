import numpy as np
import math as mt

# Transformação de translação para objetos 3D
def aplica_transformacao(vertice, rotacao, translacao, escala):
    
    theta_x = np.radians(rotacao[0])
    
    rotacao_x = np.array([[1, 0, 0],
                        [0, np.cos(theta_x), -np.sin(theta_x)],
                        [0, np.sin(theta_x), np.cos(theta_x)]])
    
    theta_y = np.radians(rotacao[1])
    
    rotacao_y = np.array([[np.cos(theta_y), 0, np.sin(theta_y)],
                        [0, 1, 0],
                        [-np.sin(theta_y), 0, np.cos(theta_y)]])
    
    theta_z = np.radians(rotacao[2])
    
    rotacao_z = np.array([[np.cos(theta_z), -np.sin(theta_z), 0],
                        [np.sin(theta_z), np.cos(theta_z), 0],
                        [0, 0, 1]])
    
    rotacao_matriz = np.dot(rotacao_z, np.dot(rotacao_y, rotacao_x))
    
    transformacao_vertices = []
    for vertice_atual in vertice:
        
        v = np.array(vertice_atual) * escala
        v = np.dot(rotacao_matriz, v)
        v = v + translacao
        
        transformacao_vertices.append(v)
        
    return transformacao_vertices

def calculo_centro_geometrico(mesh):
    
    # Recebe a coordenada máxima e mínima dentro do mesh
    coordenada_maxima = np.copy(mesh.point(next(mesh.vertices())))
    coordenada_minima = np.copy(coordenada_maxima)
    
    # Itera sobre os vértices do mesh para encontrar a coordenada máxima e mínima
    for vh in mesh.vertices():
        
        # Recebe a coordenada do vértice atual
        coordenada = mesh.point(vh)
        
        # Atualiza a coordenada máxima e mínima
        
        # Recebe para a coordenada minima
        if coordenada[0] < coordenada_minima[0]:
            coordenada_minima[0] = coordenada[0]
        if coordenada[1] < coordenada_minima[1]:
            coordenada_minima[1] = coordenada[1]
        if coordenada[2] < coordenada_minima[2]:
            coordenada_minima[2] = coordenada[2]
            
        # Recebe para a coordenada máxima
        if coordenada[0] > coordenada_maxima[0]:
            coordenada_maxima[0] = coordenada[0]
        if coordenada[1] > coordenada_maxima[1]:
            coordenada_maxima[1] = coordenada[1]
        if coordenada[2] > coordenada_maxima[2]:
            coordenada_maxima[2] = coordenada[2]
            
    # Calcula o centro geométrico
    centro_geometrico_x = (coordenada_maxima[0] + coordenada_minima[0]) / 2
    centro_geometrico_y = (coordenada_maxima[1] + coordenada_minima[1]) / 2
    centro_geometrico_z = (coordenada_maxima[2] + coordenada_minima[2]) / 2
    
    return np.array([centro_geometrico_x, centro_geometrico_y, centro_geometrico_z])