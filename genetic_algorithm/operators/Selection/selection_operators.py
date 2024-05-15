from typing import List

from genetic_algorithm.Individuals.individual import Individual


class SelectionOperator:
    @staticmethod
    def select(population: List[Individual]) -> List[Individual]:
        raise NotImplementedError("Método select debe ser implementado por subclases")
