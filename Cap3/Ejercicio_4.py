import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import random

# Tamaño de la imagen
alto, ancho = 120, 180

# Imagen objetivo
objetivo = np.array(Image.open(r"Cap3\mapache_gordito.jpg").resize((ancho, alto)))[:,:,:3]
# plt.imshow(objetivo)
# plt.title("Imagen Objetivo")
# plt.axis("off")
# plt.show()

poblacion = 50
num_torneo = int(poblacion * 0.3)
generaciones = 1000

# Función de aptitud
def aptitud(img):
    # Convertir ambas imágenes a escala de grises antes de calcular SSIM
    imagen_gris = np.mean(img, axis=2)
    objetivo_gris = np.mean(objetivo, axis=2)
    return ssim(imagen_gris, objetivo_gris, data_range=255)

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
def evolucionar(poblacion, generaciones):
    gen_sin_mejora = 0
    mejor_aptitud = -1
    for gen in range(generaciones):
        poblacion.sort(key=aptitud, reverse=True)
        mejor = poblacion[0]
        mejor_aptitud_gen = aptitud(mejor)
        
        if mejor_aptitud_gen > mejor_aptitud:
            mejor_aptitud = mejor_aptitud_gen
            gen_sin_mejora = 0
        else:
            gen_sin_mejora += 1
        
        print(f"Generación {gen}, aptitud: {aptitud(mejor)}")

        if gen_sin_mejora > 100:
            print("No hay mejoras significativas, terminando evolución.")
            break

        nueva_gen = [mejor]
        while len(nueva_gen) < len(poblacion):
            p1, p2 = random.choices(poblacion[:num_torneo], k=2)
            hijo = cruzar(p1, p2)
            hijo = mutar(hijo)
            nueva_gen.append(hijo)

        poblacion = nueva_gen
    return poblacion[0]

# Crear población inicial
poblacion = [crear_individuo() for _ in range(poblacion)]

# Evolucionar
mejor_imagen = evolucionar(poblacion, generaciones=generaciones)

# Mostrar resultado
plt.imshow(mejor_imagen)
plt.title("Imagen Evolucionada")
plt.axis("off")
plt.show()
