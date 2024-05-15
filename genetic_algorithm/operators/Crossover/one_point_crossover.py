from typing import List

import numpy as np
from genetic_algorithm.Individuals.individual import Individual
from genetic_algorithm.operators.Crossover.crossover_operators import CrossoverOperator


class OnePoint(CrossoverOperator):
    @staticmethod
    def crossover(population_selected: List[Individual]) -> List[Individual]:
        new_population = []
        for i in range(len(population_selected) - 1):
            parent1 = population_selected[i]
            parent2 = population_selected[i + 1]

            # Realizamos el crossover en un punto
            crossover_point = np.random.randint(1, len(parent1.genotype) - 1)
            child_genotype = np.concatenate(
                (parent1.genotype[:crossover_point], parent2.genotype[crossover_point:])
            )

            # Creamos un nuevo individuo con el genotipo resultante
            child = Individual(child_genotype)
            new_population.append(child)

        return new_population
