import numpy as np


class Individual:
    def __init__(self, genotype: np.ndarray):
        self.genotype = genotype
        self.fitness = None
