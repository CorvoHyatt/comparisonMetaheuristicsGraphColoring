from typing import List

import numpy as np
from genetic_algorithm.Individuals.individual import Individual
from genetic_algorithm.operators.Mutation.mutation_operators import MutationOperator


class BitInversion(MutationOperator):
    @staticmethod
    def mutate(population: List[Individual], probability: int) -> List[Individual]:
        new_population = []
        for individual in population:
            random_prob = np.random.randint(
                1, 1001
            )  # Generar un número aleatorio entre 1 y 1000
            if random_prob <= probability:
                mutated_genotype = np.copy(individual.genotype)
                # Seleccionar un índice aleatorio y realizar la mutación de bit invertido
                index = np.random.randint(0, len(mutated_genotype))
                mutated_genotype[index] = 1 - mutated_genotype[index]  # Invertir el bit
                mutated_individual = Individual(mutated_genotype)
                new_population.append(mutated_individual)
            else:
                new_population.append(individual)
        return new_population
