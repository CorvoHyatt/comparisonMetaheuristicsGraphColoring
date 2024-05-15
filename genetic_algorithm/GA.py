import sys
import time
from typing import List, Literal
from genetic_algorithm.Individuals.individual import Individual
from genetic_algorithm.operators.Crossover.crossover_operators import CrossoverOperator
from genetic_algorithm.operators.Crossover.k_points_crossover import Kpoints
from genetic_algorithm.operators.Crossover.one_point_crossover import OnePoint
from genetic_algorithm.operators.Crossover.ordered_crossover import OrderedOX1
from genetic_algorithm.operators.Crossover.uniform_crossover import Uniform
from genetic_algorithm.operators.Mutation.bit_inversion_mutation import BitInversion
from genetic_algorithm.operators.Mutation.inversion_mutation import Inversion
from genetic_algorithm.operators.Mutation.mutation_operators import MutationOperator
from genetic_algorithm.operators.Mutation.shuffle_mutation import Shuffle
from genetic_algorithm.operators.Mutation.swap_mutation import Swap
from genetic_algorithm.operators.Selection.SUS_selection import (
    StochasticUniversalSampling,
)
from genetic_algorithm.operators.Selection.rank_selection import RankSelection
from genetic_algorithm.operators.Selection.roulette_selection import RouletteSelection
from genetic_algorithm.operators.Selection.scaling_selection import ScalingSelection
from genetic_algorithm.operators.Selection.selection_operators import SelectionOperator
from genetic_algorithm.operators.Selection.tournament_selection import (
    TournamentSelection,
)
from genetic_algorithm.population_generators.binary_generator import (
    BinaryPopulationGenerator,
)
from genetic_algorithm.population_generators.combinatory_generator import (
    CombinatoryPopulationGenerator,
)
from genetic_algorithm.population_generators.permutation_generator import (
    PermutationPopulationGenerator,
)
from genetic_algorithm.population_generators.population_generator import (
    PopulationGenerator,
)
from genetic_algorithm.utils.utils import (
    calcular_bits,
    calcular_modulo,
    calcular_promedio_fitness,
)


