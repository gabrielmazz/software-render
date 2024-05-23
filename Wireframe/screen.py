import customtkinter as ctk
import tkinter as tk
import os

class Screen_Wireframe():
    
    def __init__(self):
        
        # Define a aparência da tela principal como dark
        ctk.set_appearance_mode("dark")
        
        self.app = ctk.CTk()
        self.app.title("Wireframe")
        self.app.geometry("1610x900")
        
        self.points = []
        
        self.create_frame_grid()
        self.grid()
        
    def run(self):
        
        # Cria as binds para os botões
        self.binds()
        
        self.app.mainloop()
        
    def binds(self):
        
        # Botao 12 do teclado fecha o programa
        self.app.bind("<F12>", self.quit)
    
    def quit(self, event=None):
        
        # Destroi a tela principal
        self.app.destroy()
        
    def create_frame_grid(self):
        
        # Define a configuração de colunas, dividindo em 2
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)
        
        # Cria um canvas para desenhar os pontos
        self.canvas = ctk.CTkCanvas(self.app, width=800, height=800, borderwidth=2, relief="solid")
        self.canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Cria um frame para lista os objetos criados
        self.frame_objects = ctk.CTkScrollableFrame(self.app)
        self.frame_objects.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Adiciona titulo no frame de objetos
        self.label_objects = ctk.CTkLabel(self.frame_objects, text="Objects criados",
                                     text_color="white", justify="center", font=("Arial", 30))
        self.label_objects.grid(row=0, column=0, padx=10, pady=10)
        
    def grid(self):
        
        # Define as linhas do grid, desenhando elas no canvas
        for i in range(0, 1600, 20):
            self.canvas.create_line(i, 0, i, 900, fill="gray")
            
        for i in range(0, 900, 20):
            self.canvas.create_line(0, i, 1600, i, fill="gray")
            
    def register_click(self):
        
        # Registra o clique do botão
        self.canvas.bind("<Button-1>", self.click)
        
        # Registra o clique q do teclado
        self.app.bind("q", self.register_points_file)
    
    def click(self, event):
            
        # Registra o ponto clicado
        self.points.append((event.x, event.y))
        
        # Desenha o ponto no canvas
        self.canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill="red")
        
        # Se tiver mais de 1 ponto, desenha a linha
        if len(self.points) > 1:
            self.canvas.create_line(self.points[-2][0], self.points[-2][1], self.points[-1][0], self.points[-1][1], fill="red")
        
    def register_points_file(self, event=None):
        
        # Conta a quantidade de arquivo para definir o final do nome do arquivo
        count = 0
        for file in os.listdir(os.path.join("Wireframe", "points")):
            count += 1
            
        # Cria o arquivo
        with open(os.path.join("Wireframe", "points", f"points_{count}.txt"), "w") as file:
            for point in self.points:
                file.write(f"{point[0]} {point[1]}\n")
                
        # Limpa os pontos
        self.points = []
        
        # Limpa o canvas
        self.canvas.delete("all")
        
        # Redesenha o grid
        self.grid()
        
        self.lista_objetos()
        
        print("Points saved!")
          
    def delete_points_file(self):
        
        # Deleta todos os arquivos de pontos
        for file in os.listdir(os.path.join("Wireframe", "points")):
            os.remove(os.path.join("Wireframe", "points", file))
            
        print("Points deleted!")
        
    def lista_objetos(self):
        
        # Conta a quantidade de arquivos de pontos
        count_files = len(os.listdir(os.path.join("Wireframe", "points")))

        # Itera por cada arquivo de pontos
        for file_index in range(count_files):
            file_name = f"points_{file_index}.txt"
            file_path = os.path.join("Wireframe", "points", file_name)

            # Cria um rótulo para o nome do arquivo
            label_file = ctk.CTkLabel(self.frame_objects, text=f"Desenho - {file_index+1}")
            label_file.grid(row=file_index + 1, column=0)

            # Lê os pontos do arquivo
            with open(file_path, "r") as file:
                points = file.readlines()

            # Cria a string da lista de pontos
            points_list_str = ""
            for point in points:
                points_list_str += f"{point.strip()}\n"  # Remove espaços em branco e adiciona \n

            # Cria um rótulo para a lista de pontos
            label_points_list = ctk.CTkLabel(self.frame_objects, text=points_list_str,
                                            justify="left", font=("Arial", 12))
            label_points_list.grid(row=file_index + 1, column=1)
