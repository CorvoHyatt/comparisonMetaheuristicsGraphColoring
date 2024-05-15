import numpy as np
from genetic_algorithm.Individuals.individual import Individual


def check_equals(individual1: Individual, individual2: Individual) -> bool:
    flag = False
    if np.array_equal(individual1.genotype, individual2.genotype):
        flag = True
    return flag
