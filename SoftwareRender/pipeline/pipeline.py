import numpy as np

# A base ortonormal do SRC define a matriz de rotações que alinha os eixos do 
# SRC aos eixos do SRU.
# -> Calcula-se o vetor n, que é a direção do eixo Z do SRC em relação ao SRU.
# -> Calcula-se o vetor v, que é a direção do eixo Y do SRC em relação ao SRU.
# -> Calcula-se o vetor u, que é a direção do eixo X do SRC em relação ao SRU.
# -> A matriz Msru_src é a matriz de rotação que alinha os eixos do SRC aos eixos do SRU.
def Msru_src(vrp_x, vrp_y, vrp_z,
            ponto_focal_x, ponto_focal_y, ponto_focal_z,
            view_up_x, view_up_y, view_up_z):

    # Calculando a Base Ortonormal -> Vetor N
    N = np.array([vrp_x - ponto_focal_x, vrp_y - ponto_focal_y, vrp_z - ponto_focal_z])
    n = (N / np.linalg.norm(N))
    
    # Calculando a base Ortonormal -> Vetor V
    Y = np.array([view_up_x, view_up_y, view_up_z])
    V = (Y - np.dot(Y, n) * n)
    v = (V / np.linalg.norm(V))
    
    # Calculando a base Ortonormal -> Vetor U
    u = np.cross(v, n)
    
    # Cria o vrp como um vetor
    vrp = np.array([vrp_x, vrp_y, vrp_z])
    
    # Matriz de Transformação Msru -> Msrc
    Msru_src = np.array([[u[0], u[1], u[2], np.dot(-vrp, u)],
                         [v[0], v[1], v[2], np.dot(-vrp, v)],
                         [n[0], n[1], n[2], np.dot(-vrp, n)],
                         [0, 0, 0, 1]])
    
    
    return Msru_src

# Projeção é o processo que possibilita representar objetos tridimensionais (3D) 
# em meios bidimensionais (2D), que são os dispositivos de exibição utilizados 
# nos computadores
# -> Usando coordenadas homogêneas, podemos escrever a transformação perspectiva 
# na forma matricial.
def Mproj_perspectiva(dp):
    
    Mproj = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, -(1/dp), 0]])
    
    return Mproj

# O plano de projeção é perpendicular à direção de projeção, tendo uma visão
# frontal ao objeto, isso chama-se projeção paralela (ortogonal).
def Mproj_paralela():
    
    Mproj = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 1]])
    
    return Mproj

# O mapeamento para SRT corresponde a uma porção visível do mundo, porta de visão
# para a região da tela correspondente, se a janela e a porta de visão não possuirem
# a mesma razão de aspecto, a imagem será distorcida.
def Mjp(uMin, uMax, vMin, vMax,
         xMin, xMax, yMin, yMax):
    
    Mjp = np.array([[((uMax - uMin) / (xMax - xMin)), 0, 0, uMin - xMin * (uMax - uMin) / (xMax - xMin)],
                    [0, ((vMin - vMax) / (yMax - yMin)), 0, vMin - yMin * (vMax - vMin) / (yMax - yMin)],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    
    return Mjp
  
# Para reduzir a quantidade de cálculos, concatena-se as matrizes de transformação
# na ordem correta para obter a matriz de transformação final
# -> Msru_srt = Mjp * Mproj * Msru_src  
def Msru_srt(Msru_src, Mproj, Mjp):
    
    Msru_srt = np.dot(Mjp, np.dot(Mproj, Msru_src))

    return Msru_srt