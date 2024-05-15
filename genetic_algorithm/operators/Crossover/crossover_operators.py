from typing import List
from genetic_algorithm.Individuals.individual import Individual


class CrossoverOperator:
    @staticmethod
    def crossover(population_selected: List[Individual]) -> List[Individual]:
        raise NotImplementedError(
            "Método crossover debe ser implementado por subclases"
        )
