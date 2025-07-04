import random
import numpy as np

# Parametros del modelo
partidos = ['A', 'B', 'C', 'D', 'E']
curules = {'A':10, 'B':5, 'C':16, 'D':12, 'E':7}

num_entidades = 50
pesos_entidades = np.random.randint(1, 101, size=num_entidades)

total_peso_politico = np.sum(pesos_entidades)

tamaño_poblacion = 8
poblacion = []
num_individuos_torneo = 3
p_mutacion=0.2

generaciones = 100
mejor_individuo = None
mejor_aptitud = float('inf')

# Poblacion inicial
for i in range(tamaño_poblacion):
    partidos_restantes = ['A', 'B', 'C', 'D', 'E']
    individuo = {'A':[], 'B':[], 'C':[], 'D':[], 'E':[]}
    for j in range(num_entidades):
        partido_seleccionado = random.choice(partidos_restantes)
        individuo[partido_seleccionado].append(j)
        if len(individuo[partido_seleccionado]) >= curules[partido_seleccionado]:
            partidos_restantes.remove(partido_seleccionado)
    poblacion.append(individuo)

# Funcion de aptitud, es el error cuadratico medio, que se espera sea cercano a cero
def aptitud(individuo:dict):
    # Se espera que cada partido tenga un 20% del poder politico
    error_cuadratico_medio = 0
    for i in partidos:
        peso_partido = 0
        for j in individuo[i]:
            peso_partido += pesos_entidades[j]
        error_cuadratico_medio += ((0.2 - peso_partido/total_peso_politico) ** 2) / 5
    
    return error_cuadratico_medio

# Seleccion por torneo
def seleccion():
    seleccionados = []
    for _ in range(len(poblacion)):
        competidores = random.sample(poblacion, num_individuos_torneo)
        mejor = min(competidores, key=aptitud)
        seleccionados.append(mejor)
    return seleccionados

# Cruce
def reparar_individuo(individuo):
    asignaciones = {}
    for partido, entidades in individuo.items():
        for e in entidades:
            asignaciones[e] = asignaciones.get(e, []) + [partido]

    # Resolver conflictos
    for e, ps in asignaciones.items():
        if len(ps) > 1:
            elegido = random.choice(ps)
            for p in ps:
                if p != elegido:
                    individuo[p].remove(e)
        elif len(ps) == 0:
            # Entidad no asignada: la agregamos al partido con menos entidades
            menor = min(individuo, key=lambda x: len(individuo[x]))
            individuo[menor].append(e)

    # Truncar listas si exceden su límite
    for p in partidos:
        if len(individuo[p]) > curules[p]:
            random.shuffle(individuo[p])
            individuo[p] = individuo[p][:curules[p]]
    
    return individuo

def cruzar(padre1, padre2):
    hijo1 = {p: [] for p in partidos}
    hijo2 = {p: [] for p in partidos}
    
    # Elegimos un punto de corte aleatorio por partido
    for p in partidos:
        corte = random.randint(1, min(len(padre1[p]), len(padre2[p])) - 1)
        hijo1[p] = padre1[p][:corte] + padre2[p][corte:]
        hijo2[p] = padre2[p][:corte] + padre1[p][corte:]

    # Ajustar si hay entidades repetidas o no asignadas
    hijo1 = reparar_individuo(hijo1)
    hijo2 = reparar_individuo(hijo2)
    
    return hijo1, hijo2

# Mutación
def mutar(individuo):
    nuevo = {p: list(entidades) for p, entidades in individuo.items()}
    p1, p2 = random.sample(partidos, 2)

    # Asegurarse que ambos partidos tengan al menos una curul asignada
    if not nuevo[p1] or not nuevo[p2]:
        return nuevo  # No se puede mutar

    # Seleccionar una entidad al azar de cada partido
    e1 = random.choice(nuevo[p1])
    e2 = random.choice(nuevo[p2])

    # Intercambiar las entidades
    nuevo[p1].remove(e1)
    nuevo[p1].append(e2)

    nuevo[p2].remove(e2)
    nuevo[p2].append(e1)

    return nuevo

def aplicar_mutacion():
    global poblacion
    nueva_poblacion = []
    for i in poblacion:
        if random.random() < p_mutacion:
            nueva_poblacion.append(mutar(i))
        else:
            nueva_poblacion.append(i)
    poblacion = nueva_poblacion

for gen in range(generaciones):
    # 1. Evaluar aptitud
    poblacion.sort(key=aptitud)

    # 2. Guardar mejor individuo
    candidato_a_lider = poblacion[0]
    if aptitud(candidato_a_lider) < mejor_aptitud:
        mejor_individuo = candidato_a_lider
        mejor_aptitud = aptitud(candidato_a_lider)

    # 3. Selección
    seleccionados = seleccion()

    # 4. Cruce por parejas
    nueva_poblacion = []
    for i in range(0, len(seleccionados), 2):
        if i + 1 < len(seleccionados):
            hijo1, hijo2 = cruzar(seleccionados[i], seleccionados[i+1])
            nueva_poblacion.extend([hijo1, hijo2])
        else:
            nueva_poblacion.append(seleccionados[i])  # Impar

    poblacion = nueva_poblacion

    # 5. Mutación
    aplicar_mutacion()

    # 6. Preservar el mejor
    poblacion.sort(key=aptitud)
    poblacion[-1] = mejor_individuo

    print(f"Generación {gen+1}, mejor aptitud: {mejor_aptitud:.6f}")
print()

print(f"RESULTADOS:")
print(f"Pesos de las entidades:")
for i in range(num_entidades):
    print(f"| {i:2d} | {pesos_entidades[i]:3d} |")
print()

print(f"Mejor individuo:")
for i in partidos:
    poder_politico = sum(pesos_entidades[j] for j in mejor_individuo[i])
    print(f"{i} | {poder_politico} | {poder_politico/total_peso_politico:9f} | {mejor_individuo[i]} |")
