import random
import timeit

from Optimization.Genetic import GeneticOperations2
from Optimization.Genetic.Evaluator import calculateFitnessPopulation
from Optimization.Genetic.GeneticOperations2 import mutate
from Optimization.Solution import Solution
from pympler.tracker import SummaryTracker


def generatePopulation(levelSkeleton,popSize):
    solutions = []
    for i in range(popSize):
        solutions.append(Solution.createRandomSolutionFromSkeleton2(levelSkeleton))
    return solutions


def selection(population,probability,fitnesses):
    selected = []
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

def mutationSelection(mutationRate,population):
    for p in population:
        if random.uniform(0,1) < mutationRate:
            yield p

def search(levelSkeleton,popSize=30,crossRate=0.3,mutRate=0.5,maxIterations=70
           ,geneticOps=GeneticOperations2):
    start = timeit.default_timer()
    population = generatePopulation(levelSkeleton,popSize)
    # tracker = SummaryTracker()

    for i in range(maxIterations):
        # tracker.print_diff()
        print("len population: " + str(len(population)))
        print ("iteration: " + str(i))
        start = timeit.default_timer()
        fitnesses = calculateFitnessPopulation(population)
        stop = timeit.default_timer()
        print ("time it took fitness: " + str(stop - start))

        # for fit in fitnesses:
        #     print "fitness is " + str(fit)
        start = timeit.default_timer()
        best = max(fitnesses)
        print ("best is : " + str(best))
        selected = selection(population,crossRate/2,fitnesses)
        stop = timeit.default_timer()
        print ("time it took selection: " + str(stop - start))
        start = timeit.default_timer()
        newComers = []
        for s1,s2 in selected:
            s3,s4 = geneticOps.cross(s1,s2)
            # print "fitnesses are : " +str(s3.getFitness()) + " " + str(s4.getFitness())
            newComers.append(s3)
            newComers.append(s4)

        stop = timeit.default_timer()
        print ("time it took cross: " + str(stop - start))
        start = timeit.default_timer()
        for s in mutationSelection(mutRate,newComers):
            # print "mutating!!"
            mutate(s)
        population.extend(newComers)
        stop = timeit.default_timer()
        print ("time it took mutation: " + str(stop - start))

        start = timeit.default_timer()
        fits = calculateFitnessPopulation(population)
        stop = timeit.default_timer()
        print ("time it took fitness2: " + str(stop - start))
        start = timeit.default_timer()
        for k in range(len(selected)*2):
            index = min(range(len(fits)), key=lambda a: fits[a])
            del population[index]
            del fits[index]

        stop = timeit.default_timer()
        print ("time it took delete: " + str(stop - start))


    fitnesses = calculateFitnessPopulation(population)
    bestIndex = max(range(len(fitnesses)), key=lambda a: fitnesses[a])
    stop = timeit.default_timer()
    print ("time it took: " + str(stop - start))
    solution = population[bestIndex]
    fitness = solution.getFitness()
    print ("in x: " + str(fitness['lengthX']) + " in y: " + str(fitness['lengthY']))
    print ("score in x: " + str(fitness['lengthShearX']) + " in y: " + str(fitness['lengthShearY']))
    print ("needed: " + str(solution.levelSkeleton.getVoileLengthNeeded()))
    return solution


