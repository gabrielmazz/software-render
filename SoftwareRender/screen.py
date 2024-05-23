import customtkinter as ctk
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from SoftwareRender.pipeline.pipeline import Msru_src, Mproj_perspectiva, Mproj_paralela, Mjp, Msru_srt
from SoftwareRender.transformações_geometricas.transformacoes import translacao, escala, rotacao_x, rotacao_y, rotacao_z

# Variáveis para os parâmetros, no caso é uma lista com os valores
# obtidos nos entrys do tkinter
global world_list, view_port_list, view_up_list, vrp_list, ponto_focal_list, distancia_ao_plano_list, janela_mundo_list

world_list, view_port_list, view_up_list, vrp_list, ponto_focal_list, distancia_ao_plano_list, janela_mundo_list = [], [], [], [], [], [], []

class Screen():
    
    def __init__(self, files_classes):
        
        super().__init__()
        
        # Define a lista de classes de objetos
        self.files_classes = files_classes
        
        # Define a aparência da tela principal como dark
        ctk.set_appearance_mode("dark")
        
        self.app = ctk.CTk()
        self.app.title("T02 - Software Render")
        self.app.geometry("1610x900")

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
        
        # Plota os objetos no canvas
        self.plota_objetos()
        
    def run(self):
        
        # Cria as binds para os botões
        self.binds()
        
        self.app.mainloop()
    
    def quit(self, event=None):
        self.app.quit()  
    
    def binds(self):
        
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
               
    def grid_canvas_column(self):
        
        # Define a configuração de colunas, dividindo em 2
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=1)

        # Cria um canvas para a tela principal
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
        opcoes = ["Objeto " + str(i+1) for i in range(len(self.files_classes))]
        
        self.label_objeto = ctk.CTkLabel(self.frame_objeto, text="Seleção de Objetos",
                                        text_color="White", justify="center", font=("Arial", 15))
        self.label_objeto.grid(row=0, column=0, padx=10, pady=10)    
        
        optionmenu_var = ctk.StringVar(value="Objeto 1")
        self.opcao_menu = ctk.CTkOptionMenu(self.frame_objeto, values=opcoes,
                                            variable=optionmenu_var)
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
        
        # self.label_distancia_ao_plano_near = ctk.CTkLabel(self.frame_distancia_ao_plano, text="Near",
        #                                     text_color="White", justify="center", font=("Arial", 15))
        
        # self.label_distancia_ao_plano_near.grid(row=1, column=2, pady=10, padx=10)
        
        # self.entry_distancia_ao_plano_near = ctk.CTkEntry(self.frame_distancia_ao_plano, width=100, placeholder_text=5)
        # self.entry_distancia_ao_plano_near.grid(row=1, column=3, pady=10)
        
        # self.label_distancia_ao_plano_far = ctk.CTkLabel(self.frame_distancia_ao_plano, text="Far",
        #                                     text_color="White", justify="center", font=("Arial", 15))
        
        # self.label_distancia_ao_plano_far.grid(row=2, column=0, pady=10)
        
        # self.entry_distancia_ao_plano_far = ctk.CTkEntry(self.frame_distancia_ao_plano, width=100, placeholder_text=15)
        # self.entry_distancia_ao_plano_far.grid(row=2, column=1, pady=10)
                                                              
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
      
    def print_values(self, event):
            
        # Printa os valores obtidos nos entrys
        print("Valores obtidos nos entrys")
        print("View-Port: ", view_port_list)
        print("View-Up: ", view_up_list)
        print("VRP: ", vrp_list)
        print("Ponto Focal: ", ponto_focal_list)
        print("Distância ao Plano: ", distancia_ao_plano_list)
        print("Janela Mundo: ", janela_mundo_list)
    
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
                
            # Verificação da janela mundo
            if self.entry_janela_mundo_xMin.get() == "":
                self.entry_janela_mundo_xMin.insert(0, -10)
            if self.entry_janela_mundo_xMax.get() == "":
                self.entry_janela_mundo_xMax.insert(0, 10)
            if self.entry_janela_mundo_yMin.get() == "":
                self.entry_janela_mundo_yMin.insert(0, -10)
            if self.entry_janela_mundo_yMax.get() == "":
                self.entry_janela_mundo_yMax.insert(0, 10)                
            
            # ...
        
        # Limpa as listas de parâmetros
        view_port_list.clear()
        view_up_list.clear()
        vrp_list.clear()
        ponto_focal_list.clear()
        distancia_ao_plano_list.clear()
        janela_mundo_list.clear()
        
        # Verificaçãp dos entrys
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
        
        janela_mundo_xMin = int(self.entry_janela_mundo_xMin.get())
        janela_mundo_xMax = int(self.entry_janela_mundo_xMax.get())
        janela_mundo_yMin = int(self.entry_janela_mundo_yMin.get())
        janela_mundo_yMax = int(self.entry_janela_mundo_yMax.get())
        
        
        # Verifica o tipo de projeção, para depois calcular as matrizes
        if self.radio_var_projecao.get() == 0:
                
            # Calcula a matriz de transformação Msru_src
            Matrix_sru_src = Msru_src(vrp_x, vrp_y, vrp_z, 
                                ponto_focal_x, ponto_focal_y, ponto_focal_z, 
                                view_up_x, view_up_y, view_up_z)
            
            # Calcula a matriz de projeção
            Matrix_proj = Mproj_perspectiva(dp)
            
            # Calcula a matriz de janela de projeção
            Matrix_jp = Mjp(uMin, uMax, vMin, vMax,
                        janela_mundo_xMin, janela_mundo_xMax, janela_mundo_yMin, janela_mundo_yMax)
            
            # Calcula a matriz de transformação Msru_srt
            Matrix_sru_srt = Msru_srt(Matrix_sru_src, Matrix_proj, Matrix_jp)
        
        
        elif self.radio_var_projecao.get() == 1:
                
            # Calcula a matriz de transformação Msru_src
            Matrix_sru_src = Msru_src(vrp_x, vrp_y, vrp_z, 
                                ponto_focal_x, ponto_focal_y, ponto_focal_z, 
                                view_up_x, view_up_y, view_up_z)
            
            # Calcula a matriz de projeção
            Matrix_proj = Mproj_paralela()
            
            # Calcula a matriz de janela de projeção
            Matrix_jp = Mjp(uMin, uMax, vMin, vMax,
                        janela_mundo_xMin, janela_mundo_xMax, janela_mundo_yMin, janela_mundo_yMax)
            
            # Calcula a matriz de transformação Msru_srt
            Matrix_sru_srt = Msru_srt(Matrix_sru_src, Matrix_proj, Matrix_jp)
    
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

                # Plota os pontos x, y e z nos gráficos 3D
                axs[1].plot_surface(self.files_classes[0].xn, self.files_classes[0].yn, self.files_classes[0].zn)
            
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
         
    def plota_objetos(self):
        
        # Plota um cubo na tela
        def cube3D(x1, y1, x2, y2, depth, fcolor="black", bcolor="grey"):
            self.canvas.create_line(x1, y2, x1+depth, y2-depth, fill=fcolor)
            self.canvas.create_line(x1+depth, y2-depth, x1+depth, y1-depth, fill=fcolor)
            self.canvas.create_line(x1+depth, y2-depth, x2+depth, y2-depth, fill=fcolor)
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=fcolor, fill=bcolor)
            self.canvas.create_line(x1, y1, x1+depth, y1-depth, fill=fcolor)
            self.canvas.create_line(x1+depth, y1-depth, x2+depth, y1-depth, fill=fcolor)
            self.canvas.create_line(x2+depth, y1-depth, x2+depth, y2-depth, fill=fcolor)
            self.canvas.create_line(x2+depth, y1-depth, x2, y1, fill=fcolor)
            self.canvas.create_line(x2+depth, y2-depth, x2, y2, fill=fcolor)
        
        # -> Está função pega os pontos xn, yn, zn e plota no canvas. No caso
        #    eles estão armazenados no files_classes que é uma lista de objetos
        #    todos contendo os pontos dos arquivos de pontos_3d -> xn, yn e zn
        
        cube3D(100, 100, 250, 200, 50)
        