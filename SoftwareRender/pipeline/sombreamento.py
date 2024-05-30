import openmesh as om
import numpy as np
from math import pow 

def calcular_centroide(face, mesh):
    
    pontos = []
    for vh in mesh.fv(face): 
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
      
    # Printa todos os parametros usados
    print("Coordenadas da fonte de luz: ", coordenadas_fonte_luz_x, coordenadas_fonte_luz_y, coordenadas_fonte_luz_z)
    print("Iluminacao ambiente Ila_r: ", luz_ambiente_Ila_r)
    print("Iluminacao ambiente Ila_g: ", luz_ambiente_Ila_g)
    print("Iluminacao ambiente Ila_b: ", luz_ambiente_Ila_b)
    print("Iluminacao pontual Il_r: ", luz_pontual_Il_r)
    print("Iluminacao pontual Il_g: ", luz_pontual_Il_g)
    print("Iluminacao pontual Il_b: ", luz_pontual_Il_b)
    print("ka_r: ", ka_r)
    print("ka_g: ", ka_g)
    print("ka_b: ", ka_b)
    print("kd_r: ", kd_r)
    print("kd_g: ", kd_g)
    print("kd_b: ", kd_b)
    print("ks_r: ", ks_r)
    print("ks_g: ", ks_g)
    print("ks_b: ", ks_b)
    print("n: ", n)
    

    # Calcula o centroide da face
    CENTROIDE = calcular_centroide(fh, mesh)
    
    # Iluminacao ambiente
    Ia_r = luz_ambiente_Ila_r * ka_r
    Ia_g = luz_ambiente_Ila_g * ka_g
    Ia_b = luz_ambiente_Ila_b * ka_b
    
    print("Iluminacao ambiente Ia_r: ", Ia_r)
    print("Iluminacao ambiente Ia_g: ", Ia_g)
    print("Iluminacao ambiente Ia_b: ", Ia_b)
    
    # Iluminacao difusa
    n = mesh.calc_face_normal(fh)
    
    # L = L - CENTROIDE
    L = np.array([coordenadas_fonte_luz_x - CENTROIDE[0], 
                    coordenadas_fonte_luz_y - CENTROIDE[1], 
                    coordenadas_fonte_luz_z - CENTROIDE[2]])

    # Normaliza o L
    l = (L / np.linalg.norm(L))
    
    print(np.dot(n, l))
    
    dot_nl = np.dot(n, l)
    
    # Teste de iluminacao difusa
    if dot_nl <= 0:
        
        # Não passou no teste de iluminacao difusa, portanto, não há iluminacao especular
        It_r = Ia_r + 0 + 0
        It_g = Ia_g + 0 + 0
        It_b = Ia_b + 0 + 0
    
    else:   
        
        # Passou no teste de iluminacao difusa 
        Id_r = luz_pontual_Il_r * kd_r * np.dot(n, l)
        Id_g = luz_pontual_Il_g * kd_g * np.dot(n, l)
        Id_b = luz_pontual_Il_b * kd_b * np.dot(n, l)
        
        print("Iluminacao difusa Id_r: ", Id_r)
        print("Iluminacao difusa Id_g: ", Id_g)
        print("Iluminacao difusa Id_b: ", Id_b)
        
        # Iluminacao Especular
        # R = 2 * (N.L) * N - L
        rx = 2 * np.dot(n, l) * n[0] - l[0]
        ry = 2 * np.dot(n, l) * n[1] - l[1]
        rz = 2 * np.dot(n, l) * n[2] - l[2]
        
        # Rearranja o vetor R
        r = np.array([rx, ry, rz])
        
        # S = S - CENTROIDE
        S = np.array([vrp_x - CENTROIDE[0], vrp_y - CENTROIDE[1], vrp_z - CENTROIDE[2]])

        # Normaliza o S
        s = (S / np.linalg.norm(S))
        
        print("S: ", s)
        print("R: ", r)
        
        dot_rs = np.dot(r, s)
        print("Dot_rs: ", dot_rs)
        
        # Teste de iluminacao especular
        if dot_rs <= 0:
            
            # Não passou no teste de iluminacao especular, portanto, não há iluminacao especular
            It_r = Ia_r + Id_r + 0
            It_g = Ia_g + Id_g + 0
            It_b = Ia_b + Id_b + 0
            
        else:
            
            
            # Passou no teste de iluminacao especular
            Is_r = luz_pontual_Il_r * ks_r * pow(dot_rs, 2.15) # -> NAO SEI PORQUE QUANDO ELEVA
            Is_g = luz_pontual_Il_g * ks_g * pow(dot_rs, 2.15) # -> A n ELE DROPA UM VETOR
            Is_b = luz_pontual_Il_b * ks_b * pow(dot_rs, 2.15)
            
            print("Iluminacao especular Is_r: ", Is_r)
            print("Iluminacao especular Is_g: ", Is_g)
            print("Iluminacao especular Is_b: ", Is_b)
            
            # Iluminacao total
            It_r = Ia_r + Id_r + Is_r
            It_g = Ia_g + Id_g + Is_g
            It_b = Ia_b + Id_b + Is_b
    
    print("Iluminacao It_r: ", It_r)
    print("Iluminacao It_g: ", It_g)
    print("Iluminacao It_b: ", It_b)    
    print("Sombreamento: ", It_r, It_g, It_b)
    
    # Rearranja o vetor de cor
    cor = np.array([It_r, It_g, It_b, 1])
    
    cor = np.clip(cor, 0, 255)
    
    # Aplique a cor na face do objeto
    mesh.set_color(fh, cor)
    
    return mesh