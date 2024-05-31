import os
import numpy as np
import openmesh as om
import copy

class Points_Object():
    
    def __init__(self, name):
        
        # Nome do arquivo
        self.name = name
        
        # Pontos no campo 2D
        self.points_line = []    
        self.x = []
        self.y = []
        
        # Pontos no campo 3D
        
        self.points_x = []
        self.points_y = []
        self.points_z = []
        
        # Revolução
        self.slices = None
        self.theta = None
        self.xn = None
        self.yn = None
        self.zn = None
        
        # Define a cor do objeto
        self.color = None
        
        # Define os parametros de rotacao, translacao e escala
        self.rotacao = np.array([0, 0, 0]) # -> [rotacao_x, rotacao_y, rotacao_z]
        self.translacao = np.array([0, 0, 0])
        self.escala = 1
        
    def points_file_to_points_line(self):
        
        # Abre o arquivo
        with open(os.path.join("Wireframe", "points", self.name), "r") as file:
            # Lê o arquivo
            lines = file.readlines()

            # Adiciona os pontos a lista não contando as duas últimas linhas
            for line in lines[:-2]:
                values = line.split()
                if len(values) >= 2:
                    x, y = values[:2]
                    self.points_line.append((int(x), int(y)))   

            # Adiciona o número de fatias
            self.slices = int(lines[-2])

            # Adiciona a cor
            self.color = lines[-1].strip()  # remove any trailing newline

    def points_x_2d(self):
            
        # Adiciona os pontos x
        for point in self.points_line:
            self.x.append(point[0])
        
        return self.x

    def points_y_2d(self):
                
        # Adiciona os pontos y
        for point in self.points_line:
            self.y.append(point[1])
        
        return self.y

    def reverse_points(self, points):
        return points[::-1]
    
    def revolucion(self):
        # Define os pontos no eixo x e y
        self.x = self.points_x_2d()
        self.y = self.points_y_2d()

        # Salva as coordenadas do ponto inicial
        initial_point = (self.x[0], self.y[0])

        # Translada os pontos para que o ponto inicial esteja na origem
        self.x = [x - initial_point[0] for x in self.x]
        self.y = [y - initial_point[1] for y in self.y]

        # Adicionar um ponto extra na base para fechar a parte inferior
        self.x.append(0)
        self.y.append(min(self.y))  # O ponto mais baixo na y
        
        # Parametriza
        self.theta = np.linspace(0, 2 * np.pi, self.slices)

        # Parametriza x, y
        self.xn = np.outer(self.x, np.cos(self.theta))
        self.yn = np.outer(self.x, np.sin(self.theta))

        # Cria uma array z vazia do shape de x / y
        self.zn = np.zeros_like(self.xn)

        # Copia os valores de y do plano 2D para o círculo de revolução
        for i in range(len(self.x)):
            self.zn[i, :] = self.y[i]

        # Translada os pontos de volta à sua posição original
        self.xn += initial_point[0]
        self.yn += initial_point[1]

        # Cria uma malha vazia
        self.mesh = om.TriMesh()

        # Adiciona os vértices à malha
        vertex_handles = []
        for i in range(len(self.xn)):
            for j in range(len(self.theta)):
                vertex_handles.append(self.mesh.add_vertex([self.xn[i][j], self.yn[i][j], self.zn[i][j]]))

        # Adiciona as faces à malha
        for i in range(len(self.xn) - 1):
            for j in range(len(self.theta) - 1):
                vh1 = vertex_handles[i * len(self.theta) + j]
                vh2 = vertex_handles[i * len(self.theta) + (j + 1)]
                vh3 = vertex_handles[(i + 1) * len(self.theta) + j]
                vh4 = vertex_handles[(i + 1) * len(self.theta) + (j + 1)]
                self.mesh.add_face(vh1, vh2, vh4)
                self.mesh.add_face(vh1, vh4, vh3)

        # Iterar sobre todas as faces
        for fh in self.mesh.faces():
            # Obter os vértices de cada face
            vertices = [vh.idx() for vh in self.mesh.fv(fh)]
            print("Face inicial: ", vertices)

        # Iterar sobre todos os vértices
        for vh in self.mesh.vertices():
            # Obter a posição de cada vértice
            position = self.mesh.point(vh)
            print("Vértice inicial: ", position)
        
    def register_points_file(self, points):
        
        # Verifica o número que esta no arquivo, na pasta points, para definir
        # qual será o nome do arquivo, por exemplo points_0.txt -> o numero 0
        count = 0
        for file in os.listdir(os.path.join("Wireframe", "points")):
            count += 1
            
        # Cria o arquivo conforme o count, salvando na outra pasta points_3d. 
        # Salva usando o numpy para facilitar a leitura (np.savetxt)
        np.savetxt(os.path.join("Wireframe", "points_3d", f"points_3d_{count}_xn.txt"), self.xn)
        np.savetxt(os.path.join("Wireframe", "points_3d", f"points_3d_{count}_yn.txt"), self.yn)
        np.savetxt(os.path.join("Wireframe", "points_3d", f"points_3d_{count}_zn.txt"), self.zn)
        
        
        print("Points saved!")
        
    def update_rotacao(self, dx, dy, dz):
        self.rotacao += np.array([dx, dy, dz])
        
    def update_translacao(self, dx, dy):
        self.translacao += np.array([dx, dy, 0])
        
    def update_escala(self, fator):
        self.escala *= fator
        
    def update_color(self, color):
        self.color = color