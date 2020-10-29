import math
import time
from random import choices, random, randint, randrange
from typing import List, Tuple

Chromosome = List[int]
Population = List[Chromosome]


def generate_chromosome(length: int) -> Chromosome:
    return choices([0, 1], k=length)


def genereate_population(size: int, chrom_length: int) -> Population:
    return [generate_chromosome(chrom_length) for _ in range(size)]


def decode(chrom: Chromosome) -> Tuple[float, float]:
    x1 = chrom[0:int(len(chrom)/2)]
    x2 = chrom[int(len(chrom)/2):]
    valx1 = 0
    valx2 = 0
    penyebut = 0

    k = 1
    while k < int(len(chrom)/2)+1:
        penyebut += pow(2, -k)
        k += 1

    for i in range(len(x1)):
        valx1 += x1[i]*pow(2, -(i+1))

    for j in range(len(x2)):
        valx2 += x2[j]*pow(2, -(j+1))

    valuex1 = -1 + (3/penyebut) * valx1
    valuex2 = -1 + (2/penyebut) * valx2

    return valuex1, valuex2


def fitness(chrom: Chromosome) -> float:
    x1, x2 = decode(chrom)
    h = math.cos(x1) * math.sin(x2) - (x1 / (pow(x2, 2) + 1))

    return pow(3, -h)


def select_parent(pop: Population, k: int) -> Chromosome:     # Tournament selection
    best=[]
    for _ in range(k):
        individu = pop[randrange(len(pop))]
        if best == [] or fitness(individu) > fitness(best):
            best = individu
    return best


def single_point_crossover(a: Chromosome, b: Chromosome, chance: float) -> Tuple[Chromosome, Chromosome]:
    if random() < chance:
        p = randint(1, len(a) - 1)
        return a[0:p] + b[p:], b[0:p] + a[p:]
    return a, b


def mutation(chrom: Chromosome, chance: float) -> Chromosome:
    index = randrange(len(chrom))
    chrom[index] = chrom[index] if random() > chance else 1 - chrom[index]
    return chrom


# Running
generation_limit = 100
cross_chance = 0.65
mutation_chance = 0.15

start = time.time()
population = genereate_population(100, 20)   # initial population

for i in range(generation_limit):
    # sorting the population
    population = sorted(
        population,
        key=lambda chromosome: fitness(chromosome),
        reverse=True
    )

    # Fitness Threshold
    if fitness(population[0]) > 9.21:
        break

    # Elitism
    next_gen = population[0:2]

    # Mating pool
    for _ in range(int(len(population) / 2) - 1):
        parent1 = select_parent(population, 5)
        parent2 = select_parent(population, 5)
        while parent1 == parent2:
            parent2 = select_parent(population, 5)
        child_a, child_b = single_point_crossover(parent1, parent2, cross_chance)
        child_a = mutation(child_a, mutation_chance)
        child_b = mutation(child_b, mutation_chance)
        next_gen += [child_a, child_b]

    population = next_gen

# last sort just to make sure
population = sorted(
        population,
        key=lambda chromosome: fitness(chromosome),
        reverse=True
    )

# Decode best individual
x1, x2 = decode(population[0])
end = time.time()


# Result screen
print(f"\ngeneration #{i}")
print(f"time: {end-start}s")
print(f"\nbest chromosome: {population[0]}")
print(f"best solution: x1= {x1}, x2= {x2}")
print(f"fitness: {fitness(population[0])}")