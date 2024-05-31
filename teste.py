def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Testando a função
rgb_color = hex_to_rgb("#e346ff")
print(rgb_color)
