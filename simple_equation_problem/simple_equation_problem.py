#!/usr/bin/env python3

from __future__ import annotations
from random import choice, random, randrange

import sys, os
sys.path.append(os.pardir)
from ga import Chromosome, GeneticAlgorithm as GA

class SimpleEquationProblem(Chromosome):

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @classmethod
    def new_random_instance(cls) -> SimpleEquationProblem:
        x = randrange(100)
        y = randrange(100)
        return SimpleEquationProblem(x, y)

    def problem(self, x: int, y: int) -> int:
        return 6 * x - x ** 2 + 4 * y - y ** 2

    @property
    def fitness(self) -> float:
        return float(self.problem(self.x, self.y))

    def crossover(self, other: SimpleEquationProblem) -> None:
        self.x = other.x
        other.y = self.y

    def mutation(self) -> None:
        value = choice([-1, 1])
        if random() < 0.5:
            self.x += value
        else:
            self.y += value

    def __str__(self) -> str:
        x = self.x
        y = self.y
        fitness = self.fitness
        return str(f'x={x:2d}  y={y:2d}  fitness={fitness:7,.0f}')

if __name__ == '__main__':
    population = GA.generate_population(n=10, chromosome=SimpleEquationProblem)
    GA.print_population(population)
    print()

    for i in range(100):
        best_chromosome = max(population)
        print(f'<{i:2d}>  {best_chromosome}')
        if 13 <= best_chromosome.fitness:
            break
        elite_population = GA.elite_selection(n=1, population=population)
        selected_population = GA.tournament_selection(n=9, population=population, tournament_size=3)
        GA.crossover(selected_population, probability=0.5)
        GA.mutation(selected_population, probability=0.5)
        population = elite_population + selected_population
