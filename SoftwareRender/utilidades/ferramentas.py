def rgb_to_hex(color):

	return "#"+format(int(color[0]),'02x')+format(int(color[1]),'02x')+format(int(color[2]),'02x')

def hex_to_rgb(hex_color):
    
	hex_color = hex_color.lstrip('#')
 
	return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def soma_rgb(color1, color2):
	
	# Vindo do objeto, a cor esta indexada da seguinte forma: (218, 23, 255)
	# Vindo da face, a cor esta indexada da seguinte forma: [48. 48. 48.]
 
	return (color1[0] + color2[0], color1[1] + color2[1], color1[2] + color2[2])