import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import mean_squared_error
from PIL import Image
import random

# Tamaño de la imagen
alto, ancho = 120, 180

# Imagen objetivo
objetivo = np.array(Image.open(r"Cap3\mapache_gordito.jpg").resize((ancho, alto)))[:,:,:3]

# Función de aptitud
def aptitud(img):
    return mean_squared_error(img, objetivo)

# Crear individuo aleatorio (imagen)
def crear_individuo():
    return np.random.randint(0, 256, size=(alto, ancho, 3), dtype=np.uint8)

# Cruce de dos imágenes
def cruzar(p1, p2):
    mask = np.random.randint(0, 2, size=(alto, ancho, 1), dtype=bool)
    return np.where(mask, p1, p2)

# Mutación
def mutar(img, tasa=0.01):
    mutado = img.copy()
    mask = np.random.rand(alto, ancho, 3) < tasa
    mutado[mask] = np.random.randint(0, 256, size=np.count_nonzero(mask), dtype=np.uint8)
    return mutado

# Evolución
def evolucionar(poblacion, generaciones=100):
    for gen in range(generaciones):
        poblacion.sort(key=aptitud)
        mejor = poblacion[0]
        print(f"Generación {gen}, aptitud: {aptitud(mejor)}")

        nueva_gen = [mejor]
        while len(nueva_gen) < len(poblacion):
            p1, p2 = random.choices(poblacion[:10], k=2)
            hijo = cruzar(p1, p2)
            hijo = mutar(hijo)
            nueva_gen.append(hijo)

        poblacion = nueva_gen
    return poblacion[0]

# Crear población inicial
poblacion = [crear_individuo() for _ in range(50)]

# Evolucionar
mejor_imagen = evolucionar(poblacion, generaciones=100)

# Mostrar resultado
plt.imshow(mejor_imagen)
plt.title("Imagen Evolucionada")
plt.axis("off")
plt.show()
