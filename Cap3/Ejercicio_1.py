import random
import numpy as np

tamaño_poblacion = 50
generaciones = 100
tasa_mutacion = 0.01
longitud_cromosoma = 16

# Función objetivo
def f(x):
    return x * np.sin(10 * np.pi * x) + 1

def binario_a_real(bin_str):
    entero = int(bin_str, 2)
    return entero / (2**longitud_cromosoma - 1)

def crear_individuo():
    return ''.join(random.choice('01') for _ in range(longitud_cromosoma))

# Evaluar aptitud
def aptitud(individuo):
    x = binario_a_real(individuo)
    return f(x)

# Selección por torneo
def seleccion_torneo():
    torneo = random.sample(poblacion, 3)
    return max(torneo, key=aptitud)

# Cruce de un punto
def cruzar(padre1, padre2):
    punto = random.randint(1, longitud_cromosoma - 1)
    return padre1[:punto] + padre2[punto:]

# Mutación
def mutar(individuo):
    nuevo = ''
    for bit in individuo:
        if random.random() < tasa_mutacion:
            nuevo += '0' if bit == '1' else '1'
        else:
            nuevo += bit
    return nuevo

# Población inicial
poblacion = [crear_individuo() for _ in range(tamaño_poblacion)]

# Evolución
mejores = []

for gen in range(generaciones):
    nueva_poblacion = []

    for _ in range(tamaño_poblacion):
        p1 = seleccion_torneo()
        p2 = seleccion_torneo()
        hijo = cruzar(p1, p2)
        hijo = mutar(hijo)
        nueva_poblacion.append(hijo)

    poblacion = nueva_poblacion
    mejor = max(poblacion, key=aptitud)
    mejores.append(aptitud(mejor))

# Resultados
mejor_final = max(poblacion, key=aptitud)
x_mejor = binario_a_real(mejor_final)
print(f"Mejor x: {x_mejor:.6f}")
print(f"f(x): {f(x_mejor):.6f}")
