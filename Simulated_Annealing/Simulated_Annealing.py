from typing import Literal
import numpy as np
import math
import time
from .utils import *
import pandas as pd


class SimulatedAnnealing(object):
    def __init__(
        self,
        stopping_criteria_type: Literal[
            "function_calls",
            "default",
        ] = "function_calls",
        max_call_functions=100,
        verbose=False,
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
        self.verbose = verbose

        self.stopping_criteria_type = stopping_criteria_type
        self.max_call_functions = max_call_functions
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

        if self.problem_type == "BenchMark":
            self.bits_enteros, self.bits_decimales = calcular_bits(
                self.limits[1], self.precision
            )

    def stopping_criteria(self) -> bool:

        if (
            self.stopping_criteria_type == "function_calls"
            and self.function_call_counter >= self.max_call_functions
        ):
            return False
        elif (
            self.stopping_criteria_type == "default"
            and self.temperature > self.final_temperature
        ):
            return False

        return True

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
        self.function_call_counter = 0
        actual_solutions = self.create_first_solution()
        self.epoch = 0
        self.i = 0
        number_tested_solution = 0
        aceptanced = 100
        decimal = len(str(calcular_modulo(self.precision))) - 1
        tiempo_inicio = time.time()
        optimal = []
        while self.stopping_criteria():

            number_worst_solution_acepted = 0
            self.i = 0
            while self.i < self.equilibrium:
                random_solutions = self.create_neighbor_solution(actual_solutions)
                number_tested_solution += 1
                fxyrand = objetive(random_solutions)
                fxy = objetive(actual_solutions)
                delta_E = fxyrand - fxy
                self.function_call_counter += 2
                aceptance_flag = False
                if validar_min_max(delta_E, self.min_or_max):
                    actual_solutions = random_solutions.copy()
                    optimal = actual_solutions
                else:
                    deg_deltaE = self.aceptance_probability(delta_E, self.temperature)
                    if np.random.uniform(0, 1) < deg_deltaE:
                        actual_solutions = random_solutions.copy()
                        number_worst_solution_acepted += 1
                        optimal = actual_solutions
                        aceptance_flag = True

                if aceptance_flag:
                    self.cost_.append(fxyrand)
                else:
                    self.cost_.append(fxy)

                self.epoch_strlen = len(str(self.epoch))
                if self.verbose:
                    imprimir_valores(
                        decimal,
                        self.epoch_strlen,
                        self.epoch,
                        self.i,
                        self.temperature,
                        fxy,
                        aceptanced,
                        self.function_call_counter,
                    )
                self.i += 1
                self.epoch += 1
            self.aceptanced = (
                number_worst_solution_acepted * 100 / number_tested_solution
            )
            self.temperature = self.update_temperature(self.temperature, self.i)

        print(
            "\r%0*d Epoch | Equilibrium %d | Temperature %.2f "
            "| Cost function: %.{}f  | Aceptance: %.2f | Function Call: %d".format(
                decimal
            )
            % (
                self.epoch_strlen,
                self.epoch + 1,
                self.i + 1,
                self.temperature,
                fxy,
                aceptanced,
                self.function_call_counter,
            )
        )
        print(f"Solucion: {optimal}")
        tiempo_fin = time.time()
        tiempo_total = tiempo_fin - tiempo_inicio
        print(
            f"Tiempo de ejecución: {int(tiempo_total // 3600):02d}:{int((tiempo_total % 3600) // 60):02d}:{int(tiempo_total % 60):02d}"
        )
        return optimal
