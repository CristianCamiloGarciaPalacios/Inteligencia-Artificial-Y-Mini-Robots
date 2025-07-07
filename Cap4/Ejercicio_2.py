from deap import gp, base, tools, creator
import operator, random

# Definición del conjunto de terminales y funciones
pset = gp.PrimitiveSet("MAIN", 4)
pset.renameArguments(ARG0="A", ARG1="B", ARG2="C", ARG3="D")
pset.addPrimitive(operator.and_, 2)
pset.addPrimitive(operator.or_, 2)
pset.addPrimitive(operator.not_, 1)
pset.addPrimitive(operator.xor, 2)
pset.addTerminal(0)
pset.addTerminal(1)

# Evaluación de individuos
def eval_ind(ind):
    func = toolbox.compile(expr=ind)
    error = 0
    for inputs, expected in truth_table.items():
        try:
            output = func(*inputs)
        except:
            output = 0
        error += abs(output - expected)
    return 1 / (0.1 + error),

# Tabla de verdad simplificada (solo segmento 'a')
truth_table = {
    (0,0,0,0): 1,
    (0,0,0,1): 0,
    (0,0,1,0): 1,
    (0,1,0,0): 0,
    (1,0,0,0): 1
}

# Configuración de DEAP
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)
toolbox.register("evaluate", eval_ind)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr, pset=pset)

# Proceso evolutivo
population = toolbox.population(n=100)
for gen in range(20):
    offspring = toolbox.select(population, len(population))
    offspring = list(map(toolbox.clone, offspring))
    
    for c1, c2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.7:
            toolbox.mate(c1, c2)
            del c1.fitness.values, c2.fitness.values
    for mutant in offspring:
        if random.random() < 0.2:
            toolbox.mutate(mutant)
            del mutant.fitness.values
    invalid = [ind for ind in offspring if not ind.fitness.valid]
    for ind in invalid:
        ind.fitness.values = toolbox.evaluate(ind)
    population[:] = offspring

# Resultado
best = tools.selBest(population, 1)[0]
print("Mejor programa:", best)