class GeneticAlgorithm:
    def __init__(
        self,
        selection_operator: Literal["rank", "roulette", "scaling", "SUS", "tournament"],
        crossover_operator: Literal["kpoints", "onepoint", "ordered", "uniform"],
        mutation_operator: Literal["bitinversion", "inversion", "shuffle", "swap"],
        stopping_criteria_type: Literal[
            "function_calls", "generations", "found_optimal", "nochangebest"
        ] = "nochangebest",
        max_call_functions: int = None,
        max_generations: int = None,
        optimal_solution: int = None,
        max_nochange_best: int = None,
        long_term_memory_reset: bool = True,
        problem_type: Literal["COP", "BenchMark"] = "BenchMark",
        limits: tuple[int, int] = [0, 32],
        precision: float = 0.00001,
        variables: int = 1,
        min_or_max: Literal["min", "max"] = "min",
        population_size: int = 100,
        probability_mutation: int = 7,
        codification: Literal["binary", "permutation", "combination"] = "permutation",
    ):
        self.population_size = population_size
        if selection_operator == "rank":
            self.selection_operator = RankSelection
        elif selection_operator == "roulette":
            self.selection_operator = RouletteSelection
        elif selection_operator == "scaling":
            self.selection_operator = ScalingSelection
        elif selection_operator == "SUS":
            self.selection_operator = StochasticUniversalSampling
        elif selection_operator == "tournament":
            self.selection_operator = TournamentSelection

        if crossover_operator == "kpoints":
            self.crossover_operator = Kpoints
        elif crossover_operator == "onepoint":
            self.crossover_operator = OnePoint
        elif crossover_operator == "ordered":
            self.crossover_operator = OrderedOX1
        elif crossover_operator == "uniform":
            self.crossover_operator = Uniform

        if mutation_operator == "bitinversion":
            self.mutation_operator = BitInversion
        elif mutation_operator == "inversion":
            self.mutation_operator = Inversion
        elif mutation_operator == "shuffle":
            self.mutation_operator = Shuffle
        elif mutation_operator == "swap":
            self.mutation_operator = Swap
        self.precision = precision
        self.variables = variables
        self.min_or_max = min_or_max
        self.probability_mutation = probability_mutation
        self.stopping_criteria_type = stopping_criteria_type
        self.max_call_functions = max_call_functions
        self.max_generations = max_generations
        self.optimal_solution = optimal_solution
        self.max_nochange_best = max_nochange_best
        self.long_term_memory_reset = long_term_memory_reset
        self.problem_type = problem_type
        self.limits = limits
        if codification == "binary":
            self.codification = "binary"
            self.population_generator = BinaryPopulationGenerator
        elif codification == "permutation":
            self.codification = "permutation"
            self.population_generator = PermutationPopulationGenerator
        else:
            self.codification = "combination"
            self.population_generator = CombinatoryPopulationGenerator

    def _clear(self, objetive):
        self._cost_worst = []
        self._cost_best = []
        self._cost_prom = []
        self.actual_best = None
        self.generations = 0
        self.best_nochange_conunter = 0
        self.function_call_counter = 0
        self.objetive = objetive

    def update_costs(self, population: List[Individual]):
        best: Individual = (min if self.min_or_max == "min" else max)(
            population, key=lambda individual: individual.fitness
        )
        if self.generations != 0:
            is_better = (
                best.fitness < self.actual_best.fitness
                if self.min_or_max == "min"
                else best.fitness > self.actual_best.fitness
            )
            if not is_better:
                self.best_nochange_conunter += 1

        self.actual_best = best
        self._cost_best.append(best.fitness)
        worst = (max if self.min_or_max == "min" else min)(
            population, key=lambda individual: individual.fitness
        )
        self._cost_worst.append(worst.fitness)
        prom = calcular_promedio_fitness(population)
        self._cost_prom.append(prom)

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
            self.stopping_criteria_type == "generations"
            and self.generations > self.max_generations
        ):
            return False

        if (
            self.stopping_criteria_type == "found_optimal"
            and self.best == self.optimal_solution
        ):
            return False

        return True

    def initialize_population(self) -> List[Individual]:
        if self.codification == "binary":
            bits_enteros, bits_decimales = calcular_bits(self.limits[1], self.precision)
            genotype_structure = [bits_enteros, bits_decimales, self.variables]
            return self.population_generator.generate_population(
                self.population_size, genotype_structure
            )
        elif self.codification == "permutation":
            return self.population_generator.generate_population(
                self.population_size, self.limits[1]
            )
        else:
            return self.population_generator.generate_population(
                self.population_size, self.limits[1]
            )

    def select_parents(self, population: List[Individual]) -> List[Individual]:
        # Lógica para seleccionar padres
        return self.selection_operator.select(population)

    def crossover(self, population: List[Individual]) -> List[Individual]:
        # Lógica para realizar el cruce
        return self.crossover_operator.crossover(population)

    def mutate(self, population: List[Individual]) -> List[Individual]:
        # Lógica para realizar la mutación
        return self.mutation_operator.mutate(population, self.probability_mutation)

    def evaluate_fitness(self, population: List[Individual]) -> List[Individual]:
        evaluated_population = []
        for individual in population:
            individual.fitness = self.objetive(individual.genotype)
            evaluated_population.append(individual)
            self.function_call_counter += 1
        return evaluated_population

    def evolve(self, objetive) -> List[Individual]:
        self._clear(objetive)
        decimal = len(str(calcular_modulo(self.precision))) - 1
        population = self.initialize_population()
        tiempo_inicio = time.time()
        while self.stopping_criteria():
            population_evaluated = self.evaluate_fitness(population)
            self.update_costs(population_evaluated)
            population_selected = self.select_parents(population_evaluated)
            population_cross = self.crossover(population_selected)
            population = self.mutate(population_cross)

            if self.problem_type == "COP":
                sys.stderr.write(
                    "\r Generations %d | call_functions %d | Best: %.2f"
                    % (
                        self.generations,
                        self.function_call_counter,
                        self.actual_best.fitness,
                    )
                )
            else:
                sys.stderr.write(
                    f"\r Generations %d | call_functions %d | Best: %.{decimal}f"
                    % (
                        self.generations,
                        self.function_call_counter,
                        self.actual_best.fitness,
                    )
                )
            self.generations += 1
            sys.stderr.flush()
        sys.stderr.flush()
        if self.problem_type == "COP":
            sys.stderr.write(
                "\r Generations %d | call_functions %d | Best: %.2f"
                % (
                    self.generations,
                    self.function_call_counter,
                    self.actual_best.fitness,
                )
            )
        else:
            sys.stderr.write(
                f"\r Generations %d | call_functions %d | Best: %.{decimal}f"
                % (
                    self.generations,
                    self.function_call_counter,
                    self.actual_best.fitness,
                )
            )

        tiempo_fin = time.time()
        tiempo_total = tiempo_fin - tiempo_inicio
        print(
            f"Tiempo de ejecución: {int(tiempo_total // 3600):02d}:{int((tiempo_total % 3600) // 60):02d}:{int(tiempo_total % 60):02d}"
        )
        return self.actual_best
