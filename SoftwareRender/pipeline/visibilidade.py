import copy
import numpy as np
from SoftwareRender.transformações_geometricas.transformacoes import calculo_centro_geometrico

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

def verifica_mesh_visivel(mesh, near, far):
    
    # Calcula o centro geométrico do objeto da mesh indicada
    CENTRO_GEOMETRICO = calculo_centro_geometrico(mesh)
    
    # Faz o teste de distância do centro geométrico em relação ao near e o far
    if ((-CENTRO_GEOMETRICO[2] < near) or (-CENTRO_GEOMETRICO[2] > far)):
        return True
    else:
        return False