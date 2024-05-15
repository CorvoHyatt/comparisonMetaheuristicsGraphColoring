from typing import List
from random import sample

import numpy as np
from genetic_algorithm.Individuals.individual import Individual


class TournamentSelection:
    @staticmethod
    def select(
        population: List[Individual], tournament_size: int = 3
    ) -> List[Individual]:
        selected_parents = []
        while len(selected_parents) < len(population) + 1:
            # Seleccionar un subconjunto aleatorio de individuos para el torneo
            tournament = sample(population, tournament_size)
            # Seleccionar al individuo con el mejor fitness en el torneo
            winner = min(tournament, key=lambda x: x.fitness)
            # Verificar que el nuevo padre sea diferente de los padres seleccionados previamente
            if not selected_parents or winner != selected_parents[-1]:
                selected_parents.append(winner)
        return selected_parents
