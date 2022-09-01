#!/usr/bin/env python3

from __future__ import annotations
from abc import ABC, abstractmethod

class Chromosome(ABC):

    @classmethod
    @abstractmethod
    def new_random_instance(cls, **kwargs) -> Chromosome:
        ...

    @property
    @abstractmethod
    def fitness(self) -> float:
        ...

    @abstractmethod
    def crossover(self, other: Chromosome) -> None:
        ...

    @abstractmethod
    def mutation(self) -> None:
        ...

    def __lt__(self, other: Chromosome) -> bool:
        return bool(self.fitness < other.fitness)

if __name__ == '__main__':
    pass
