#!/usr/bin/env python3

from __future__ import annotations
from typing import TypedDict
from random import randrange
from bitarray import bitarray, util

import sys, os
sys.path.append(os.pardir)
from ga import Chromosome, GeneticAlgorithm as GA

Item = TypedDict('Item', capacity=int, value=int)

items: list[Item] = [
    {'capacity': 52, 'value': 16},
    {'capacity':  5, 'value': 54},
    {'capacity': 21, 'value': 57},
    {'capacity': 54, 'value':  4},
    {'capacity': 26, 'value': 44},
    {'capacity': 22, 'value': 83},
    {'capacity': 87, 'value': 87},
    {'capacity': 59, 'value': 14},
    {'capacity': 67, 'value': 28},
    {'capacity': 77, 'value': 43},
    {'capacity': 60, 'value':  9},
    {'capacity': 88, 'value': 89},
    {'capacity': 64, 'value':  6},
    {'capacity': 49, 'value': 54},
    {'capacity': 23, 'value': 77},
    {'capacity':  3, 'value': 34},
    {'capacity': 71, 'value': 21},
    {'capacity': 31, 'value': 36},
    {'capacity': 67, 'value': 49},
    {'capacity':  2, 'value': 34},
    {'capacity': 99, 'value': 11},
    {'capacity': 93, 'value': 65},
    {'capacity': 83, 'value':  9},
    {'capacity': 76, 'value': 42},
    {'capacity': 48, 'value': 32},
    {'capacity': 36, 'value': 99},
    {'capacity':  5, 'value': 93},
    {'capacity': 15, 'value': 15},
    {'capacity': 75, 'value': 49},
    {'capacity': 50, 'value': 92},
    {'capacity':  5, 'value': 85},
    {'capacity': 85, 'value': 57}]

class KnapsackProblem(Chromosome):

    def __init__(self, gene: bitarray, items: list[Item], knapsack_capacity: int) -> None:
        self.gene = gene
        self.items = items
        self.knapsack_capacity = knapsack_capacity

    @classmethod
    def new_random_instance(cls, items: list[Item], knapsack_capacity: int) -> KnapsackProblem:
        gene = util.urandom(len(items))
        return KnapsackProblem(gene, items, knapsack_capacity)

    def gene_expression(self) -> tuple[int, int]:
        capacity = 0
        value = 0
        for i, bit in enumerate(self.gene):
            if bit == 1:
                capacity += self.items[i]['capacity']
                value += self.items[i]['value']
        return capacity, value

    def problem(self, capacity: int, value: int) -> int:
        if self.knapsack_capacity < capacity:
            fitness = 0
        else:
            fitness = value
        return fitness

    @property
    def fitness(self) -> float:
        capacity, value = self.gene_expression()
        return float(self.problem(capacity, value))

    def crossover(self, other: KnapsackProblem) -> None:
        length = len(self.gene)
        point = length // 2
        self.gene[0:point] = other.gene[0:point]
        other.gene[point:length] = self.gene[point:length]

    def mutation(self) -> None:
        index = randrange(len(self.gene))
        self.gene[index] = not self.gene[index]

    def __str__(self) -> str:
        str_gene = self.gene.to01()
        capacity, value = self.gene_expression()
        fitness = self.fitness
        return str(f'gene={str_gene}  capacity={capacity:4d}  value={value:4d}  fitness={fitness:5.0f}')

if __name__ == '__main__':
    population = GA.generate_population(n=50, chromosome=KnapsackProblem, items=items, knapsack_capacity=1000)
    GA.print_population(population)
    print()

    for i in range(500):
        best_chromosome = max(population)
        print(f'<{i:3d}>  {best_chromosome}')
        elite_population = GA.elite_selection(n=1, population=population)
        selected_population = GA.roulette_wheel_selection(n=49, population=population)
        GA.crossover(selected_population, probability=0.7)
        GA.mutation(selected_population, probability=0.7)
        population = elite_population + selected_population
