import openmesh as om
import copy
import numpy as np

# A função tem como função a transformação dos vértices do objeto 3D (malha)
# utilizando a matriz de transformação Msru_src depois de homogenizado
# passando vertice por vertice aplicando-a
def computacao_dos_vertices(mesh, Msru_src_homogenizado):
    
    for vh in mesh.vertices():
        
        # Pega as coordenadas do vértice
        coord = np.append(copy.deepcopy(mesh.point(vh)), 1)
        
        # Transforma as coordenadas em uma matriz coluna
        coord = coord.reshape((4, 1))
        
        # Aplica a matriz de transformação
        coord = np.dot(Msru_src_homogenizado, coord)
        
        coord_homogenizadas = np.array([[coord[0][0] / coord[3][0]],
                                        [coord[1][0] / coord[3][0]],
                                        [coord[2][0]],
                                        [coord[3][0]]])
        
        # Atualiza as coordenadas do vértice
        mesh.point(vh)[0] = coord_homogenizadas[0]
        mesh.point(vh)[1] = coord_homogenizadas[1]
        mesh.point(vh)[2] = coord_homogenizadas[2]
        
    return mesh
        