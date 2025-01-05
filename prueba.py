import matplotlib.pyplot as plt
import numpy as np

# Configuración del semicírculo
radio = 60
centro_x = 0
centro_y = 0
max_dist = 1000
angulos = np.linspace(-np.pi / 2, np.pi / 2, 180)  # De -90 grados a 90 grados

# Coordenadas del semicírculo
x = centro_x + radio * np.cos(angulos)
y = centro_y + radio * np.sin(angulos)

# Tamaño de la figura (ancho, alto) en pulgadas
figsize = (10, 8)

# Creación de la figura y el eje con el tamaño especificado
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=figsize)

# Gráfico del semicírculo
ax.plot(angulos, [radio]*len(angulos), color='blue')

# Configuración del rango de los ejes
ax.set_ylim(0, max_dist)

# Agregar una grilla circular
ax.grid(True)
grid = np.linspace(100, max_dist, 10, dtype=int)  # Ajuste de la grilla

ax.set_rticks(grid)  # Radio de las líneas de la grilla

# Personalizar las etiquetas de los ejes
ax.set_yticklabels(grid)
ax.set_xticks(np.linspace(-np.pi / 2, np.pi / 2, 5))
ax.set_xticklabels(['-90°', '-45°', '0°', '45°', '90°'])

# Limitar la visualización a los cuadrantes deseados

ax.set_theta_direction(1)
ax.set_thetamax(90)

# Título del gráfico
plt.title('Mapeo de mediciones')

plt.scatter(np.pi/2,300)
# Mostrar el gráfico
plt.show()
