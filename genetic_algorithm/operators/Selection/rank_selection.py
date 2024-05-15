from typing import List
from random import choices

import numpy as np

from genetic_algorithm.Individuals.individual import Individual
from genetic_algorithm.operators.Selection.selection_operators import SelectionOperator


class RankSelection(SelectionOperator):
    @staticmethod
    def select(population: List[Individual]) -> List[Individual]:
        sorted_population = sorted(population, key=lambda x: x.fitness)

        # ranks = list(range(1, len(sorted_population) + 1))
        ranks = list(range(len(sorted_population), 0, -1))
        total_ranks = sum(ranks)
        selection_probabilities = [rank / total_ranks for rank in ranks]

        selected_parents = []
        while len(selected_parents) < len(population) + 1:
            new_parent = choices(
                sorted_population, weights=selection_probabilities, k=1
            )[0]
            if not selected_parents or new_parent != selected_parents[-1]:
                selected_parents.append(new_parent)

        return selected_parents
