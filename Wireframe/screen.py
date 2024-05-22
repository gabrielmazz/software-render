import customtkinter as ctk
import tkinter as tk
import os

class Screen_Wireframe():
    
    def __init__(self):
        
        # Define a aparência da tela principal como dark
        ctk.set_appearance_mode("dark")
        
        self.app = ctk.CTk()
        self.app.title("Wireframe")
        self.app.geometry("800x800")
        
        self.points = []
        
        self.create_frame_grid()
        self.grid()
        
    def run(self):
        self.app.mainloop()
        
    def create_frame_grid(self):
        
        # Cria um frame para o canvas
        self.frame_canvas = ctk.CTkFrame(self.app)
        self.frame_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Cria um canvas
        self.canvas = ctk.CTkCanvas(self.frame_canvas)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
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
        
        print("Points saved!")
          
    def delete_points_file(self):
        
        # Deleta todos os arquivos de pontos
        for file in os.listdir(os.path.join("Wireframe", "points")):
            os.remove(os.path.join("Wireframe", "points", file))
            
        print("Points deleted!")