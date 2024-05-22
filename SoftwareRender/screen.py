import customtkinter as ctk
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        self.app.title("Custom Tkinter")
        self.app.geometry("1610x900")

        # Define o grid da tela (tela inteira)
        self.grid_canvas_column()

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
        
        # Limpa as listas de parâmetros
        view_port_list.clear()
        view_up_list.clear()
        vrp_list.clear()
        ponto_focal_list.clear()
        distancia_ao_plano_list.clear()
        janela_mundo_list.clear()
            
        # Pega os valores dos entrys e armazena nas listas de parâmetros
        view_port_list.append([int(self.entry_view_port_uMin.get()), int(self.entry_view_port_uMax.get()), 
                            int(self.entry_view_port_vMin.get()), int(self.entry_view_port_vMax.get())])
        
        view_up_list.append([int(self.entry_view_up_x.get()), int(self.entry_view_up_y.get()), int(self.entry_view_up_z.get())])
        
        vrp_list.append([int(self.entry_vrp_x.get()), int(self.entry_vrp_y.get()), int(self.entry_vrp_z.get())])
        
        ponto_focal_list.append([int(self.entry_ponto_focal_x.get()), int(self.entry_ponto_focal_y.get()), int(self.entry_ponto_focal_z.get())])
        
        distancia_ao_plano_list.append([int(self.entry_distancia_ao_plano_projecao.get()), int(self.entry_distancia_ao_plano_near.get()), int(self.entry_distancia_ao_plano_far.get())])
        
        janela_mundo_list.append([int(self.entry_janela_mundo_xMin.get()), int(self.entry_janela_mundo_xMax.get()), 
                                int(self.entry_janela_mundo_yMin.get()), int(self.entry_janela_mundo_yMax.get())])
        
    def grid_canvas_column(self):
        
        # Define a configuração de colunas, dividindo em 2
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)
        
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
        
        self.label_distancia_ao_plano_projecao = ctk.CTkLabel(self.frame_distancia_ao_plano, text="Projeção",
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
        