from typing import List
from genetic_algorithm.Individuals.individual import Individual


class MutationOperator:
    def mutate(
        self, population: List[Individual], probability: int
    ) -> List[Individual]:
        raise NotImplementedError("Método mutate debe ser implementado por subclases")
