import customtkinter as ctk
import tkinter as tk
import os
import copy
import numpy as np
import openmesh as om
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from rich import print

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from SoftwareRender.pipeline.pipeline import Msru_src, Mproj_perspectiva, Mproj_paralela, Mjp, Msru_srt, homogenizar
from SoftwareRender.pipeline.visibilidade import verifica_faces_visiveis, verifica_mesh_visivel
from SoftwareRender.pipeline.sombreamento import aplicacao_sombreamento
from SoftwareRender.pipeline.computacao_vertices import computacao_dos_vertices
from SoftwareRender.transformações_geometricas.transformacoes import aplica_transformacao
from SoftwareRender.utilidades.ferramentas import rgb_to_hex

class Screen():
    
    def __init__(self, files_classes):
        
        super().__init__()
        
        # Define a lista de classes de objetos
        self.files_classes = files_classes
        
        # Define um backup da lista de classes de objetos
        self.backup_files_classes = copy.deepcopy(files_classes)
        
        # Define a aparência da tela principal como dark
        ctk.set_appearance_mode("dark")
        
        self.app = ctk.CTk()
        self.app.title("T02 - Software Render")
        self.app.geometry("1600x900")

        self.app.resizable(False, False)

        self.photo = tk.PhotoImage(file="img/formas.png")
        self.app.iconphoto(False, self.photo)

        # Define o grid da tela (tela inteira)
        self.grid_canvas_column()

        # Cria os botões de projeção
        self.botoes_projeção()
        
        # Cria os botões de seleção de objeto
        self.opcao_objeto()

        # Define os dados da viwe-port
        self.dados_view_port()
        self.dados_view_up()
        self.dados_vrp()
        self.dados_ponto_focal()
        self.distancia_ao_plano()
        self.dados_janela_mundo()
        
        # Define os dados de sombreamento
        self.sombreamento_Ka() 
        self.sombreamento_Kd()
        self.sombreamento_Ks()
        self.luz_ambiente_Ila()
        self.luz_pontual_Il()
        self.coordenadas_fonte_luz()
        self.n()
        
        
        # Define parametros gerais do pipeline
        self.Matrix_sru_src = None
        self.Matrix_proj = None
        self.Matrix_jp = None
        self.Matrix_sru_srt = None
        self.Msru_srt_homogenizado = None

        self.fill_color = False

        # Desenha todos os objetos na tela
        for objeto in self.files_classes:
            self.draw_mesh(objeto)
        
    def run(self):
        
        # Cria as binds para os botões, por padrao o objeto 1 é selecionado
        self.binds("Objeto 1")
        
        self.app.mainloop()
    
    def quit(self, event=None):
        self.app.quit()  
    
    def binds(self, objeto_selecionado):
        
        # Botão 1 do teclado para printar os valores obtidos nos entrys
        self.app.bind("<F1>", self.print_values)
        
        # Botão 2 do teclado para pegar os valores dos entrys
        self.app.bind("<F2>", self.get_values)
          
        # Botao 9 do teclado para plotar o gráfico do objeto
        self.app.bind("<F9>", self.plota_grafico)
        
        # Botao 10 do teclado para deletar o gráfico do objeto
        self.app.bind("<F10>", self.plota_grafico)
        
        # Botao 12 do teclado fecha o programa
        self.app.bind("<F12>", self.quit)  
        
        # Botão U do teclado para atualizar o canvas e redesenhar o objeto
        self.app.bind("u", self.update_canvas)
        self.app.bind("U", self.update_canvas)
        
        # Botão R do teclado para restaurar os valores dos objetos
        self.app.bind("r", self.restaura_files_classes)
        self.app.bind("R", self.restaura_files_classes)
        
        
        # Verifica qual objeto está selecionado com base no OptionMenu, para ai
        # sim atualizar os parametros de rotacao, translacao e escala.
        # Ele esta selecionado como [Objeto {numero}], então pegamos o numero para
        # pegar a classe correta

        # Pega o numero do objeto selecionado
        numero_objeto = int(objeto_selecionado.split(" ")[1]) - 1
        
        # Pega a classe do objeto selecionado
        objeto = self.files_classes[numero_objeto]
        
        # Define os botoes de rotacao, translacao e escala
        self.app.bind("<Left>", lambda event: self.update_translacao_esquerda(objeto))
        self.app.bind("<Right>", lambda event: self.update_translacao_direita(objeto))
        self.app.bind("<Up>", lambda event: self.update_translacao_cima(objeto))
        self.app.bind("<Down>", lambda event: self.update_translacao_baixo(objeto))
        
        self.app.bind("w", lambda event: self.update_rotacao_x_mais(objeto))
        self.app.bind("W", lambda event: self.update_rotacao_x_mais(objeto))
        
        self.app.bind("s", lambda event: self.update_rotacao_x_menos(objeto))
        self.app.bind("S", lambda event: self.update_rotacao_x_menos(objeto))
        
        self.app.bind("a", lambda event: self.update_rotacao_y_mais(objeto))
        self.app.bind("A", lambda event: self.update_rotacao_y_mais(objeto))
        
        self.app.bind("d", lambda event: self.update_rotacao_y_menos(objeto))
        self.app.bind("D", lambda event: self.update_rotacao_y_menos(objeto))
        
        self.app.bind("q", lambda event: self.update_rotacao_z_mais(objeto))
        self.app.bind("Q", lambda event: self.update_rotacao_z_mais(objeto))
        
        self.app.bind("e", lambda event: self.update_rotacao_z_menos(objeto))
        self.app.bind("E", lambda event: self.update_rotacao_z_menos(objeto))
        
        self.app.bind("z", lambda event: self.update_escala_mais(objeto))
        self.app.bind("Z", lambda event: self.update_escala_mais(objeto))
        
        self.app.bind("x", lambda event: self.update_escala_menos(objeto))
        self.app.bind("X", lambda event: self.update_escala_menos(objeto))
                   
    def update_rotacao_x_mais(self, objeto, event=None):
        
        objeto.update_rotacao(2, 0, 0)
        self.update_canvas()
        
    def update_rotacao_x_menos(self, objeto, event=None):
            
        objeto.update_rotacao(-2, 0, 0)
        self.update_canvas()
    
    def update_rotacao_y_mais(self, objeto, event=None):
            
        objeto.update_rotacao(0, 2, 0)
        self.update_canvas()   
        
    def update_rotacao_y_menos(self, objeto, event=None):
                
        objeto.update_rotacao(0, -2, 0)
        self.update_canvas()     
        
    def update_rotacao_z_mais(self, objeto, event=None):
                    
        objeto.update_rotacao(0, 0, 2)
        self.update_canvas()    
    
    def update_rotacao_z_menos(self, objeto, event=None):
        
        objeto.update_rotacao(0, 0, -2)
        self.update_canvas()
        
    def update_translacao_esquerda(self, objeto, event=None):
        
        objeto.update_translacao(-10, 0)
        self.update_canvas()
        
    def update_translacao_direita(self, objeto, event=None):
        
        objeto.update_translacao(10, 0)
        self.update_canvas()
        
    def update_translacao_cima(self, objeto, event=None):
        
        objeto.update_translacao(0, -10)
        self.update_canvas()
        
    def update_translacao_baixo(self, objeto, event=None):
        
        objeto.update_translacao(0, 10)
        self.update_canvas()
        
    def update_escala_mais(self, objeto, event=None):
        
        objeto.update_escala(1.1)
        self.update_canvas()
        
    def update_escala_menos(self, objeto, event=None):
        
        objeto.update_escala(0.9)
        self.update_canvas()
   
    def update_canvas(self, event=None):
        
        # Limpa o canvas
        self.canvas.delete("all")
        
        # Plota novamente todos os objetos
        for objeto in self.files_classes:
            
            self.draw_mesh(objeto)
            
        # Recria as binds para os botões apenas se o usuário mudou o objeto
        self.binds(self.optionmenu_var.get())
     
    def restaura_files_classes(self, event=None):
        
        # Restaura os valores dos objetos antes das transformações
        self.files_classes = copy.deepcopy(self.backup_files_classes)
        
        # Atualiza o canvas
        self.update_canvas()
        
    def projeta_ponto(self, vertice, width=800, height=800):
        
        x = vertice[0] + width / 2
        y = vertice[1] + height / 2
        
        return x, y

    def draw_mesh(self, objeto, width=800, height=800):
        
        # Separa a mesh do objeto selecionado
        mesh = objeto.mesh

        # Itera sobre todas as faces
        for face in mesh.faces():
            
            # Obtem os vértices da face
            vertices = [mesh.point(vh) for vh in mesh.fv(face)]

            transformacao_vertices = aplica_transformacao(vertices, objeto.rotacao, objeto.translacao, objeto.escala)

            # Projeta os vértices 3d para 2d
            projected = [self.projeta_ponto(v) for v in transformacao_vertices]

            # Desenha a face
            
            if self.fill_color == True:
                
                # Resgate a cor da face
                color = mesh.color(face)
                
                # Retira a ultima posição da cor que é 1
                color = color[:-1]
                
                # Converte a cor para hexadecimal
                color = rgb_to_hex(color)
            
                self.canvas.create_polygon(projected, outline=color, fill=color)
                
            else:
                
                self.canvas.create_polygon(projected, outline="gray", fill="gray")
    
    def grid_canvas_column(self):
        
        # Define a configuração de colunas, dividindo em 2
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=1)
        
        self.canvas = ctk.CTkCanvas(self.app, width=800, height=800, bg="white", borderwidth=2, relief="solid")
        self.canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros do mundo
        self.frame_parameters = ctk.CTkScrollableFrame(self.app)
        self.frame_parameters.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    
        # Configura o grid do frame_parameters para que tenha 4 linhas
        self.frame_parameters.grid_rowconfigure(0, weight=1)
        self.frame_parameters.grid_rowconfigure(1, weight=1)
        self.frame_parameters.grid_rowconfigure(2, weight=1)
        self.frame_parameters.grid_rowconfigure(3, weight=1)
        
        # Cria um frame abaixo do canvas, linha 1 coluna 0 para os botões de 
        # projeção
        self.frame_projeção = ctk.CTkFrame(self.app)
        self.frame_projeção.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configura o grid do frame_projeção para que tenha 2 colunas
        self.frame_projeção.grid_columnconfigure(0, weight=1)
        self.frame_projeção.grid_columnconfigure(1, weight=1)
        
        # Cria um frame abaixo no CTkScrollableFrame para selecionar o objeto
        # que será modificado
        self.frame_objeto = ctk.CTkFrame(self.app)
        self.frame_objeto.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
    def botoes_projeção(self):
        
        self.radio_var_projecao = ctk.IntVar(value=0)
        
        # Cria um botão radio para a projeção perspectiva
        radio_perspectiva = ctk.CTkRadioButton(self.frame_projeção, text="Perspectiva",
                                               variable=self.radio_var_projecao, value=0)
        radio_perspectiva.grid(row=0, column=0, padx=10, pady=10)
        
        # Cria um botão radio para a projeção paralela
        radio_paralela = ctk.CTkRadioButton(self.frame_projeção, text="Paralela",
                                               variable=self.radio_var_projecao, value=1)
        radio_paralela.grid(row=0, column=1, padx=10, pady=10)
    
    def opcao_objeto(self):
        
        # Lista com as opções de objetos, baseado na quantidade de classes 
        # dentro da lista files_classes
        
        # Cria uma lista com as strings Objeto 1, Objeto 2, Objeto 3, ..., com
        # base na quantidade de classes dentro da lista files_classes
        self.opcoes = ["Objeto " + str(i+1) for i in range(len(self.files_classes))]
        
        self.label_objeto = ctk.CTkLabel(self.frame_objeto, text="Seleção de Objetos",
                                        text_color="White", justify="center", font=("Arial", 15))
        self.label_objeto.grid(row=0, column=0, padx=10, pady=10)    
        
        self.optionmenu_var = ctk.StringVar(value="Objeto 1")
        self.opcao_menu = ctk.CTkOptionMenu(self.frame_objeto, values=self.opcoes,
                                            variable=self.optionmenu_var)
        self.opcao_menu.grid(row=0, column=1, padx=10, pady=10)
           
    def dados_view_port(self):
        
        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros da view-port
        self.frame_view_port = ctk.CTkFrame(self.frame_parameters)
        self.frame_view_port.grid(row=0, column=0, sticky="nsew")
        
        # Configura p frame da view-port para que tenha 3 linhas e 4 colunas
        self.frame_view_port.grid_rowconfigure(0, weight=1)
        self.frame_view_port.grid_rowconfigure(1, weight=1)
        self.frame_view_port.grid_rowconfigure(2, weight=1)
        self.frame_view_port.grid_columnconfigure(0, weight=1)
        self.frame_view_port.grid_columnconfigure(1, weight=1)
        self.frame_view_port.grid_columnconfigure(2, weight=1)
        self.frame_view_port.grid_columnconfigure(3, weight=1)
        
        
        self.label_view_port = ctk.CTkLabel(self.frame_view_port, text="View-Port", 
                                            text_color="White", justify="center", font=("Arial", 20))
        self.label_view_port.grid(row=0, column=0, pady=10)
        
        self.label_view_port_uMin = ctk.CTkLabel(self.frame_view_port, text="uMin", 
                                                text_color="White", justify="center", font=("Arial", 15))
        self.label_view_port_uMin.grid(row=1, column=0, pady=10)
     
        self.entry_view_port_uMin = ctk.CTkEntry(self.frame_view_port, width=100, placeholder_text=0)
        self.entry_view_port_uMin.grid(row=1, column=1, pady=10)
        
        self.label_view_port_uMax = ctk.CTkLabel(self.frame_view_port, text="uMax", 
                                                text_color="White", justify="center", font=("Arial", 15))
        self.label_view_port_uMax.grid(row=1, column=2, pady=10, padx=10)
        
        self.entry_view_port_uMax = ctk.CTkEntry(self.frame_view_port, width=100, placeholder_text=800)
        self.entry_view_port_uMax.grid(row=1, column=3, pady=10)
        
        self.label_view_port_vMin = ctk.CTkLabel(self.frame_view_port, text="vMin", 
                                                text_color="White", justify="center", font=("Arial", 15))
        self.label_view_port_vMin.grid(row=2, column=0, pady=10)
        
        self.entry_view_port_vMin = ctk.CTkEntry(self.frame_view_port, width=100, placeholder_text=0)
        self.entry_view_port_vMin.grid(row=2, column=1, pady=10)
               
        self.label_view_port_vMax = ctk.CTkLabel(self.frame_view_port, text="vMax", 
                                                text_color="White", justify="center", font=("Arial", 15))
        self.label_view_port_vMax.grid(row=2, column=2, pady=10)
        
        self.entry_view_port_vMax = ctk.CTkEntry(self.frame_view_port, width=100, placeholder_text=800)
        self.entry_view_port_vMax.grid(row=2, column=3, pady=10)
         
    def dados_view_up(self):
        
        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros da view-up
        self.frame_view_up = ctk.CTkFrame(self.frame_parameters)
        self.frame_view_up.grid(row=1, column=0, sticky="nsew")
        
        # Configura o frame da view-up para que tenha 3 linhas e 4 colunas
        self.frame_view_up.grid_rowconfigure(0, weight=1)
        self.frame_view_up.grid_rowconfigure(1, weight=1)
        self.frame_view_up.grid_rowconfigure(2, weight=1)
        self.frame_view_up.grid_columnconfigure(0, weight=1)
        self.frame_view_up.grid_columnconfigure(1, weight=1)
        self.frame_view_up.grid_columnconfigure(2, weight=1)
        self.frame_view_up.grid_columnconfigure(3, weight=1)
        
        self.label_view_up = ctk.CTkLabel(self.frame_view_up, text="View-Up", 
                                            text_color="White", justify="center", font=("Arial", 20))
        self.label_view_up.grid(row=0, column=0, pady=10)
        
        self.label_view_up_x = ctk.CTkLabel(self.frame_view_up, text="x", 
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_view_up_x.grid(row=1, column=0, pady=10)
        
        self.entry_view_up_x = ctk.CTkEntry(self.frame_view_up, width=100, placeholder_text=0)
        self.entry_view_up_x.grid(row=1, column=1, pady=10)
        
        self.label_view_up_y = ctk.CTkLabel(self.frame_view_up, text="y", 
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_view_up_y.grid(row=1, column=2, pady=10, padx=10)
        
        self.entry_view_up_y = ctk.CTkEntry(self.frame_view_up, width=100, placeholder_text=1)
        self.entry_view_up_y.grid(row=1, column=3, pady=10)
        
        self.label_view_up_z = ctk.CTkLabel(self.frame_view_up, text="z", 
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_view_up_z.grid(row=1, column=4, pady=10, padx=10)

        self.entry_view_up_z = ctk.CTkEntry(self.frame_view_up, width=100, placeholder_text=0)
        self.entry_view_up_z.grid(row=1, column=5, pady=10)
             
    def dados_vrp(self):
        
        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros da vrp
        self.frame_vrp = ctk.CTkFrame(self.frame_parameters)
        self.frame_vrp.grid(row=2, column=0, sticky="nsew")
        
        # Configura o frame da vrp para que tenha 3 linhas e 4 colunas
        self.frame_vrp.grid_rowconfigure(0, weight=1)
        self.frame_vrp.grid_rowconfigure(1, weight=1)
        self.frame_vrp.grid_rowconfigure(2, weight=1)
        self.frame_vrp.grid_columnconfigure(0, weight=1)
        self.frame_vrp.grid_columnconfigure(1, weight=1)
        self.frame_vrp.grid_columnconfigure(2, weight=1)
        self.frame_vrp.grid_columnconfigure(3, weight=1)
        
        self.label_vrp = ctk.CTkLabel(self.frame_vrp, text="VRP", 
                                            text_color="White", justify="center", font=("Arial", 20))
        self.label_vrp.grid(row=0, column=0, pady=10)
        
        self.label_vrp_x = ctk.CTkLabel(self.frame_vrp, text="x", 
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_vrp_x.grid(row=1, column=0, pady=10)
        
        self.entry_vrp_x = ctk.CTkEntry(self.frame_vrp, width=100, placeholder_text=0)
        self.entry_vrp_x.grid(row=1, column=1, pady=10)
        
        self.label_vrp_y = ctk.CTkLabel(self.frame_vrp, text="y", 
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_vrp_y.grid(row=1, column=2, pady=10, padx=10)
        
        self.entry_vrp_y = ctk.CTkEntry(self.frame_vrp, width=100, placeholder_text=10)
        self.entry_vrp_y.grid(row=1, column=3, pady=10)
        
        self.label_vrp_z = ctk.CTkLabel(self.frame_vrp, text="z", 
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_vrp_z.grid(row=1, column=4, pady=10, padx=10)
        
        self.entry_vrp_z = ctk.CTkEntry(self.frame_vrp, width=100, placeholder_text=10)
        self.entry_vrp_z.grid(row=1, column=5, pady=10)
                 
    def dados_ponto_focal(self):
            
        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros do ponto focal
        self.frame_ponto_focal = ctk.CTkFrame(self.frame_parameters)
        self.frame_ponto_focal.grid(row=3, column=0, sticky="nsew")
        
        # Configura o frame do ponto focal para que tenha 3 linhas e 4 colunas
        self.frame_ponto_focal.grid_rowconfigure(0, weight=1)
        self.frame_ponto_focal.grid_rowconfigure(1, weight=1)
        self.frame_ponto_focal.grid_rowconfigure(2, weight=1)
        self.frame_ponto_focal.grid_columnconfigure(0, weight=1)
        self.frame_ponto_focal.grid_columnconfigure(1, weight=1)
        self.frame_ponto_focal.grid_columnconfigure(2, weight=1)
        self.frame_ponto_focal.grid_columnconfigure(3, weight=1)
        
        self.label_ponto_focal = ctk.CTkLabel(self.frame_ponto_focal, text="Ponto Focal", 
                                            text_color="White", justify="center", font=("Arial", 20))
        self.label_ponto_focal.grid(row=0, column=0, pady=10)
        
        self.label_ponto_focal_x = ctk.CTkLabel(self.frame_ponto_focal, text="x", 
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_ponto_focal_x.grid(row=1, column=0, pady=10)
        
        self.entry_ponto_focal_x = ctk.CTkEntry(self.frame_ponto_focal, width=100, placeholder_text=0)
        self.entry_ponto_focal_x.grid(row=1, column=1, pady=10)
        
        self.label_ponto_focal_y = ctk.CTkLabel(self.frame_ponto_focal, text="y", 
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_ponto_focal_y.grid(row=1, column=2, pady=10, padx=10)
        
        self.entry_ponto_focal_y = ctk.CTkEntry(self.frame_ponto_focal, width=100, placeholder_text=0)
        self.entry_ponto_focal_y.grid(row=1, column=3, pady=10)
        
        self.label_ponto_focal_z = ctk.CTkLabel(self.frame_ponto_focal, text="z",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_ponto_focal_z.grid(row=1, column=4, pady=10, padx=10)
        
        self.entry_ponto_focal_z = ctk.CTkEntry(self.frame_ponto_focal, width=100, placeholder_text=0)
        self.entry_ponto_focal_z.grid(row=1, column=5, pady=10)     
        
    def distancia_ao_plano(self):
        
        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros da distância ao plano
        self.frame_distancia_ao_plano = ctk.CTkFrame(self.frame_parameters)
        self.frame_distancia_ao_plano.grid(row=4, column=0, sticky="nsew")
        
        # Configura o frame da distância ao plano para que tenha 3 linhas e 4 colunas
        self.frame_distancia_ao_plano.grid_rowconfigure(0, weight=1)
        self.frame_distancia_ao_plano.grid_rowconfigure(1, weight=1)
        self.frame_distancia_ao_plano.grid_rowconfigure(2, weight=1)
        self.frame_distancia_ao_plano.grid_columnconfigure(0, weight=1)
        self.frame_distancia_ao_plano.grid_columnconfigure(1, weight=1)
        self.frame_distancia_ao_plano.grid_columnconfigure(2, weight=1)
        self.frame_distancia_ao_plano.grid_columnconfigure(3, weight=1)
        
        self.label_distancia_ao_plano = ctk.CTkLabel(self.frame_distancia_ao_plano, text="Distância ao Plano", 
                                            text_color="White", justify="center", font=("Arial", 20))
        self.label_distancia_ao_plano.grid(row=0, column=0, pady=10)
        
        self.label_distancia_ao_plano_projecao = ctk.CTkLabel(self.frame_distancia_ao_plano, text="DP",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_distancia_ao_plano_projecao.grid(row=1, column=0, pady=10)
        
        self.entry_distancia_ao_plano_projecao = ctk.CTkEntry(self.frame_distancia_ao_plano, width=100, placeholder_text=10)
        self.entry_distancia_ao_plano_projecao.grid(row=1, column=1, pady=10)
        
        self.label_distancia_ao_plano_near = ctk.CTkLabel(self.frame_distancia_ao_plano, text="Near",
                                            text_color="White", justify="center", font=("Arial", 15))
        
        self.label_distancia_ao_plano_near.grid(row=1, column=2, pady=10, padx=10)
        
        self.entry_distancia_ao_plano_near = ctk.CTkEntry(self.frame_distancia_ao_plano, width=100, placeholder_text=5)
        self.entry_distancia_ao_plano_near.grid(row=1, column=3, pady=10)
        
        self.label_distancia_ao_plano_far = ctk.CTkLabel(self.frame_distancia_ao_plano, text="Far",
                                            text_color="White", justify="center", font=("Arial", 15))
        
        self.label_distancia_ao_plano_far.grid(row=2, column=0, pady=10)
        
        self.entry_distancia_ao_plano_far = ctk.CTkEntry(self.frame_distancia_ao_plano, width=100, placeholder_text=15)
        self.entry_distancia_ao_plano_far.grid(row=2, column=1, pady=10)
                                                              
    def dados_janela_mundo(self):
        
        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros da janela mundo
        self.frame_janela_mundo = ctk.CTkFrame(self.frame_parameters)
        self.frame_janela_mundo.grid(row=5, column=0, sticky="nsew")
        
        # Configura o frame da janela mundo para que tenha 3 linhas e 4 colunas
        self.frame_janela_mundo.grid_rowconfigure(0, weight=1)
        self.frame_janela_mundo.grid_rowconfigure(1, weight=1)
        self.frame_janela_mundo.grid_rowconfigure(2, weight=1)
        self.frame_janela_mundo.grid_columnconfigure(0, weight=1)
        self.frame_janela_mundo.grid_columnconfigure(1, weight=1)
        self.frame_janela_mundo.grid_columnconfigure(2, weight=1)
        self.frame_janela_mundo.grid_columnconfigure(3, weight=1)
        
        self.label_janela_mundo = ctk.CTkLabel(self.frame_janela_mundo, text="Janela Mundo", 
                                            text_color="White", justify="center", font=("Arial", 20))
        self.label_janela_mundo.grid(row=0, column=0, pady=10)
        
        self.label_janela_mundo_xMin = ctk.CTkLabel(self.frame_janela_mundo, text="xMin", 
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_janela_mundo_xMin.grid(row=1, column=0, pady=10)
        
        self.entry_janela_mundo_xMin = ctk.CTkEntry(self.frame_janela_mundo, width=100, placeholder_text=-10)
        self.entry_janela_mundo_xMin.grid(row=1, column=1, pady=10)
        
        self.label_janela_mundo_xMax = ctk.CTkLabel(self.frame_janela_mundo, text="xMax", 
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_janela_mundo_xMax.grid(row=1, column=2, pady=10, padx=10)
        
        self.entry_janela_mundo_xMax = ctk.CTkEntry(self.frame_janela_mundo, width=100, placeholder_text=10)
        self.entry_janela_mundo_xMax.grid(row=1, column=3, pady=10)
        
        self.label_janela_mundo_yMin = ctk.CTkLabel(self.frame_janela_mundo, text="yMin", 
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_janela_mundo_yMin.grid(row=2, column=0, pady=10)
        
        self.entry_janela_mundo_yMin = ctk.CTkEntry(self.frame_janela_mundo, width=100, placeholder_text=-10)
        self.entry_janela_mundo_yMin.grid(row=2, column=1, pady=10)
        
        self.label_janela_mundo_yMax = ctk.CTkLabel(self.frame_janela_mundo, text="yMax", 
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_janela_mundo_yMax.grid(row=2, column=2, pady=10, padx=10)
        
        self.entry_janela_mundo_yMax = ctk.CTkEntry(self.frame_janela_mundo, width=100, placeholder_text=10)
        self.entry_janela_mundo_yMax.grid(row=2, column=3, pady=10)
    
    def sombreamento_Ka(self):
        
        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros do sombreamento Ka
        self.frame_sombreamento_Ka = ctk.CTkFrame(self.frame_parameters)
        self.frame_sombreamento_Ka.grid(row=6, column=0, sticky="nsew")
        
        # Configura o frame do sombreamento Ka para que tenha 3 linhas e 4 colunas
        self.frame_sombreamento_Ka.grid_rowconfigure(0, weight=1)
        self.frame_sombreamento_Ka.grid_rowconfigure(1, weight=1)
        self.frame_sombreamento_Ka.grid_rowconfigure(2, weight=1)
        self.frame_sombreamento_Ka.grid_columnconfigure(0, weight=1)
        self.frame_sombreamento_Ka.grid_columnconfigure(1, weight=1)
        self.frame_sombreamento_Ka.grid_columnconfigure(2, weight=1)
        self.frame_sombreamento_Ka.grid_columnconfigure(3, weight=1)
        
        self.label_sombreamento_Ka = ctk.CTkLabel(self.frame_sombreamento_Ka, text="Ka",
                                            text_color="White", justify="center", font=("Arial", 20))
        self.label_sombreamento_Ka.grid(row=0, column=0, pady=10)
        
        self.label_sombreamento_Ka_r = ctk.CTkLabel(self.frame_sombreamento_Ka, text="R",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_sombreamento_Ka_r.grid(row=1, column=0, pady=10)
        
        self.entry_sombreamento_Ka_r = ctk.CTkEntry(self.frame_sombreamento_Ka, width=100, placeholder_text=0.4)
        self.entry_sombreamento_Ka_r.grid(row=1, column=1, pady=10)
        
        self.label_sombreamento_Ka_g = ctk.CTkLabel(self.frame_sombreamento_Ka, text="G",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_sombreamento_Ka_g.grid(row=1, column=2, pady=10)
        
        self.entry_sombreamento_Ka_g = ctk.CTkEntry(self.frame_sombreamento_Ka, width=100, placeholder_text=0.4)
        self.entry_sombreamento_Ka_g.grid(row=1, column=3, pady=10)
        
        self.label_sombreamento_Ka_b = ctk.CTkLabel(self.frame_sombreamento_Ka, text="B",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_sombreamento_Ka_b.grid(row=1, column=4, pady=10)
        
        self.entry_sombreamento_Ka_b = ctk.CTkEntry(self.frame_sombreamento_Ka, width=100, placeholder_text=0.4)
        self.entry_sombreamento_Ka_b.grid(row=1, column=5, pady=10, padx=10)
        
    def sombreamento_Kd(self):
        
        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros do sombreamento Kd
        self.frame_sombreamento_Kd = ctk.CTkFrame(self.frame_parameters)
        self.frame_sombreamento_Kd.grid(row=7, column=0, sticky="nsew")
        
        # Configura o frame do sombreamento Kd para que tenha 3 linhas e 4 colunas
        self.frame_sombreamento_Kd.grid_rowconfigure(0, weight=1)
        self.frame_sombreamento_Kd.grid_rowconfigure(1, weight=1)
        self.frame_sombreamento_Kd.grid_rowconfigure(2, weight=1)
        self.frame_sombreamento_Kd.grid_columnconfigure(0, weight=1)
        self.frame_sombreamento_Kd.grid_columnconfigure(1, weight=1)
        self.frame_sombreamento_Kd.grid_columnconfigure(2, weight=1)
        self.frame_sombreamento_Kd.grid_columnconfigure(3, weight=1)
        
        self.label_sombreamento_Kd = ctk.CTkLabel(self.frame_sombreamento_Kd, text="Kd",
                                            text_color="White", justify="center", font=("Arial", 20))
        self.label_sombreamento_Kd.grid(row=0, column=0, pady=10)
        
        self.label_sombreamento_Kd_r = ctk.CTkLabel(self.frame_sombreamento_Kd, text="R",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_sombreamento_Kd_r.grid(row=1, column=0, pady=10)
        
        self.entry_sombreamento_Kd_r = ctk.CTkEntry(self.frame_sombreamento_Kd, width=100, placeholder_text=0.7)
        self.entry_sombreamento_Kd_r.grid(row=1, column=1, pady=10)
        
        self.label_sombreamento_Kd_g = ctk.CTkLabel(self.frame_sombreamento_Kd, text="G",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_sombreamento_Kd_g.grid(row=1, column=2, pady=10)
        
        self.entry_sombreamento_Kd_g = ctk.CTkEntry(self.frame_sombreamento_Kd, width=100, placeholder_text=0.7)
        self.entry_sombreamento_Kd_g.grid(row=1, column=3, pady=10)
        
        self.label_sombreamento_Kd_b = ctk.CTkLabel(self.frame_sombreamento_Kd, text="B",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_sombreamento_Kd_b.grid(row=1, column=4, pady=10)
        
        self.entry_sombreamento_Kd_b = ctk.CTkEntry(self.frame_sombreamento_Kd, width=100, placeholder_text=0.7)
        self.entry_sombreamento_Kd_b.grid(row=1, column=5, pady=10, padx=10)
        
    def sombreamento_Ks(self):
        
        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros do sombreamento Ks
        self.frame_sombreamento_Ks = ctk.CTkFrame(self.frame_parameters)
        self.frame_sombreamento_Ks.grid(row=8, column=0, sticky="nsew")
        
        # Configura o frame do sombreamento Ks para que tenha 3 linhas e 4 colunas
        self.frame_sombreamento_Ks.grid_rowconfigure(0, weight=1)
        self.frame_sombreamento_Ks.grid_rowconfigure(1, weight=1)
        self.frame_sombreamento_Ks.grid_rowconfigure(2, weight=1)
        self.frame_sombreamento_Ks.grid_columnconfigure(0, weight=1)
        self.frame_sombreamento_Ks.grid_columnconfigure(1, weight=1)
        self.frame_sombreamento_Ks.grid_columnconfigure(2, weight=1)
        self.frame_sombreamento_Ks.grid_columnconfigure(3, weight=1)
        
        self.label_sombreamento_Ks = ctk.CTkLabel(self.frame_sombreamento_Ks, text="Ks",
                                            text_color="White", justify="center", font=("Arial", 20))
        self.label_sombreamento_Ks.grid(row=0, column=0, pady=10)
        
        self.label_sombreamento_Ks_r = ctk.CTkLabel(self.frame_sombreamento_Ks, text="R",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_sombreamento_Ks_r.grid(row=1, column=0, pady=10)
        
        self.entry_sombreamento_Ks_r = ctk.CTkEntry(self.frame_sombreamento_Ks, width=100, placeholder_text=0.5)
        self.entry_sombreamento_Ks_r.grid(row=1, column=1, pady=10)
        
        self.label_sombreamento_Ks_g = ctk.CTkLabel(self.frame_sombreamento_Ks, text="G",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_sombreamento_Ks_g.grid(row=1, column=2, pady=10)
        
        self.entry_sombreamento_Ks_g = ctk.CTkEntry(self.frame_sombreamento_Ks, width=100, placeholder_text=0.5)
        self.entry_sombreamento_Ks_g.grid(row=1, column=3, pady=10)
        
        self.label_sombreamento_Ks_b = ctk.CTkLabel(self.frame_sombreamento_Ks, text="B",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_sombreamento_Ks_b.grid(row=1, column=4, pady=10)
        
        self.entry_sombreamento_Ks_b = ctk.CTkEntry(self.frame_sombreamento_Ks, width=100, placeholder_text=0.5)
        self.entry_sombreamento_Ks_b.grid(row=1, column=5, pady=10, padx=10)
    
    def luz_ambiente_Ila(self):
        
        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros da luz ambiente Ila
        self.frame_luz_ambiente_Ila = ctk.CTkFrame(self.frame_parameters)
        self.frame_luz_ambiente_Ila.grid(row=9, column=0, sticky="nsew")
        
        # Configura o frame da luz ambiente Ila para que tenha 3 linhas e 4 colunas
        self.frame_luz_ambiente_Ila.grid_rowconfigure(0, weight=1)
        self.frame_luz_ambiente_Ila.grid_rowconfigure(1, weight=1)
        self.frame_luz_ambiente_Ila.grid_rowconfigure(2, weight=1)
        self.frame_luz_ambiente_Ila.grid_columnconfigure(0, weight=1)
        self.frame_luz_ambiente_Ila.grid_columnconfigure(1, weight=1)
        self.frame_luz_ambiente_Ila.grid_columnconfigure(2, weight=1)
        self.frame_luz_ambiente_Ila.grid_columnconfigure(3, weight=1)
        
        self.label_luz_ambiente_Ila = ctk.CTkLabel(self.frame_luz_ambiente_Ila, text="Ila",
                                            text_color="White", justify="center", font=("Arial", 20))
        self.label_luz_ambiente_Ila.grid(row=0, column=0, pady=10)
        
        self.label_luz_ambiente_Ila_r = ctk.CTkLabel(self.frame_luz_ambiente_Ila, text="R",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_luz_ambiente_Ila_r.grid(row=1, column=0, pady=10)
        
        self.entry_luz_ambiente_Ila_r = ctk.CTkEntry(self.frame_luz_ambiente_Ila, width=100, placeholder_text=120)
        self.entry_luz_ambiente_Ila_r.grid(row=1, column=1, pady=10)
        
        self.label_luz_ambiente_Ila_g = ctk.CTkLabel(self.frame_luz_ambiente_Ila, text="G",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_luz_ambiente_Ila_g.grid(row=1, column=2, pady=10)
        
        self.entry_luz_ambiente_Ila_g = ctk.CTkEntry(self.frame_luz_ambiente_Ila, width=100, placeholder_text=120)
        self.entry_luz_ambiente_Ila_g.grid(row=1, column=3, pady=10)
        
        self.label_luz_ambiente_Ila_b = ctk.CTkLabel(self.frame_luz_ambiente_Ila, text="B",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_luz_ambiente_Ila_b.grid(row=1, column=4, pady=10)
        
        self.entry_luz_ambiente_Ila_b = ctk.CTkEntry(self.frame_luz_ambiente_Ila, width=100, placeholder_text=120)
        self.entry_luz_ambiente_Ila_b.grid(row=1, column=5, pady=10, padx=10)
        
    def luz_pontual_Il(self):
        
        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros da luz pontual Il
        self.frame_luz_pontual_Il = ctk.CTkFrame(self.frame_parameters)
        self.frame_luz_pontual_Il.grid(row=10, column=0, sticky="nsew")
        
        # Configura o frame da luz pontual Il para que tenha 3 linhas e 4 colunas
        self.frame_luz_pontual_Il.grid_rowconfigure(0, weight=1)
        self.frame_luz_pontual_Il.grid_rowconfigure(1, weight=1)
        self.frame_luz_pontual_Il.grid_rowconfigure(2, weight=1)
        self.frame_luz_pontual_Il.grid_columnconfigure(0, weight=1)
        self.frame_luz_pontual_Il.grid_columnconfigure(1, weight=1)
        self.frame_luz_pontual_Il.grid_columnconfigure(2, weight=1)
        self.frame_luz_pontual_Il.grid_columnconfigure(3, weight=1)
        
        self.label_luz_pontual_Il = ctk.CTkLabel(self.frame_luz_pontual_Il, text="Il",
                                            text_color="White", justify="center", font=("Arial", 20))
        self.label_luz_pontual_Il.grid(row=0, column=0, pady=10)
        
        self.label_luz_pontual_Il_r = ctk.CTkLabel(self.frame_luz_pontual_Il, text="R",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_luz_pontual_Il_r.grid(row=1, column=0, pady=10)
        
        self.entry_luz_pontual_Il_r = ctk.CTkEntry(self.frame_luz_pontual_Il, width=100, placeholder_text=150)
        self.entry_luz_pontual_Il_r.grid(row=1, column=1, pady=10)
        
        self.label_luz_pontual_Il_g = ctk.CTkLabel(self.frame_luz_pontual_Il, text="G",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_luz_pontual_Il_g.grid(row=1, column=2, pady=10)
        
        self.entry_luz_pontual_Il_g = ctk.CTkEntry(self.frame_luz_pontual_Il, width=100, placeholder_text=150)
        self.entry_luz_pontual_Il_g.grid(row=1, column=3, pady=10)
        
        self.label_luz_pontual_Il_b = ctk.CTkLabel(self.frame_luz_pontual_Il, text="B",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_luz_pontual_Il_b.grid(row=1, column=4, pady=10)

        self.entry_luz_pontual_Il_b = ctk.CTkEntry(self.frame_luz_pontual_Il, width=100, placeholder_text=150)
        self.entry_luz_pontual_Il_b.grid(row=1, column=5, pady=10, padx=10)
        
    def coordenadas_fonte_luz(self):
        
        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros da coordenadas da fonte de luz
        self.frame_coordenadas_fonte_luz = ctk.CTkFrame(self.frame_parameters)
        self.frame_coordenadas_fonte_luz.grid(row=11, column=0, sticky="nsew")
        
        # Configura o frame das coordenadas da fonte de luz para que tenha 3 linhas e 4 colunas
        self.frame_coordenadas_fonte_luz.grid_rowconfigure(0, weight=1)
        self.frame_coordenadas_fonte_luz.grid_rowconfigure(1, weight=1)
        self.frame_coordenadas_fonte_luz.grid_rowconfigure(2, weight=1)
        self.frame_coordenadas_fonte_luz.grid_columnconfigure(0, weight=1)
        self.frame_coordenadas_fonte_luz.grid_columnconfigure(1, weight=1)
        self.frame_coordenadas_fonte_luz.grid_columnconfigure(2, weight=1)
        self.frame_coordenadas_fonte_luz.grid_columnconfigure(3, weight=1)
        
        self.label_coordenadas_fonte_luz = ctk.CTkLabel(self.frame_coordenadas_fonte_luz, text="Coord Luz",
                                            text_color="White", justify="center", font=("Arial", 20))
        self.label_coordenadas_fonte_luz.grid(row=0, column=0, pady=10)
        
        self.label_coordenadas_fonte_luz_x = ctk.CTkLabel(self.frame_coordenadas_fonte_luz, text="x",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_coordenadas_fonte_luz_x.grid(row=1, column=0, pady=10)
        
        self.entry_coordenadas_fonte_luz_x = ctk.CTkEntry(self.frame_coordenadas_fonte_luz, width=100, placeholder_text=70)
        self.entry_coordenadas_fonte_luz_x.grid(row=1, column=1, pady=10)
        
        self.label_coordenadas_fonte_luz_y = ctk.CTkLabel(self.frame_coordenadas_fonte_luz, text="y",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_coordenadas_fonte_luz_y.grid(row=1, column=2, pady=10)
        
        self.entry_coordenadas_fonte_luz_y = ctk.CTkEntry(self.frame_coordenadas_fonte_luz, width=100, placeholder_text=20)
        self.entry_coordenadas_fonte_luz_y.grid(row=1, column=3, pady=10)
        
        self.label_coordenadas_fonte_luz_z = ctk.CTkLabel(self.frame_coordenadas_fonte_luz, text="z",
                                            text_color="White", justify="center", font=("Arial", 15))
        self.label_coordenadas_fonte_luz_z.grid(row=1, column=4, pady=10)
        
        self.entry_coordenadas_fonte_luz_z = ctk.CTkEntry(self.frame_coordenadas_fonte_luz, width=100, placeholder_text=35)
        self.entry_coordenadas_fonte_luz_z.grid(row=1, column=5, pady=10, padx=10)
    
    def n(self):
        
        # Cria um frame para o CTkScrollableFrame aonde ficará os parâmetros de n
        self.frame_n = ctk.CTkFrame(self.frame_parameters)
        self.frame_n.grid(row=12, column=0, sticky="nsew")
        
        # Configura o frame de n para que tenha 2 linhas e 2 colunas
        self.frame_n.grid_rowconfigure(0, weight=1)
        self.frame_n.grid_rowconfigure(1, weight=1)
        self.frame_n.grid_columnconfigure(0, weight=1)  

        self.label_n = ctk.CTkLabel(self.frame_n, text="n",
                                            text_color="White", justify="center", font=("Arial", 20))
        self.label_n.grid(row=0, column=0, pady=10)
        
        self.entry_n = ctk.CTkEntry(self.frame_n, width=100, placeholder_text=2.15)
        self.entry_n.grid(row=1, column=0, pady=10)
    
    def get_values(self, event):
        
        def verificacao_valores_entry():
            
            # Verificação da view_port
            if self.entry_view_port_uMin.get() == "":
                self.entry_view_port_uMin.insert(0, 0)
            if self.entry_view_port_uMax.get() == "":
                self.entry_view_port_uMax.insert(0, 800)
            if self.entry_view_port_vMin.get() == "":
                self.entry_view_port_vMin.insert(0, 0)
            if self.entry_view_port_vMax.get() == "":
                self.entry_view_port_vMax.insert(0, 800)
                
            # Verificação da view_up
            if self.entry_view_up_x.get() == "":
                self.entry_view_up_x.insert(0, 0)
            if self.entry_view_up_y.get() == "":
                self.entry_view_up_y.insert(0, 1)
            if self.entry_view_up_z.get() == "":
                self.entry_view_up_z.insert(0, 0)
                
            # Verificação da vrp
            if self.entry_vrp_x.get() == "":
                self.entry_vrp_x.insert(0, 0)
            if self.entry_vrp_y.get() == "":
                self.entry_vrp_y.insert(0, 10)
            if self.entry_vrp_z.get() == "":
                self.entry_vrp_z.insert(0, 10)
                
            # Verificação do ponto focal
            if self.entry_ponto_focal_x.get() == "":
                self.entry_ponto_focal_x.insert(0, 0)
            if self.entry_ponto_focal_y.get() == "":
                self.entry_ponto_focal_y.insert(0, 0)
            if self.entry_ponto_focal_z.get() == "":
                self.entry_ponto_focal_z.insert(0, 0)
                
            # Verificação da distância ao plano
            if self.entry_distancia_ao_plano_projecao.get() == "":
                self.entry_distancia_ao_plano_projecao.insert(0, 10)
            if self.entry_distancia_ao_plano_near.get() == "":
                self.entry_distancia_ao_plano_near.insert(0, 5)
            if self.entry_distancia_ao_plano_far.get() == "":
                self.entry_distancia_ao_plano_far.insert(0, 15)    
              
            # Verificação da janela mundo
            if self.entry_janela_mundo_xMin.get() == "":
                self.entry_janela_mundo_xMin.insert(0, -10)
            if self.entry_janela_mundo_xMax.get() == "":
                self.entry_janela_mundo_xMax.insert(0, 10)
            if self.entry_janela_mundo_yMin.get() == "":
                self.entry_janela_mundo_yMin.insert(0, -10)
            if self.entry_janela_mundo_yMax.get() == "":
                self.entry_janela_mundo_yMax.insert(0, 10)                
            
            # Verificação do sombreamento Ka
            if self.entry_sombreamento_Ka_r.get() == "":
                self.entry_sombreamento_Ka_r.insert(0, 0.4)
            if self.entry_sombreamento_Ka_g.get() == "":
                self.entry_sombreamento_Ka_g.insert(0, 0.4)
            if self.entry_sombreamento_Ka_b.get() == "":
                self.entry_sombreamento_Ka_b.insert(0, 0.4)
                
            # Verificação do sombreamento Kd
            if self.entry_sombreamento_Kd_r.get() == "":
                self.entry_sombreamento_Kd_r.insert(0, 0.7)
            if self.entry_sombreamento_Kd_g.get() == "":
                self.entry_sombreamento_Kd_g.insert(0, 0.7)
            if self.entry_sombreamento_Kd_b.get() == "":
                self.entry_sombreamento_Kd_b.insert(0, 0.7)
                
            # Verificação do sombreamento Ks
            if self.entry_sombreamento_Ks_r.get() == "":
                self.entry_sombreamento_Ks_r.insert(0, 0.5)
            if self.entry_sombreamento_Ks_g.get() == "":
                self.entry_sombreamento_Ks_g.insert(0, 0.5)
            if self.entry_sombreamento_Ks_b.get() == "":
                self.entry_sombreamento_Ks_b.insert(0, 0.5)
             
            # Verificação da luz ambiente Ila
            if self.entry_luz_ambiente_Ila_r.get() == "":
                self.entry_luz_ambiente_Ila_r.insert(0, 120)
            if self.entry_luz_ambiente_Ila_g.get() == "":
                self.entry_luz_ambiente_Ila_g.insert(0, 120)
            if self.entry_luz_ambiente_Ila_b.get() == "":
                self.entry_luz_ambiente_Ila_b.insert(0, 120)
                
            # Verificação da luz pontual Il
            if self.entry_luz_pontual_Il_r.get() == "":
                self.entry_luz_pontual_Il_r.insert(0, 150)
            if self.entry_luz_pontual_Il_g.get() == "":
                self.entry_luz_pontual_Il_g.insert(0, 150)
            if self.entry_luz_pontual_Il_b.get() == "":
                self.entry_luz_pontual_Il_b.insert(0, 150)
                
            # Verificação das coordenadas da fonte de luz
            if self.entry_coordenadas_fonte_luz_x.get() == "":
                self.entry_coordenadas_fonte_luz_x.insert(0, 70)
            if self.entry_coordenadas_fonte_luz_y.get() == "":
                self.entry_coordenadas_fonte_luz_y.insert(0, 20)
            if self.entry_coordenadas_fonte_luz_z.get() == "":
                self.entry_coordenadas_fonte_luz_z.insert(0, 35)   
                
            # Verificação de n
            if self.entry_n.get() == "":
                self.entry_n.insert(0, 2.15)
                
        # Verificação dos entrys
        verificacao_valores_entry()
    
        # Pega os valores dos entrys -> Apenas por conveniência
        uMin = int(self.entry_view_port_uMin.get())
        uMax = int(self.entry_view_port_uMax.get())
        vMin = int(self.entry_view_port_vMin.get())
        vMax = int(self.entry_view_port_vMax.get())    
        
        view_up_x = int(self.entry_view_up_x.get())
        view_up_y = int(self.entry_view_up_y.get())
        view_up_z = int(self.entry_view_up_z.get())
        
        vrp_x = int(self.entry_vrp_x.get())
        vrp_y = int(self.entry_vrp_y.get())
        vrp_z = int(self.entry_vrp_z.get())
        
        ponto_focal_x = int(self.entry_ponto_focal_x.get())
        ponto_focal_y = int(self.entry_ponto_focal_y.get())
        ponto_focal_z = int(self.entry_ponto_focal_z.get())
        
        dp = int(self.entry_distancia_ao_plano_projecao.get())
        near = int(self.entry_distancia_ao_plano_near.get())
        far = int(self.entry_distancia_ao_plano_far.get())
                
        janela_mundo_xMin = int(self.entry_janela_mundo_xMin.get())
        janela_mundo_xMax = int(self.entry_janela_mundo_xMax.get())
        janela_mundo_yMin = int(self.entry_janela_mundo_yMin.get())
        janela_mundo_yMax = int(self.entry_janela_mundo_yMax.get())
        
        sombreamento_Ka_r = float(self.entry_sombreamento_Ka_r.get())
        sombreamento_Ka_g = float(self.entry_sombreamento_Ka_g.get())
        sombreamento_Ka_b = float(self.entry_sombreamento_Ka_b.get())
        
        sombreamento_Kd_r = float(self.entry_sombreamento_Kd_r.get())
        sombreamento_Kd_g = float(self.entry_sombreamento_Kd_g.get())
        sombreamento_Kd_b = float(self.entry_sombreamento_Kd_b.get())
        
        sombreamento_Ks_r = float(self.entry_sombreamento_Ks_r.get())
        sombreamento_Ks_g = float(self.entry_sombreamento_Ks_g.get())
        sombreamento_Ks_b = float(self.entry_sombreamento_Ks_b.get())
        
        luz_ambiente_Ila_r = float(self.entry_luz_ambiente_Ila_r.get())
        luz_ambiente_Ila_g = float(self.entry_luz_ambiente_Ila_g.get())
        luz_ambiente_Ila_b = float(self.entry_luz_ambiente_Ila_b.get())
        
        luz_pontual_Il_r = float(self.entry_luz_pontual_Il_r.get())
        luz_pontual_Il_g = float(self.entry_luz_pontual_Il_g.get())
        luz_pontual_Il_b = float(self.entry_luz_pontual_Il_b.get())
        
        coordenadas_fonte_luz_x = int(self.entry_coordenadas_fonte_luz_x.get())
        coordenadas_fonte_luz_y = int(self.entry_coordenadas_fonte_luz_y.get())
        coordenadas_fonte_luz_z = int(self.entry_coordenadas_fonte_luz_z.get())
        
        n = float(self.entry_n.get())
    
        # Verifica o tipo de projeção, para depois calcular as matrizes
        if self.radio_var_projecao.get() == 0:
                
            # Calcula a matriz de transformação Msru_src
            self.Matrix_sru_src = Msru_src(vrp_x, vrp_y, vrp_z, 
                                ponto_focal_x, ponto_focal_y, ponto_focal_z, 
                                view_up_x, view_up_y, view_up_z)
            
            # Calcula a matriz de projeção
            self.Matrix_proj = Mproj_perspectiva(dp)
            
            # Calcula a matriz de janela de projeção
            self.Matrix_jp = Mjp(uMin, uMax, vMin, vMax,
                        janela_mundo_xMin, janela_mundo_xMax, janela_mundo_yMin, janela_mundo_yMax)
            
            # Calcula a matriz de transformação Msru_srt
            self.Matrix_sru_srt = Msru_srt(self.Matrix_sru_src, self.Matrix_proj, self.Matrix_jp)
           
        elif self.radio_var_projecao.get() == 1:
                
            # Calcula a matriz de transformação Msru_src
            self.Matrix_sru_src = Msru_src(vrp_x, vrp_y, vrp_z, 
                                ponto_focal_x, ponto_focal_y, ponto_focal_z, 
                                view_up_x, view_up_y, view_up_z)
            
            # Calcula a matriz de projeção
            self.Matrix_proj = Mproj_paralela()
            
            # Calcula a matriz de janela de projeção
            self.Matrix_jp = Mjp(uMin, uMax, vMin, vMax,
                        janela_mundo_xMin, janela_mundo_xMax, janela_mundo_yMin, janela_mundo_yMax)
            
            # Calcula a matriz de transformação Msru_srt
            self.Matrix_sru_srt = Msru_srt(self.Matrix_sru_src, self.Matrix_proj, self.Matrix_jp)
          
        # PRINTA AS MATRIZES
        print("Matriz de transformação Msru_src: \n", self.Matrix_sru_src)
        print("\n\nMatriz de projeção: \n", self.Matrix_proj)  
        print("\n\nMatriz de janela de projeção: \n", self.Matrix_jp)
        print("\n\nMatriz de transformação Msru_srt: \n", self.Matrix_sru_srt)
          
        # # Pega a primeira mesh da lista de meshes
        # mesh = self.files_classes[0].mesh

        # # Iterar sobre todas as faces
        # for fh in mesh.faces():
        #     # Obter os vértices de cada face
        #     vertices = [vh.idx() for vh in mesh.fv(fh)]
        #     print("Face inicial: ", vertices)      
    
        # # Iterar sobre todos os vértices
        # for vh in mesh.vertices():
        #     # Obter a posição de cada vértice
        #     position = mesh.point(vh)
        #     print("Vértice inicial: ", position)
            
        mesh_objetos_modificado = []
        # Computa os vertices com a matriz de transformação obtida anteriomente
        for i in range(len(self.files_classes)):
            
            # Separa a mash do objeto (apenas por conveniência)
            mesh = copy.deepcopy(self.files_classes[i].mesh)
            
            mesh_mod = computacao_dos_vertices(mesh, self.Matrix_sru_srt)
           
            mesh_objetos_modificado.append(mesh_mod)

       
        #  # Pega a primeira mesh da lista de meshes
        # mesh = mesh_objetos_modificado[0]

        # # Iterar sobre todas as faces
        # for fh in mesh.faces():
        #     # Obter os vértices de cada face
        #     vertices = [vh.idx() for vh in mesh.fv(fh)]
        #     print("Face: ", vertices)      
    
        # # Iterar sobre todos os vértices
        # for vh in mesh.vertices():
        #     # Obter a posição de cada vértice
        #     position = mesh.point(vh)
        #     print("Vértice: ", position)
        
        
        # Visualiza se as faces das mash são visiveis, passando por todas
        # dentro da lista mesh_objetos_modificado
        mesh_objetos_modificado_verificacao_faces = []
        for mesh in mesh_objetos_modificado:
            
            # Verifica se as faces são visíveis
            mesh_objetos_modificado_verificacao_faces.append(verifica_faces_visiveis(mesh, vrp_x, vrp_y, vrp_z, ponto_focal_x, ponto_focal_y, ponto_focal_z))
        
        
        # # # Pega a primeira mesh da lista de meshes
        # mesh = mesh_objetos_modificado[0]

        # # Iterar sobre todas as faces
        # for fh in mesh.faces():
        #     # Obter os vértices de cada face
        #     vertices = [vh.idx() for vh in mesh.fv(fh)]
        #     print("Face inicial: ", vertices)      
    
        # # Iterar sobre todos os vértices
        # for vh in mesh.vertices():
        #     # Obter a posição de cada vértice
        #     position = mesh.point(vh)
        #     print("Vértice inicial: ", position)
    
    
        # Aplicação do sombreamento constante
        mesh_objeto_modificado_sombreamento = []
        for i in range(len(mesh_objetos_modificado_verificacao_faces)):
            
            # Aplica uma copia da mesh modificada
            mesh_objeto_sombreamento = copy.deepcopy(mesh_objetos_modificado_verificacao_faces[i])
            
            print(mesh_objeto_sombreamento)
            
            # Percorre todas as faces da mesh
            for fh in mesh_objetos_modificado[i].faces():
                
                mesh_objeto_sombreamento = aplicacao_sombreamento(mesh_objetos_modificado[i], fh, 
                                                                vrp_x, vrp_y, vrp_z,
                                                                luz_ambiente_Ila_r, luz_ambiente_Ila_g, luz_ambiente_Ila_b,
                                                                luz_pontual_Il_r, luz_pontual_Il_g, luz_pontual_Il_b,
                                                                coordenadas_fonte_luz_x, coordenadas_fonte_luz_y, coordenadas_fonte_luz_z,
                                                                sombreamento_Ka_r, sombreamento_Ka_g, sombreamento_Ka_b,
                                                                sombreamento_Kd_r, sombreamento_Kd_g, sombreamento_Kd_b,
                                                                sombreamento_Ks_r, sombreamento_Ks_g, sombreamento_Ks_b, n)
                                        
            # Adiciona a mesh modificada com o sombreamento constante
            mesh_objeto_modificado_sombreamento.append(mesh_objeto_sombreamento)
              
        # # # Pega a primeira mesh da lista de mesheswsl
        # # mesh = mesh_objeto_modificado_sombreamento[0] 
        # # # Iterate over all faces and print their colors
        # # for fh in mesh.faces():
        # #     color = mesh.color(fh)
        # #     print(f"Face {fh.idx()}: Color {color}")                                  
                                   
        # # Computa os vertices com a matriz de transformação obtida anteriomente
        # for i in range(len(mesh_objeto_modificado_sombreamento)):
        #     mesh_objeto_modificado_sombreamento[i] = computacao_dos_vertices(mesh_objeto_modificado_sombreamento[i], self.Matrix_sru_srt)
        
        
        # Pega a primeira mesh da lista de meshes
        mesh = mesh_objeto_modificado_sombreamento[0]
        
        # Iterar sobre todas as faces
        for fh in mesh.faces():
            # Obter os vértices de cada face
            vertices = [vh.idx() for vh in mesh.fv(fh)]
            print("Face final: ", vertices)      
    
        # Iterar sobre todos os vértices
        for vh in mesh.vertices():
            # Obter a posição de cada vértice
            position = mesh.point(vh)
            print("Vértice final: ", position)
            
        # Substitui a mesh original pela mesh modificada
        # A função está dentro do objeto da classe
        for objeto in range(len(self.files_classes)):
            self.files_classes[objeto].mesh = mesh_objeto_modificado_sombreamento[objeto]
            
        # Para pintar
        self.fill_color = True
     
    def print_values(self, event):
            
        console = Console()
        
        # Printa os valores dos entrys com o rich em formato de tabela
        # -> View-Port
        table = Table(title="View-Port", show_edge=True)
        table.add_column("Parâmetro", justify="center", style="cyan", no_wrap=True)
        table.add_column("Valor", justify="center", style="magenta", no_wrap=True)
        table.add_row("uMin", self.entry_view_port_uMin.get())
        table.add_row("uMax", self.entry_view_port_uMax.get())
        table.add_row("vMin", self.entry_view_port_vMin.get())
        table.add_row("vMax", self.entry_view_port_vMax.get())
        console.print(table)
        
        # -> View-Up
        table = Table(title="View-Up", show_edge=True)
        table.add_column("Parâmetro", justify="center", style="cyan", no_wrap=True)
        table.add_column("Valor", justify="center", style="magenta", no_wrap=True)
        table.add_row("x", self.entry_view_up_x.get())
        table.add_row("y", self.entry_view_up_y.get())
        table.add_row("z", self.entry_view_up_z.get())
        console.print(table)
        
        # -> VRP
        table = Table(title="VRP", show_edge=True)
        table.add_column("Parâmetro", justify="center", style="cyan", no_wrap=True)
        table.add_column("Valor", justify="center", style="magenta", no_wrap=True)
        table.add_row("x", self.entry_vrp_x.get())
        table.add_row("y", self.entry_vrp_y.get())
        table.add_row("z", self.entry_vrp_z.get())
        console.print(table)
        
        # -> Ponto Focal
        table = Table(title="Ponto Focal", show_edge=True)
        table.add_column("Parâmetro", justify="center", style="cyan", no_wrap=True)
        table.add_column("Valor", justify="center", style="magenta", no_wrap=True)
        table.add_row("x", self.entry_ponto_focal_x.get())
        table.add_row("y", self.entry_ponto_focal_y.get())
        table.add_row("z", self.entry_ponto_focal_z.get())
        console.print(table)
        
        # -> Distância ao Plano
        table = Table(title="Distância ao Plano", show_edge=True)
        table.add_column("Parâmetro", justify="center", style="cyan", no_wrap=True)
        table.add_column("Valor", justify="center", style="magenta", no_wrap=True)
        table.add_row("DP", self.entry_distancia_ao_plano_projecao.get())
        console.print(table)
        
        # -> Janela Mundo
        table = Table(title="Janela Mundo", show_edge=True)
        table.add_column("Parâmetro", justify="center", style="cyan", no_wrap=True)
        table.add_column("Valor", justify="center", style="magenta", no_wrap=True)
        table.add_row("xMin", self.entry_janela_mundo_xMin.get())
        table.add_row("xMax", self.entry_janela_mundo_xMax.get())
        table.add_row("yMin", self.entry_janela_mundo_yMin.get())
        table.add_row("yMax", self.entry_janela_mundo_yMax.get())
        console.print(table)
        
        # Printa os valores das matrizes com o rich em formato de tabela
        table = Table(title="Matrizes do Pipeline", show_edge=True)
        table.add_column("Matriz", justify="center", style="cyan", no_wrap=True)
        table.add_column("Valores", justify="center", style="magenta", no_wrap=True)
        table.add_row("Matriz -> sru_src", str(self.Matrix_sru_src))
        table.add_row("\n", "\n")
        table.add_row("Matriz -> projeção", str(self.Matrix_proj))
        table.add_row("\n", "\n")
        table.add_row("Matriz -> janela de projeção", str(self.Matrix_jp))
        table.add_row("\n", "\n")
        table.add_row("Matriz -> sru_srt", str(self.Matrix_sru_srt))
        table.add_row("\n", "\n")
        table.add_row("Matriz -> sru_srt homogenizada", str(self.Msru_srt_homogenizado))
        console.print(table)
        
    def plota_grafico(self, event):
        
        # Cria um subplot dependendo do número de classes criadas na lista
        # files_classes

        # Testa se o evento é o F9
        if event.keysym == "F9":
            
            # Número de subplots, no caso é o número de classes de objetos
            n_subplots = len(self.files_classes)

            # Cria os subplots 2D na parte de cima
            fig, axs = plt.subplots(2, n_subplots)

            # Adiciona um título ao subplot
            fig.suptitle('Visualização dos Objetos 2D e 3D')

            for ax in axs.flat:
                
                # Retira as bordas dos subplots
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)
                ax.spines['bottom'].set_visible(False) 
                
                # Retira os eixos dos subplots
                ax.get_xaxis().set_visible(False)
                ax.get_yaxis().set_visible(False)
                
            
            # Verifica se o número na lista files_classes é igual a 1
            if (n_subplots == 1):
                
                # Plota os pontos x e y nos gráficos 2D
                axs[0].plot(self.files_classes[0].x, self.files_classes[0].y)

                # Transforma os subplots da parte de baixo em 3D
                axs[1] = fig.add_subplot(2, n_subplots, n_subplots+1, projection='3d')

                # Plota os pontos x, y, z
                axs[1].plot_surface(self.files_classes[0].xn, self.files_classes[0].yn, self.files_classes[0].zn)
            
                # Coloca os eixos x, y e z nos gráficos 3D
                axs[1].set_xlabel('X')
                axs[1].set_ylabel('Y')
                axs[1].set_zlabel('Z')
                
            else:
                
                for i in range(n_subplots):
                    
                    # Plota os pontos x e y nos gráficos 2D
                    axs[0, i].plot(self.files_classes[i].x, self.files_classes[i].y)

                    # Transforma os subplots da parte de baixo em 3D
                    axs[1, i] = fig.add_subplot(2, n_subplots, n_subplots+i+1, projection='3d')

                    # Plota os pontos x, y e z nos gráficos 3D
                    axs[1, i].plot_surface(self.files_classes[i].xn, self.files_classes[i].yn, self.files_classes[i].zn)

            # Cria um canvas para o gráfico
            self.canvas_grafico = FigureCanvasTkAgg(fig, master=self.app)
            self.canvas_grafico.draw()
            self.canvas_grafico.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        elif event.keysym == "F10":
            # Deleta o canvas do gráfico
            self.canvas_grafico.get_tk_widget().destroy()