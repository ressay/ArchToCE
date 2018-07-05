import random
import timeit

from Optimization.Genetic import GeneticOperations2
from Optimization.Genetic.Evaluator import calculateFitnessPopulation
from Optimization.Solution import Solution


def generatePopulation(levelSkeleton,popSize):
    # ratio = levelSkeleton.getRatio()
    # print "ratio is " + str(ratio)
    solutions = []
    for i in range(popSize):
        solutions.append(Solution.createRandomSolutionFromSkeleton2(levelSkeleton))
    return solutions

# def selection(population,probability):
#     popSize = len(population)
#     indexes = range(popSize)
#     size = popSize*probability
#     selected = []
#     for i in range(size):
#         select = indexes[int(random.uniform(0,popSize-0.1))]
#         indexes.remove(select)
#         popSize -= 1
#
#     return selected

def selection(population,probability,fitnesses):
    selected = []
    # i1 = max(range(len(fitnesses)), key=lambda a: fitnesses[a])
    # i2 = max([i for i in range(len(fitnesses)) if i != i1], key=lambda a: fitnesses[a])
    popSize = len(population)
    indexes = range(popSize)
    size = int(probability*popSize)
    for i in range(size):
        i1 = int(random.uniform(0, len(indexes) - 0.1))
        ind = indexes[i1]
        del indexes[i1]
        i2 = int(random.uniform(0, len(indexes) - 0.1))
        ind2 = indexes[i2]
        del indexes[i2]
        selected.append((population[ind],population[ind2]))
    return selected

def search(levelSkeleton,popSize=300,crossRate=0.1,mutRate=0.2,maxIterations=1000
           ,geneticOps=GeneticOperations2):
    start = timeit.default_timer()
    population = generatePopulation(levelSkeleton,popSize)

    for i in range(maxIterations):
        print ("iteration: " + str(i))
        fitnesses = calculateFitnessPopulation(population)
        # for fit in fitnesses:
        #     print "fitness is " + str(fit)
        # best = max(fitnesses)
        # print ("best is : " + str(best))
        selected = selection(population,crossRate/2,fitnesses)
        for s1,s2 in selected:
            s3,s4 = geneticOps.cross(s1,s2)
            # print "fitnesses are : " +str(s3.getFitness()) + " " + str(s4.getFitness())
            population.append(s3)
            population.append(s4)


        fits = calculateFitnessPopulation(population)

        for k in range(len(selected)*2):
            index = min(range(len(fits)), key=lambda a: fits[a])
            del population[index]
            del fits[index]


    fitnesses = calculateFitnessPopulation(population)
    bestIndex = max(range(len(fitnesses)), key=lambda a: fitnesses[a])
    stop = timeit.default_timer()

    print ("time it took: " + str(stop - start))
    return population[bestIndex]


