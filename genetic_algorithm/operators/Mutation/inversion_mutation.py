from typing import List

import numpy as np
from genetic_algorithm.Individuals.individual import Individual
from genetic_algorithm.operators.Mutation.mutation_operators import MutationOperator


class Inversion(MutationOperator):
    @staticmethod
    def mutate(population: List[Individual], probability: int) -> List[Individual]:
        new_population = []
        for individual in population:
            random_prob = np.random.randint(
                1, 1001
            )  # Generar un número aleatorio entre 1 y 1000
            if random_prob <= probability:
                mutated_genotype = np.copy(individual.genotype)
                # Seleccionar dos índices aleatorios diferentes y realizar la inversión de bits
                start, end = np.random.choice(len(mutated_genotype), 2, replace=False)
                start, end = min(start, end), max(start, end)
                mutated_genotype[start : end + 1] = mutated_genotype[start : end + 1][
                    ::-1
                ]  # Invertir los bits en el rango seleccionado
                mutated_individual = Individual(mutated_genotype)
                new_population.append(mutated_individual)
            else:
                new_population.append(individual)
        return new_population
