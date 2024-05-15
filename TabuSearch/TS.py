import sys
import time
import numpy as np
from typing import Literal
from .utils import *
from IPython.display import clear_output


class TabuSearch(object):
    def __init__(
        self,
        first_point,
        tabu_list_size,
        number_of_points,
        diversification_type: Literal["static", "oscillation", "None"] = "static",
        diversification_size: int = 20,
        stopping_criteria_type: Literal[
            "function_calls", "iterations", "found_optimal", "nochangebest"
        ] = "nochangebest",
        max_call_functions: int = None,
        max_iterations: int = None,
        optimal_solution: int = None,
        max_nochange_best: int = None,
        long_term_memory_reset: bool = True,
        problem_type: Literal["COP", "BenchMark"] = "BenchMark",
        min_or_max: Literal["min", "max"] = "min",
        codification: Literal[
            "binary", "permutation", "combination", "real"
        ] = "permutation",
    ) -> None:
        self.first_point = first_point
        self.tabu_list_size = tabu_list_size
        self.number_of_points = number_of_points
        self.diversification_type = diversification_type
        self.diversification_size = diversification_size
        self.stopping_criteria_type = stopping_criteria_type
        self.max_call_functions = max_call_functions
        self.max_iterations = max_iterations
        self.optimal_solution = optimal_solution
        self.max_nochange_best = max_nochange_best
        self.long_term_memory_reset = long_term_memory_reset
        self.problem_type = problem_type
        self.min_or_max = min_or_max
        self.codification = codification

    def __str__(self):
        return f"iterations: {self.iterations} | call_functions: {self.function_call_counter} | best: {self.best} | actual_sol: {self.actual_solution_value}"

    def _clear(self, objetive):
        self._cost_actual = []
        self._cost_best = []
        self.iterations = 0
        self.best_nochange_conunter = 0
        self.function_call_counter = 0
        self.points = []
        self.tabu_list = ["" for numero in range(self.tabu_list_size)]
        self.long_term_memory = {}
        self.actual_solution = self.first_point
        self.objetive = objetive
        self.best = objetive(self.first_point)
        self.actual_solution_value = self.best
        self.function_call_counter += 1
        self._cost_best.append(self.best)

    def stopping_criteria(self) -> bool:
        if (
            self.stopping_criteria_type == "nochangebest"
            and self.best_nochange_conunter > self.max_nochange_best
        ):
            return False

        if (
            self.stopping_criteria_type == "function_calls"
            and self.function_call_counter <= self.max_call_functions
        ):
            return False
        if (
            self.stopping_criteria_type == "iterations"
            and self.iterations > self.max_iterations
        ):
            return False

        if (
            self.stopping_criteria_type == "found_optimal"
            and self.best == self.optimal_solution
        ):
            return False

        return True

    def move(self, actual_solution: list[int]) -> dict:
        points = []
        # Permutation
        if self.codification == "permutation":
            for _ in range(self.number_of_points):

                neighbor_val = actual_solution.copy()
                idx1, idx2 = np.random.choice(len(actual_solution), 2, replace=False)
                while idx1 == idx2:
                    idx2 = np.random.choice(len(actual_solution))

                neighbor_val[idx1], neighbor_val[idx2] = (
                    neighbor_val[idx2],
                    neighbor_val[idx1],
                )
                neighbor = (f"{idx1},{idx2}", neighbor_val)
                points.append(neighbor)

        # Combination
        if self.codification == "combination":
            for _ in range(self.number_of_points):
                neighbor_val = actual_solution.copy()
                idx = np.random.choice(len(actual_solution), replace=False)
                neighbor_val[idx] = np.random.choice(len(actual_solution)) + 1
                neighbor = (f"{idx},{neighbor_val[idx]}", neighbor_val)
                points.append(neighbor)
        # TODO Binary
        self.points = points

        return points

    def evaluate_points(self):
        resultados = []

        for clave, arreglo in self.points:
            resultado_funcion_costo = self.objetive(arreglo)
            self.function_call_counter += 1
            valor_diccionario = self.long_term_memory.get(clave, 0)

            resultados.append(
                [
                    clave,
                    arreglo,
                    resultado_funcion_costo,
                    valor_diccionario,
                    resultado_funcion_costo + valor_diccionario,
                ]
            )
        # Diversificación estatica
        if (
            self.iterations % self.diversification_size == 0
            and self.diversification_type == "static"
            and self.iterations != 0
        ):
            self.diversification_static(resultados)
            return True

        if self.criterio_aspiracion(resultados):
            return True
        resultados_ = resultados
        while True:
            if len(resultados_) != 0:
                optimal_value = (min if self.min_or_max == "min" else max)(
                    resultados_, key=lambda punto: punto[2]
                )
                if optimal_value[0] in self.tabu_list:

                    resultados_ = [
                        punto
                        for punto in resultados_
                        if not np.array_equal(punto[1], optimal_value[1])
                    ]

                else:
                    is_better = (
                        optimal_value[2] < self.best
                        if self.min_or_max == "min"
                        else optimal_value[2] > self.best
                    )

                    if is_better:
                        self.best = optimal_value[2]
                        self.best_nochange_conunter = 0

                    self.best_nochange_conunter += 1
                    self.update_tabu_frec(optimal_value)
                    self.actual_solution = optimal_value[1]
                    self.actual_solution_value = optimal_value[4]
                    self._cost_actual.append(optimal_value[4])
                    return True
            else:
                # optimal_value = (min if self.min_or_max == "min" else max)(
                #     resultados_, key=lambda punto: punto[2]
                # )
                self.best_nochange_conunter += 1
                # self._cost_actual.append(optimal_value[2])
                self._cost_actual.append(self.actual_solution_value)
                return True

    def diversification_static(self, resultados):

        optimal_value = (min if self.min_or_max == "min" else max)(
            resultados, key=lambda punto: punto[4]
        )
        is_better = (
            optimal_value[4] < self.best
            if self.min_or_max == "min"
            else optimal_value[4] > self.best
        )
        if is_better:
            self.best = optimal_value[4]
            self.best_nochange_conunter = 0

        if self.long_term_memory_reset == True:
            self.long_term_memory = {}
            # self.tabu_list = ["" for _ in range(self.tabu_list_size)]

        self.best_nochange_conunter += 1
        self.actual_solution = optimal_value[1]
        self.actual_solution_value = optimal_value[2]
        self._cost_actual.append(optimal_value[2])

    def criterio_aspiracion(self, resultados):
        optimal_value = (min if self.min_or_max == "min" else max)(
            resultados, key=lambda punto: punto[2]
        )
        is_better = (
            optimal_value[2] < self.best
            if self.min_or_max == "min"
            else optimal_value[2] > self.best
        )

        if is_better:
            self.best = optimal_value[2]
            self.best_nochange_conunter = 0
            self.update_tabu_frec(optimal_value)
            self.actual_solution = optimal_value[1]
            self.actual_solution_value = optimal_value[2]
            self._cost_actual.append(optimal_value[2])
            return True
        return False

    def update_tabu_frec(self, value: list) -> None:
        self.tabu_list[self.iterations % self.tabu_list_size] = value[0]
        if value[0] in self.long_term_memory:
            self.long_term_memory[value[0]] += 1
        else:
            self.long_term_memory[value[0]] = 1

    def fit(self, objetive) -> list:
        self._clear(objetive)
        tiempo_inicio = time.time()
        while self.stopping_criteria():
            self.move(self.actual_solution)
            self.evaluate_points()

            self._cost_best.append(self.best)
            sys.stderr.write(
                "\r iterations %d | call_functions %d | Best: %.2f | actual_sol: %.2f"
                % (
                    self.iterations,
                    self.function_call_counter,
                    self.best,
                    self.actual_solution_value,
                )
            )

            sys.stderr.flush()
            self.iterations += 1
        tiempo_fin = time.time()
        tiempo_total = tiempo_fin - tiempo_inicio
        sys.stderr.write(
            "\r iterations %d | call_functions %d | Best: %.2f | actual_sol: %.2f"
            % (
                self.iterations,
                self.function_call_counter,
                self.best,
                self.actual_solution_value,
            )
        )
        print(
            f"Tiempo de ejecución: {int(tiempo_total // 3600):02d}:{int((tiempo_total % 3600) // 60):02d}:{int(tiempo_total % 60):02d}"
        )
        return self.actual_solution
