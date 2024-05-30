from SoftwareRender.screen import Screen
from Wireframe.screen import Screen_Wireframe
from Wireframe.object_3d import Points_Object

import os

if __name__ == "__main__":
    
    # Wireframe
    
    # Cria a classe do wireframe
    screen_wireframe = Screen_Wireframe()
    
    # Deleta os arquivos de pontos
    screen_wireframe.delete_points_file()
    
    # Registra os clicks no programa
    screen_wireframe.register_click()
    
    # Roda o programa
    screen_wireframe.run()
    
    # ======================================================================== #
    
    # Deleta os arquivos de pontos_3d 
    for file in os.listdir(os.path.join("Wireframe", "points_3d")):
        os.remove(os.path.join("Wireframe", "points_3d", file))
    
    # Revolução do objeto
    files_classes = []

    # Cria a quantidade de classes de objetos referente a quantidade de arquivos de pontos
    for file in os.listdir(os.path.join("Wireframe", "points")):
            
        # Cria as classes dos objetos
        files_classes.append(Points_Object(file))
        
    # Converte os pontos dos arquivos para pontos na linha
    for file in files_classes:
        file.points_file_to_points_line()
        
    # Roda a revolução dos objetos
    for file in files_classes:
        file.revolucion()
        
    # Software Render
    
    # Cria a classe do software render
    screen = Screen(files_classes)
    
    # Roda o programa
    screen.run()