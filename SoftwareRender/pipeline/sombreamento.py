import openmesh as om
import numpy as np

def calcular_centroide(face, mesh):
    
    pontos = []
    for vh in mesh.fv(face):  # Itera sobre os vértices da face
        pontos.append(mesh.point(vh))
    pontos = np.array(pontos)
    centroide = np.mean(pontos, axis=0)
    return centroide

def aplicacao_sombreamento(mesh, fh,
                           vrp_x, vrp_y, vrp_z,
                           luz_ambiente_Ila_r, luz_ambiente_Ila_g, luz_ambiente_Ila_b,
                           luz_pontual_Il_r, luz_pontual_Il_g, luz_pontual_Il_b,
                           coordenadas_fonte_luz_x, coordenadas_fonte_luz_y, coordenadas_fonte_luz_z,
                           ka_r, ka_g, ka_b,
                           kd_r, kd_g, kd_b,
                           ks_r, ks_g, ks_b, n):
      

    # Calcula o centroide da face
    CENTROIDE = calcular_centroide(fh, mesh)
    
    # Iluminacao ambiente
    Ia_r = luz_ambiente_Ila_r * ka_r
    Ia_g = luz_ambiente_Ila_g * ka_g
    Ia_b = luz_ambiente_Ila_b * ka_b
    
    # Iluminacao difusa
    n = mesh.calc_face_normal(fh)
    
    # L = L - CENTROIDE
    L = np.array([coordenadas_fonte_luz_x - CENTROIDE[0], 
                    coordenadas_fonte_luz_y - CENTROIDE[1], 
                    coordenadas_fonte_luz_z - CENTROIDE[2]])
    
    # Normaliza o L
    l = (L / np.linalg.norm(L))
    
    # Teste de iluminacao difusa
    n_l = np.dot(n, l)
    
    if n_l < 0:
        
        n_l = 0
        
        # Total dos 3 componentes
        It_r = Ia_r
        It_g = Ia_g
        It_b = Ia_b
                    
        return np.array([It_r, It_g, It_b, 1.0])
        
    else:
        
        Id_r = luz_pontual_Il_r * kd_r * n_l
        Id_g = luz_pontual_Il_g * kd_g * n_l
        Id_b = luz_pontual_Il_b * kd_b * n_l
        
        # Iluminacao especular
        
        # R = 2 * (N . L) * N - L
        rx = 2 * (np.dot(n, l)) * n[0] - l[0]
        ry = 2 * (np.dot(n, l)) * n[1] - l[1]
        rz = 2 * (np.dot(n, l)) * n[2] - l[2]
        
        # Rearranja o vetor R
        r = np.array([rx, ry, rz])
        
        # S = S - CENTROIDE
        S = np.array([vrp_x - CENTROIDE[0], vrp_y - CENTROIDE[1], vrp_z - CENTROIDE[2]])
        
        # Normaliza o S
        s = (S / np.linalg.norm(S))
        
        # Teste de iluminacao especular
        n_s = np.dot(s, r)
        
        if n_s < 0:
            n_s = 0
            
            # Total dos 3 componentes
            It_r = Ia_r + Id_r
            It_g = Ia_g + Id_g
            It_b = Ia_b + Id_b

            return np.array([It_r, It_g, It_b, 1.0])
            
        else:
            
            Is_r = luz_pontual_Il_r * ks_r * (n_s ** n)
            Is_g = luz_pontual_Il_g * ks_g * (n_s ** n)
            Is_b = luz_pontual_Il_b * ks_b * (n_s ** n)
        
            # Total dos 3 componentes
            It_r = Ia_r + Id_r + Is_r
            It_g = Ia_g + Id_g + Is_g
            It_b = Ia_b + Id_b + Is_b
    
            return np.array([It_r, It_g, It_b, 1.0])
            
    