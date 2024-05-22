import customtkinter as ctk


class Screen():
    
    def __init__(self):
        
        super().__init__()
        
        # Define a aparência da tela principal como dark
        ctk.set_appearance_mode("dark")
        
        self.app = ctk.CTk()
        self.app.title("Custom Tkinter")
        self.app.geometry("1610x900")

        self.grid_canvas_column()
        self.parameters_world()


        
    def run(self):
        self.app.mainloop()
        
    def grid_canvas_column(self):
        
        # Define a configuração de linhas, dividindo a tela em 2 partes
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=1)
        
        # Cria um frame para o canvas
        self.frame_canvas = ctk.CTkFrame(self.app, width=1590, height=500)
        self.frame_canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Cria um frame para os widgets
        self.frame_widgets = ctk.CTkFrame(self.app, width=1590, height=200)
        self.frame_widgets.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Cria 3 colunas no frame dos widgets
        self.frame_widgets.grid_columnconfigure(0, weight=1)
        self.frame_widgets.grid_columnconfigure(1, weight=1)
        self.frame_widgets.grid_columnconfigure(2, weight=1)
        
        # Cria o primeiro frame do widgets (Dados do mundo)
        self.frame_widgets_1 = ctk.CTkFrame(self.frame_widgets, width=100, height=200)
        self.frame_widgets_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Cria o segundo frame do widgets (Dados do objeto)
        self.frame_widgets_2 = ctk.CTkFrame(self.frame_widgets)
        self.frame_widgets_2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Cria o terceiro frame do widgets (Sombreamento)
        self.frame_widgets_3 = ctk.CTkFrame(self.frame_widgets)
        self.frame_widgets_3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
    
    
    def parameters_world(self):
        
        # Tudo oque será feito aqui, será relacionado ao frame_widgets_1
        
        # Dividir o frame_widgets_1 em 2 colunas e 3 linhas
        self.frame_widgets_1.grid_columnconfigure(0, weight=1)
        self.frame_widgets_1.grid_columnconfigure(1, weight=1)
        self.frame_widgets_1.grid_rowconfigure(0, weight=1)
        self.frame_widgets_1.grid_rowconfigure(1, weight=1)
        self.frame_widgets_1.grid_rowconfigure(2, weight=1)
        
        # Cria o primeiro frame do frame_widgets_1 (Dados do mundo)
        # -> 2 linha, 1 coluna
        self.frame_widgets_1_1 = ctk.CTkFrame(self.frame_widgets_1)
        self.frame_widgets_1_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configura o frame_widgets_1_1 para ter 4 coluna e 2 linhas
        self.frame_widgets_1_1.grid_columnconfigure(0, weight=1)
        self.frame_widgets_1_1.grid_columnconfigure(1, weight=1)
        self.frame_widgets_1_1.grid_columnconfigure(2, weight=1)
        self.frame_widgets_1_1.grid_columnconfigure(3, weight=1)
        self.frame_widgets_1_1.grid_rowconfigure(0, weight=1)
        self.frame_widgets_1_1.grid_rowconfigure(1, weight=1)
        
        # ==================================================================================#
        
        # Define o título do frame_widgets_1_1 (Viewport) na primeira linha
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_1, text="Viewport")
        self.label_world.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        # Define os labels do frame_widgets_1_1
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_1, text="uMin")
        self.label_world.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_1, text="uMax")
        self.label_world.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_1, text="vMin")
        self.label_world.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_1, text="vMax")
        self.label_world.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        
        # Define os entrys do frame_widgets_1_1
        self.entry_world_uMin = ctk.CTkEntry(self.frame_widgets_1_1, width=20)
        self.entry_world_uMin.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_uMax = ctk.CTkEntry(self.frame_widgets_1_1, width=20)
        self.entry_world_uMax.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_vMin = ctk.CTkEntry(self.frame_widgets_1_1, width=20)
        self.entry_world_vMin.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_vMax = ctk.CTkEntry(self.frame_widgets_1_1, width=20)
        self.entry_world_vMax.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

        # ==================================================================================#

        # Cria o segundo frame do frame_widgets_1 (Dados do mundo)
        # -> 1 linha, 1 coluna
        self.frame_widgets_1_2 = ctk.CTkFrame(self.frame_widgets_1)
        self.frame_widgets_1_2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Dividi o frame_widgets_1_2 em 2, criando outros 2 frames
        self.frame_widgets_1_2.grid_columnconfigure(0, weight=1)
        self.frame_widgets_1_2.grid_columnconfigure(1, weight=1)
        self.frame_widgets_1_2.grid_rowconfigure(0, weight=1)

        # Widgets do frame_widgets_1_2_1
        self.frame_widgets_1_2_1 = ctk.CTkFrame(self.frame_widgets_1_2)
        self.frame_widgets_1_2_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configura o frame_widgets_1_2_1 para ter 2 coluna e 4 linhas
        
        # Define os labels do frame_widgets_1_2_1
        
        # Define o título do frame_widgets_1_2_1 (Viewport) na primeira linha
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_2_1, text="View-up")
        self.label_world.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # X, Y, Z
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_2_1, text="X")
        self.label_world.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_2_1, text="Y")
        self.label_world.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_2_1, text="Z")
        self.label_world.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        # Define os entrys do frame_widgets_1_2_1
        self.entry_world_view_up_x = ctk.CTkEntry(self.frame_widgets_1_2_1, width=30)
        self.entry_world_view_up_x.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_view_up_y = ctk.CTkEntry(self.frame_widgets_1_2_1, width=30)
        self.entry_world_view_up_y.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_view_up_z = ctk.CTkEntry(self.frame_widgets_1_2_1, width=30)
        self.entry_world_view_up_z.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        
        
        # Widgets do frame_widgets_1_2_2
        self.frame_widgets_1_2_2 = ctk.CTkFrame(self.frame_widgets_1_2)
        self.frame_widgets_1_2_2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Configura o frame_widgets_1_2_2 para ter 2 coluna e 4 linhas

        # Define os labels do frame_widgets_1_2_2
        
        # Define o título do frame_widgets_1_2_2 (Viewport) na primeira linha
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_2_2, text="VRP")
        self.label_world.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # X, Y, Z
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_2_2, text="X")
        self.label_world.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_2_2, text="Y")
        self.label_world.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_2_2, text="Z")
        self.label_world.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        # Define os entrys do frame_widgets_1_2_2
        self.entry_world_vrp_x = ctk.CTkEntry(self.frame_widgets_1_2_2, width=30)
        self.entry_world_vrp_x.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_vrp_y = ctk.CTkEntry(self.frame_widgets_1_2_2, width=30)
        self.entry_world_vrp_y.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_vrp_z = ctk.CTkEntry(self.frame_widgets_1_2_2, width=30)
        self.entry_world_vrp_z.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        
        # ==================================================================================#
        
        # Cria o terceiro frame do frame_widgets_1 (Dados do mundo)
        # -> 1 linha, 1 coluna
        self.frame_widgets_1_3 = ctk.CTkFrame(self.frame_widgets_1)
        self.frame_widgets_1_3.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Dividi o frame_widgets_1_3 em 2, criando outros 2 frames
        self.frame_widgets_1_3.grid_columnconfigure(0, weight=1)
        self.frame_widgets_1_3.grid_columnconfigure(1, weight=1)
        self.frame_widgets_1_3.grid_rowconfigure(0, weight=1)
        
        # Widgets do frame_widgets_1_3_1
        self.frame_widgets_1_3_1 = ctk.CTkFrame(self.frame_widgets_1_3)
        self.frame_widgets_1_3_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configura o frame_widgets_1_3_1 para ter 2 coluna e 4 linhas

        # Define os labels do frame_widgets_1_3_1
        
        # Define o título do frame_widgets_1_3_1 (Viewport) na primeira linha
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_3_1, text="Ponto Focal")
        self.label_world.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # X, Y, Z
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_3_1, text="X")
        self.label_world.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_3_1, text="Y")
        self.label_world.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_3_1, text="Z")
        self.label_world.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        # Define os entrys do frame_widgets_1_3_1
        self.entry_world_ponto_focal_x = ctk.CTkEntry(self.frame_widgets_1_3_1, width=30)
        self.entry_world_ponto_focal_x.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_ponto_focal_y = ctk.CTkEntry(self.frame_widgets_1_3_1, width=30)
        self.entry_world_ponto_focal_y.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_ponto_focal_z = ctk.CTkEntry(self.frame_widgets_1_3_1, width=30)
        self.entry_world_ponto_focal_z.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        
        # Widgets do frame_widgets_1_3_2
        self.frame_widgets_1_3_2 = ctk.CTkFrame(self.frame_widgets_1_3)
        self.frame_widgets_1_3_2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Configura o frame_widgets_1_3_2 para ter 2 coluna e 4 linhas
        
        # Define os labels do frame_widgets_1_3_2

        # Define o título do frame_widgets_1_3_2 (Viewport) na primeira linha
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_3_2, text="Distância ao plano")
        self.label_world.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Projeção, Near, Far
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_3_2, text="Projeção")
        self.label_world.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_3_2, text="Near")
        self.label_world.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_3_2, text="Far")
        self.label_world.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        # Define os entrys do frame_widgets_1_3_2
        self.entry_world_distancia_projeção = ctk.CTkEntry(self.frame_widgets_1_3_2, width=30)
        self.entry_world_distancia_projeção.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_distancia_near = ctk.CTkEntry(self.frame_widgets_1_3_2, width=30)
        self.entry_world_distancia_near.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_distancia_far = ctk.CTkEntry(self.frame_widgets_1_3_2, width=30)
        self.entry_world_distancia_far.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        
        # ==================================================================================#
        
        # Cria o quarto frame do frame_widgets_1 (Dados do mundo)
        # -> 1 linha, 1 coluna
        self.frame_widgets_1_4 = ctk.CTkFrame(self.frame_widgets_1)
        self.frame_widgets_1_4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
                
        # Configura o frame_widgets_1_4 para ter 4 coluna e 3 linhas
        self.frame_widgets_1_4.grid_columnconfigure(0, weight=1)
        self.frame_widgets_1_4.grid_columnconfigure(1, weight=1)
        self.frame_widgets_1_4.grid_rowconfigure(0, weight=1)
        self.frame_widgets_1_4.grid_rowconfigure(1, weight=1)
        self.frame_widgets_1_4.grid_rowconfigure(2, weight=1)

        # Define o título do frame_widgets_1_4 (Viewport) na primeira linha
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_4, text="Window")
        self.label_world.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        # Define os labels do frame_widgets_1_4
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_4, text="Xmin")
        self.label_world.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_4, text="Xmax")
        self.label_world.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_4, text="Ymin")
        self.label_world.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_1_4, text="Ymax")
        self.label_world.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        
        # Define os entrys do frame_widgets_1_4
        self.entry_world_xMin = ctk.CTkEntry(self.frame_widgets_1_4, width=20)
        self.entry_world_xMin.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_xMax = ctk.CTkEntry(self.frame_widgets_1_4, width=20)
        self.entry_world_xMax.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_yMin = ctk.CTkEntry(self.frame_widgets_1_4, width=20)
        self.entry_world_yMin.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_yMax = ctk.CTkEntry(self.frame_widgets_1_4, width=20)
        self.entry_world_yMax.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")
        
        # ==================================================================================#
        
        # frame_widgets_2 com 2 novos frames
        
        # Cria o primeiro frame do frame_widgets_2 (Dados do objeto)
        # -> 1 linha, 1 coluna
        self.frame_widgets_2_1 = ctk.CTkFrame(self.frame_widgets_2)
        self.frame_widgets_2_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configura o frame_widgets_2_1 para ter 2 coluna e 4 linhas
        self.frame_widgets_2_1.grid_columnconfigure(0, weight=1)
        self.frame_widgets_2_1.grid_columnconfigure(1, weight=1)
        self.frame_widgets_2_1.grid_rowconfigure(0, weight=1)
        self.frame_widgets_2_1.grid_rowconfigure(1, weight=1)
        self.frame_widgets_2_1.grid_rowconfigure(2, weight=1)
        
        # Define o título do frame_widgets_2_1 (Viewport) na primeira linha
        self.label_world = ctk.CTkLabel(self.frame_widgets_2_1, text="Objeto")
        self.label_world.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        # Define os labels do frame_widgets_2_1
        self.label_world = ctk.CTkLabel(self.frame_widgets_2_1, text="Raio da base")
        self.label_world.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_2_1, text="Raio do topo")
        self.label_world.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_2_1, text="N de lados")
        self.label_world.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_world = ctk.CTkLabel(self.frame_widgets_2_1, text="Altura")
        self.label_world.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        
        # Define os entrys do frame_widgets_2_1
        self.entry_world_raio_base = ctk.CTkEntry(self.frame_widgets_2_1, width=20)
        self.entry_world_raio_base.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_raio_topo = ctk.CTkEntry(self.frame_widgets_2_1, width=20)
        self.entry_world_raio_topo.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_n_lados = ctk.CTkEntry(self.frame_widgets_2_1, width=20)
        self.entry_world_n_lados.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        
        self.entry_world_altura = ctk.CTkEntry(self.frame_widgets_2_1, width=20)
        self.entry_world_altura.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")
        
        # ==================================================================================#
        
        