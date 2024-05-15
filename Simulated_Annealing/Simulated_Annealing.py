from typing import Literal
import numpy as np
import math
import time
from utils import *
import pandas as pd


class SimulatedAnnealing(object):
    def __init__(
        self,
        restriction_fun=None,
        problem_type: Literal["COP", "BenchMark"] = "BenchMark",
        codification: Literal["binary", "permutation", "combination", "real"] = "real",
        cooling: Literal["linear", "geometric", "logarithmic"] = "geometric",
        min_or_max: Literal["min", "max"] = "min",
        limits: tuple[int, int] = [0, 32],
        precision: float = 0.00001,
        variables: int = 1,
        alpha: float = 0.95,
        beta: float = 1,
        time: int = 0,
        equilibrium: int = 10,
        temperature: float = 200,
        final_temperature: float = 0.1,
    ) -> None:
        self.restriction_fun = restriction_fun
        self.problem_type = problem_type
        self.codification = codification
        self.min_or_max = min_or_max
        self.variables = variables
        self.cooling = cooling
        self.precision = precision
        self.limits = limits
        self.beta = beta
        self.time = time
        self.alpha = alpha
        self.equilibrium = equilibrium
        self.temperature = temperature
        self.final_temperature = final_temperature

        if problem_type == "BenchMark":
            self.bits_enteros, self.bits_decimales = calcular_bits(
                self.limits[1], self.precision
            )

    def cost_function(self, f, solution):
        if self.codification == "binary":
            return f(
                solution,
                self.bits_enteros,
                self.bits_decimales,
                self.variables,
                self.precision,
            )

        elif self.codification == "combination":
            return f(solution, self.graph)

        elif self.codification == "permutation":
            return f(solution, self.flows, self.distances)

        return False

    def create_first_solution(self):
        first_solution = []
        if self.codification == "binary":
            first_solution = np.random.choice(
                [0, 1],
                size=(self.bits_enteros + self.bits_decimales + 1) * self.variables,
            )

        if self.codification == "combination":
            first_solution = np.random.randint(
                1, self.limits[1] + 1, size=self.limits[1]
            )

        if self.codification == "permutation":
            first_solution = np.arange(1, self.limits[1] + 1)
            np.random.shuffle(first_solution)

        return first_solution

    def create_neighbor_solution(self, actual_solution):
        neighbor = []
        if self.codification == "binary":
            neighbor = actual_solution.copy()
            indice = np.random.randint(0, len(neighbor))
            neighbor[indice] = 1 - neighbor[indice]

        elif self.codification == "permutation":
            neighbor = actual_solution.copy()
            idx1, idx2 = np.random.choice(len(actual_solution), 2, replace=False)
            while idx1 == idx2:
                idx2 = np.random.choice(len(actual_solution))
            neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]

        elif self.codification == "combination":

            # neighbor = np.random.randint(1, self.limits[1] + 1, size=self.limits[1])
            neighbor = actual_solution.copy()
            idx = np.random.choice(len(actual_solution), replace=False)
            neighbor[idx] = np.random.choice(len(actual_solution)) + 1

        return neighbor

    def aceptance_probability(self, deltaE, temperature):
        try:
            if self.min_or_max == "max":
                r = math.exp(-(-deltaE / temperature))
            else:
                r = math.exp(-deltaE / temperature)  # Reporte

        except OverflowError:
            r = float("inf")
        return r

    def update_temperature(self, temperature, i):
        new_temperature = 0

        if self.cooling == "geometric":
            new_temperature = temperature * self.alpha

        if self.cooling == "linear":
            new_temperature = temperature - i * self.beta

        if self.cooling == "logarithmic":
            new_temperature = (self.alpha * temperature) / (math.log(1 + i))

        return new_temperature

    def fit(self, objetive):
        self.cost_ = []
        actual_solutions = self.create_first_solution()
        epoch = 0
        number_tested_solution = 0
        aceptanced = 100
        decimal = len(str(calcular_modulo(self.precision))) - 1
        tiempo_inicio = time.time()
        optimal = []
        while self.temperature > self.final_temperature:

            number_worst_solution_acepted = 0
            i = 0
            while i < self.equilibrium:
                random_solutions = self.create_neighbor_solution(actual_solutions)
                number_tested_solution += 1
                delta_E = objetive(random_solutions) - objetive(actual_solutions)
                if validar_min_max(delta_E, self.min_or_max):
                    actual_solutions = random_solutions.copy()
                    optimal = actual_solutions
                else:
                    deg_deltaE = self.aceptance_probability(delta_E, self.temperature)
                    if np.random.uniform(0, 1) < deg_deltaE:
                        actual_solutions = random_solutions.copy()
                        number_worst_solution_acepted += 1
                        optimal = actual_solutions

                fxy = 0
                fxy = objetive(actual_solutions)
                self.cost_.append(fxy)
                epoch_strlen = len(str(epoch))

                imprimir_valores(
                    decimal,
                    epoch_strlen,
                    epoch,
                    i,
                    self.temperature,
                    fxy,
                    aceptanced,
                )
                i += 1
                epoch += 1
            aceptanced = number_worst_solution_acepted * 100 / number_tested_solution
            self.temperature = self.update_temperature(self.temperature, i)
            tiempo_fin = time.time()
        tiempo_total = tiempo_fin - tiempo_inicio
        print(
            f"Tiempo de ejecución: {int(tiempo_total // 3600):02d}:{int((tiempo_total % 3600) // 60):02d}:{int(tiempo_total % 60):02d}"
        )
        return optimal
        # print(f"Temperatura actualizada: {temperature}")
