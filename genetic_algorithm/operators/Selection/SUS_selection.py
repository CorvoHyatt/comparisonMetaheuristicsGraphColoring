from typing import List
from random import uniform

import numpy as np
from genetic_algorithm.Individuals.individual import Individual
from genetic_algorithm.operators.Selection.selection_operators import SelectionOperator


class StochasticUniversalSampling(SelectionOperator):
    @staticmethod
    def select(population: List[Individual]) -> List[Individual]:
        fitness_values = [individual.fitness for individual in population]
        total_fitness = sum(fitness_values)
        selection_space = total_fitness / len(population)

        start = uniform(0, selection_space)
        points = [start + i * selection_space for i in range(len(population) + 1)]

        selected_parents = []
        current_index = 0
        current_accumulated_fitness = fitness_values[0]
        while len(selected_parents) < len(population) + 1:  # Devolver n + 1 individuos
            while current_accumulated_fitness < points[len(selected_parents)]:
                current_index = (current_index + 1) % len(population)
                current_accumulated_fitness += fitness_values[current_index]
            selected_parents.append(population[current_index])

        return selected_parents
