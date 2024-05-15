import sys
import pprint
from typing import List
import numpy as np

from genetic_algorithm.Individuals.individual import Individual


class BinaryPopulationGenerator:

    @staticmethod
    def generate_population(
        population_size: int, genotype_structure: List[int]
    ) -> List[Individual]:
        bits_enteros, bits_decimales, variables = genotype_structure
        population = set()
        while len(population) < population_size:
            genotype = np.random.choice(
                [0, 1],
                size=(bits_enteros + bits_decimales + 1) * variables,
            )
            individual = Individual(genotype)
            population.add(individual)

        return population


# population = BinaryPopulationGenerator.generate_population(30, [2, 3, 3])
