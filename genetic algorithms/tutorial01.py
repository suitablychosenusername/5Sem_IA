import numpy as np
import random

# cria indivíduo
def generate_individual(n_genes: "n_bits") -> list:
  genes = []
  for i in range(n_genes):
    genes.append(round(random.uniform(0, 1))) # gera array de n bits
  return genes

# cria população
def let_there_be_life(n_individuals, n_bits) -> "two-dimensional list":
  population = []
  for i in range(n_individuals):
    population.append(generate_individual(n_bits))
  return population

# associa números em binário para cada valor do indivíduo
def encode(n_bits, lowerlimit, upperlimit) -> list:
  step = (upperlimit - lowerlimit)/(2**n_bits - 1)
  cypher1 = np.arange(lowerlimit, upperlimit+step, step)
  return cypher1

# recupera o respectivo valor do indivíduo
def decode(individual) -> float:
  return cypher[int(''.join([str(i) for i in individual]),2)]

  # função objetivo (f(x) = -x² + 16)
def goal_function(x):
  return abs(-x**2 + 16)

# calcula fitness de cada indíviduo
def measure_fitness(population) -> dict:
  fitness = {}
  for i in range(n_individuals):
    fitness[i] = goal_function(decode(population[i]))
  return fitness

def selection(selection_method: "weighted_roulette or fittest_half", population, elitism_method=None) -> "list, dict":
  return selection_method(population)

# separa os selecionados e seus respectivos valores de fitness
def parent_finder(population, selected, fitness):
  parents = []
  parents_fitness = {}
  j = 0
  for i in selected:
    parents.append(population[i])
    parents_fitness[j] = fitness[i]
    j += 1
  return parents, parents_fitness

# roleta com pesos
def weighted_roulette(population):
  fitness = measure_fitness(population)
  total_fitness = sum(fitness.values())
  cummulative_sum = []
  cummulative_sum.append(0)

  for i in range(n_individuals):
    weight = fitness[i]/total_fitness
    cummulative_sum[i] += weight
    if i == n_individuals - 1:
      pass
    else:
      cummulative_sum.append(cummulative_sum[i])
  
  tries = 0
  selected = []
  # gira a roleta
  while tries < half_n:
    roulette = random.uniform(0, 1)
    aux = list(cummulative_sum.copy())
    aux.append(roulette)
    aux = sorted(aux)
    if aux.index(roulette) >= n_individuals:
        continue
    else:
        selected.append(aux.index(roulette))
        tries += 1

  return parent_finder(population, selected, fitness)

# mais adequado
def fittest_half(population):
  fitness = measure_fitness(population)
  sorting = {}

  # prepara um dicionario para recuperar valores de fitness
  for i in range(n_individuals):
    sorting[fitness[i]] = i

  # ordena fitness por ordem decrescente
  aux = sorted(fitness.values(),reverse=True)
  selected = []

  # seleciona e retorna os n//2 maiores
  for i in range(half_n):
    selected.append(sorting[aux[i]])

  return parent_finder(population, selected, fitness)

# seleção aleatória
# def random_selection(population):

# torneio
# def tournament(population):

def pair(pairing_method, parents, parents_fitness) -> list:
  return pairing_method(parents, parents_fitness)

# mais adaptados
def fittest_pairing(parents, parents_fitness):
  sorting = {}

  # prepara um dicionario para recuperar valores de fitness
  for i in range(half_n):
    sorting[parents_fitness[i]] = i

  # ordena fitness por ordem decrescente
  aux = sorted(parents_fitness.values(),reverse=True)

  aux1 = []
  for i in range(0, half_n, 2):
    if i + 1 == half_n:
      aux2 = [population[sorting[aux[i]]]]
      aux1.append(aux2)
    else:
      aux2 = [population[sorting[aux[i]]], population[sorting[aux[i+1]]]]
      aux1.append(aux2)

  return aux1    

# pareamento aleatório
# def random_pairing(parents, fitness):

# aleatório com pesos
# def weighted_random_pairing(parents, fitness):

def mating(pairing_method: "fittest_pairing, random_pairing or weighted_random_pairing", mating_prob, parents, parents_fitness, secondpoint=None, firstpoint=1) -> list:
  pairs = pairing_method(parents, parents_fitness)
  aux1 = []
  if secondpoint == None:
      secondpoint = n_bits-1
  for i in pairs:
    if len(i) < 2:
      aux1.append(i[0])
      continue
    chance = random.random()
    if chance > mating_prob:
      aux1.append(i[0])
      aux1.append(i[1])
    else:
      for j in range(firstpoint, secondpoint+1):
        aux = i[0][j]
        i[0][j] = i[1][j]
        i[1][j] = aux
      x1 = i[0].copy()
      aux1.append(x1)
      x2 = i[1].copy()
      aux1.append(x2)
  
  return aux1

def mutation(mutation_method: "gauss_mutation, single_point_reset", offspring, mutation_prob, mutation_point, reset_type='random') -> list:
  return mutation_method(offspring, mutation_prob, mutation_point, reset_type)

# def gauss_mutation(offspring, reset_type):

def single_point_reset(offspring, mutation_prob, mutation_point, reset_type):
  if mutation_point == None:
    round(random.random()*(n_bits-1))

  aux = []
  for i in offspring:
    chance = random.random()
    if chance > mutation_prob:
      aux.append(i)
      continue
    else:    
      if reset_type == 'inversion':
        i[mutation_point] ^= 1
      else:
        i[mutation_point] = round(random.random())
  return offspring

n_bits = 4
upperlimit = 3.5
lowerlimit = -4
n_individuals = 4
selection_method = weighted_roulette

pairing_method = fittest_pairing
mating_prob = 0.8
mating_point_a = 1 # default = 0
mating_point_b = 2 # default = n_bits-1

mutation_method = single_point_reset
mutation_prob = 0.15
reset_type = 'inversion'
mutation_point = 2 # default = None

half_n = n_individuals//2

# gera codificação
cypher = encode(n_bits, lowerlimit, upperlimit)

generation_count = 1
while generation_count < 1000:
  # gera população
  if generation_count == 1:
    population = let_there_be_life(n_individuals, n_bits)
  else:
    population = let_there_be_life(half_n, n_bits)
    population.extend(offspring)

  # while
  # seleciona os pais da próxima geração
  parents, parents_fitness = selection(selection_method, population)

  # parea e cruza os pais
  offspring = mating(fittest_pairing, mating_prob, parents, parents_fitness, mating_point_b, mating_point_a)

  # testa mutação
  offspring = mutation(single_point_reset, offspring, mutation_prob, mutation_point, reset_type)

  generation_count += 1

print(population)