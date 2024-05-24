import copy
import numpy as np


# Retorna todas as faces visíveis do mesh disponivel
def verifica_faces_visiveis(mesh, 
                            vrp_x, vrp_y, vrp_z,
                            ponto_focal_x, ponto_focal_y, ponto_focal_z):
    
    # Faz uma copia "profunda" do mesh, com todas as suas camadas
    mash_visivel = copy.deepcopy(mesh)
    
    N = np.array([vrp_x - ponto_focal_x, vrp_y - ponto_focal_y, vrp_z - ponto_focal_z])
    n = (N / np.linalg.norm(N))
    
    # Checa se a face é visível, se não for, ela deleta da mash_visivel
    for fh in mesh.faces():
        face_normal = np.sum(mash_visivel.calc_face_normal(fh) * n)
        
        if face_normal < 0:
            mash_visivel.delete_face(fh)
        
    # Chama a função para limpar o mesh, removendo quaisquer elementos
    # marcados como deletados e liberando memória
    mash_visivel.garbage_collection() 
    
    return mash_visivel