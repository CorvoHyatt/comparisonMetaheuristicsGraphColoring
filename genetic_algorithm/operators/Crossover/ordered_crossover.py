import random
from typing import List

import numpy as np
from genetic_algorithm.Individuals.individual import Individual
from genetic_algorithm.operators.Crossover.crossover_operators import CrossoverOperator


class OrderedOX1(CrossoverOperator):
    "No apto para cardiacos ni para codificación binaria ni combinatoria"

    @staticmethod
    def crossover(population_selected: List[Individual]) -> List[Individual]:
        new_population = []
        for i in range(len(population_selected) - 1):
            parent1 = population_selected[i]
            parent2 = population_selected[i + 1]
            point1 = random.randint(0, len(parent1.genotype) - 2)

            while True:
                point2 = random.randint(0, len(parent1.genotype) - 2)
                if point2 != point1:
                    break

            start_point = min(point1, point2) + 1
            end_point = max(point1, point2) + 2
            genotype = [-1] * len(parent1.genotype)
            genotype[start_point:end_point] = parent2.genotype[start_point:end_point]
            index_gen = end_point
            index_parent = index_gen
            while index_gen != start_point:

                if parent1.genotype[index_parent] not in genotype:
                    genotype[index_gen] = parent1.genotype[index_parent]
                    index_parent = index_parent + 1
                    index_gen = index_gen + 1
                else:
                    index_parent = index_parent + 1
                if index_parent >= len(parent1.genotype):
                    index_parent = 0
                if index_gen >= len(parent1.genotype):
                    index_gen = 0

            # Creamos un nuevo individuo con el genotipo resultante
            child = Individual(np.array(genotype))
            new_population.append(child)

        return new_population


# # Crear instancias de Individual y asignarles un valor de fitness
# individuals = []
# for _ in range(2):
#     permutation = np.random.permutation(
#         11
#     )  # 11 porque la permutación excluye el último número

#     # Seleccionar los primeros 10 elementos de la permutación
#     genotype = permutation[:10]
#     fitness_value = np.random.uniform(
#         0, 1
#     )  # Ejemplo de un valor de fitness aleatorio entre 0 y 1
#     individual = Individual(genotype)
#     individual.fitness = fitness_value
#     individuals.append(individual)

# print(*map(lambda x: x.__dict__, individuals), sep="\n")
# population = OrderedOX1.crossover(individuals)
# print(*map(lambda x: x.__dict__, population), sep="\n")
