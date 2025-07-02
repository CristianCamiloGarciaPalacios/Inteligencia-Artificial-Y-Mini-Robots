import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap, BoundaryNorm

# Parámetros
size = 100
p = 0.25
steps = 60
burn_time = 2

# Estados
GREEN = 0
BURNING = 1
BURNED = 2

colors = ['green', 'red', 'black']
cmap = ListedColormap(colors)
bounds = [0, 1, 2, 3]
norm = BoundaryNorm(bounds, cmap.N)

# Estado inicial
forest = np.zeros((size, size), dtype=int)
burn_counters = np.zeros((size, size), dtype=int)
forest[size//2, size//2] = BURNING
burn_counters[size//2, size//2] = burn_time

def update(frame):
    global forest, burn_counters
    new_forest = forest.copy()
    new_counters = burn_counters.copy()

    for i in range(size):
        for j in range(size):
            if forest[i, j] == GREEN:
                vecinos = forest[max(i-1,0):min(i+2,size), max(j-1,0):min(j+2,size)]
                if BURNING in vecinos:
                    if np.random.rand() < p:
                        new_forest[i, j] = BURNING
                        new_counters[i, j] = burn_time
            elif forest[i, j] == BURNING:
                new_counters[i, j] -= 1
                if new_counters[i, j] <= 0:
                    new_forest[i, j] = BURNED

    forest = new_forest
    burn_counters = new_counters
    mat.set_data(forest)
    return [mat]

# Visualización
fig, ax = plt.subplots()
mat = ax.matshow(forest, cmap=cmap, norm=norm)
ax.set_title("Incendio Forestal")

ani = animation.FuncAnimation(fig, update, frames=steps, interval=300, repeat=False)
plt.show()
