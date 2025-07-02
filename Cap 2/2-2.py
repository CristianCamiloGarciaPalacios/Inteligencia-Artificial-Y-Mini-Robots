import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

size = 50         # Tamaño del bosque (cuadrícula)
p = 0.3           # Probabilidad de propagación del fuego
steps = 50        # Pasos de la simulación

GREEN = 0
BURNING = 1
BURNED = 2

# Colores
colors = ['green', 'red', 'black']
cmap = plt.cm.colors.ListedColormap(colors)

# Bosque inicial
forest = np.zeros((size, size), dtype=int)
forest[size//2, size//2] = BURNING  # fuego en el centro

def update(frame):
    global forest
    new_forest = forest.copy()
    for i in range(size):
        for j in range(size):
            if forest[i, j] == GREEN:
                # Ver vecinos (con márgenes seguros)
                neighbors = forest[max(i-1,0):min(i+2,size), max(j-1,0):min(j+2,size)]
                if BURNING in neighbors:
                    if np.random.rand() < p:
                        new_forest[i, j] = BURNING
            elif forest[i, j] == BURNING:
                new_forest[i, j] = BURNED
    forest = new_forest
    mat.set_data(forest)
    return [mat]

# Visualización
fig, ax = plt.subplots()
mat = ax.matshow(forest, cmap=cmap)
ani = animation.FuncAnimation(fig, update, frames=steps, interval=300, repeat=False)

plt.show()