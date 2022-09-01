#!/usr/bin/env python3

from __future__ import annotations
from copy import deepcopy
from heapq import nlargest
from random import choices, random, sample, shuffle

import sys, os
sys.path.append(os.pardir)
from ga.chromosome import Chromosome

class GeneticAlgorithm:

    @classmethod
    def generate_population(cls, n: int, chromosome: Chromosome, **kwargs) -> list[Chromosome]:
        population = [chromosome.new_random_instance(**kwargs) for _ in range(n)]
        return population

    @classmethod
    def print_population(cls, population: list[Chromosome]) -> None:
        for i, chromosome in enumerate(population):
            print(f'[{i:2d}]  {chromosome}')

    @classmethod
    def elite_selection(cls, n: int, population: list[Chromosome]) -> list[Chromosome]:
        selected_population = nlargest(n=n, iterable=population)
        return selected_population

    @classmethod
    def tournament_selection(cls, n: int, population: list[Chromosome], tournament_size: int) -> list[Chromosome]:
        selected_population: list[Chromosome] = []
        for _ in range(n):
            participants = sample(population, k=tournament_size)
            chromosome = nlargest(n=1, iterable=participants)[0]
            selected_population.append(deepcopy(chromosome))
        return selected_population

    @classmethod
    def roulette_wheel_selection(cls, n: int, population: list[Chromosome]) -> list[Chromosome]:
        offset = abs(min(population).fitness)
        weights = list(map(lambda fitness: fitness + offset, [chromosome.fitness for chromosome in population]))
        selected_population: list[Chromosome] = []
        for _ in range(n):
            chromosome = choices(population, weights, k=1)[0]
            selected_population.append(deepcopy(chromosome))
        return selected_population

    @classmethod
    def crossover(cls, population: list[Chromosome], probability: float) -> None:
        shuffle(population)
        for i, j in zip(range(len(population)), range(len(population) - 1, -1, -1)):
            if i >= j:
                break
            if random() < probability:
                population[i].crossover(population[j])

    @classmethod
    def mutation(cls, population: list[Chromosome], probability: float) -> None:
        for chromosome in population:
            if random() < probability:
                chromosome.mutation()

if __name__ == '__main__':
    pass
