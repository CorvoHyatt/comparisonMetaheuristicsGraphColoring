from typing import List

import numpy as np
from genetic_algorithm.Individuals.individual import Individual
from genetic_algorithm.operators.Crossover.crossover_operators import CrossoverOperator


class Uniform(CrossoverOperator):
    @staticmethod
    def crossover(population_selected: List[Individual]) -> List[Individual]:
        new_population = []
        for i in range(len(population_selected) - 1):
            parent1 = population_selected[i]
            parent2 = population_selected[i + 1]

            # Realizamos la cruza uniforme
            child_genotype = np.array(
                [
                    (
                        parent1.genotype[j]
                        if np.random.rand() < 0.5
                        else parent2.genotype[j]
                    )
                    for j in range(len(parent1.genotype))
                ]
            )

            # Creamos un nuevo individuo con el genotipo resultante
            child = Individual(child_genotype)
            new_population.append(child)

        return new_population
