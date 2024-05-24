import openmesh as om
import copy
import numpy as np

# A função tem como função a transformação dos vértices do objeto 3D (malha)
# utilizando a matriz de transformação Msru_src depois de homogenizado
# passando vertice por vertice aplicando-a
def computacao_dos_vertices(mesh, Msru_src_homogenizado):
    
    # Passa por todos os vértices da malha
    for vh in mesh.vertices():
        
        # Para cada vertice, copia as coordenadas para um vetor, adicionando
        # uma quarta coordenada sendo "1", transformando em coordenadas homogêneas
        coordenadas = np.append(copy.deepcopy(mesh.point(vh)), 1)
        
        # Multiplica as coordenadas do vértice pela matriz de transformação
        coordenadas = np.dot(Msru_src_homogenizado, coordenadas)
        
        # Converte as coordenadas homogêneas de volta para coordenadas cartesianas
        # Issa é feita dividindo as primeiras coordenadas pela quarta coordenada
        mesh.point(vh)[0] = coordenadas[0] / coordenadas[3]
        mesh.point(vh)[1] = coordenadas[1] / coordenadas[3]
        mesh.point(vh)[2] = coordenadas[2] / coordenadas[3]
        
    return mesh