# roulette_selection.py

from typing import List
from random import choices

import numpy as np
from genetic_algorithm.Individuals.individual import Individual
from genetic_algorithm.operators.Selection.selection_operators import SelectionOperator


class RouletteSelection(SelectionOperator):
    @staticmethod
    def select(population: List[Individual]) -> List[Individual]:
        fitness_values = [individual.fitness for individual in population]

        selected_parents = []
        while len(selected_parents) < len(population) + 1:
            # Seleccionar un nuevo padre con pesos proporcionales a los valores de aptitud
            new_parent = choices(population, weights=fitness_values, k=1)[0]

            # Verificar que el nuevo padre sea diferente del último padre seleccionado
            if not selected_parents or not np.array_equal(
                new_parent.genotype, selected_parents[-1].genotype
            ):
                selected_parents.append(new_parent)

        return selected_parents
