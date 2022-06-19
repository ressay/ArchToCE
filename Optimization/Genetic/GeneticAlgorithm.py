import random
import timeit
from Optimization.Genetic import GeneticOperations2
from Optimization.Genetic.Evaluator import calculateFitnessPopulation
from Optimization.Genetic.GeneticOperations2 import mutate
from Optimization.Solution import Solution


def generatePopulation(levelSkeleton,popSize, ratio):
    solutions = []
    while len(solutions)< popSize:
        ReserveWallS = []
        for wallskeleton in levelSkeleton.wallSkeletons:
            if wallskeleton.iscolumnParent:
                ReserveWallS.append(wallskeleton)
        for wallskeleton in ReserveWallS: levelSkeleton.wallSkeletons.remove(wallskeleton)

        Ssolution=Solution.createRandomSolutionFromSkeleton2(levelSkeleton, ratio)
        for wallskeleton in ReserveWallS:
            levelSkeleton.wallSkeletons.append(wallskeleton)
            Ssolution.levelSkeleton.wallSkeletons.append(wallskeleton)
        # if Ssolution.levelSkeleton.ScoreOfUnacceptableVoiles()[0]>0.99:
        solutions.append(Ssolution)
    return solutions

def selection(population,probability,fitnesses):
    selected = []
    popSize = len(population)
    indexes = list(range(popSize))
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

def search(levelSkeleton,popSize=50,crossRate=0.5,mutRate=0.65,maxIterations=1
           ,geneticOps=GeneticOperations2,filename='default', constraints=None, Comb = [0,0,0,0]):
    start1 = timeit.default_timer()
    print('Generating the population..')
    population = generatePopulation(levelSkeleton, popSize, constraints['ratio'])
    # print('The population size', len(population))
    # tracker = SummaryTracker()
    scoreDist = 0
    maxIterations = 50
    i=0
    # for i in range(maxIterations):

    while i<50 :
        # tracker.print_diff()
        # print(("len population: " + str(len(population))))
        # print(("iteration: " + str(i)))
        start = timeit.default_timer()
        fitnesses = calculateFitnessPopulation(population,constraints)
        stop = timeit.default_timer()
        # print(("time it took fitness: " + str(stop - start)))

        # for fit in fitnesses:
        #     print "fitness is " + str(fit)

        best = max(fitnesses)
        newComers = []
        bestis=[]
        condition = False
        print(("best is : " + str(best)))
        bestis.append(best)
        # while not condition:
            # start = timeit.default_timer()
        selected = selection(population,crossRate/2,fitnesses)
            # print('here selected', len(selected))
            # stop = timeit.default_timer()
            # print(("time it took selection: " + str(stop - start)))
            # start = timeit.default_timer()

        for s1, s2 in selected:
            s3,s4 = geneticOps.cross(s1,s2)
            # a = s3.levelSkeleton.ScoreOfUnacceptableVoiles()[0]
            # b = s4.levelSkeleton.ScoreOfUnacceptableVoiles()[0]
            # # print('passed')
            # if a > 0.99 and b > 0.99:
            newComers.append(s3)
            newComers.append(s4)

        # print('new comers', len(newComers))


        stop = timeit.default_timer()
        # print(("time it took cross: " + str(stop - start)))
        start = timeit.default_timer()
        for s in mutationSelection(mutRate,newComers):
            # print "mutating!!"
            s=mutate(s)
            # print('YESS HERE', s.levelSkeleton.ScoreOfUnacceptableVoiles()[0])
        population.extend(newComers)
        print('after extending:', len(population))
        stop = timeit.default_timer()
        # print(("time it took mutation: " + str(stop - start)))


        start = timeit.default_timer()
        fits = calculateFitnessPopulation(population, constraints, Comb)
        stop = timeit.default_timer()
        print(("time it took fitness2: " + str(stop - start)))
        start = timeit.default_timer()
        for k in range(len(selected)*2):
            index = min(list(range(len(fits))), key=lambda a: fits[a])
            del population[index]
            del fits[index]

        stop = timeit.default_timer()
        print(("time it took delete: " + str(stop - start)))

        bestIndex = max(list(range(len(fits))), key=lambda a: fits[a])
        sol = population[bestIndex]
        scoreDist = sol.levelSkeleton.ScoreOfUnacceptableVoiles()[0]
        s = sol.getFitness()
        tscore = s['totalScore']
        # fitness = sol.getFitness()
        # eccScore = fitness['sym']
        i= i+1
        if i>=50 and scoreDist >0.799:
            condition = True
        print("here condition scoredist",scoreDist)
        print('number of iterations',i)
    fitnesses = calculateFitnessPopulation(population, constraints)
    bestIndex = max(list(range(len(fitnesses))), key=lambda a: fitnesses[a])
    stop = timeit.default_timer()
    print(("time it took: " + str(stop - start1)))
    solution = population[bestIndex]
    fitness = solution.getFitness()
    print(("scores:\nRadius score in x: " + str(fitness['radX']) + " in y: " + str(fitness['radY'])))
    print(("length score in x: " + str(fitness['lengthShearX']) + " in y: " + str(fitness['lengthShearY'])))
    print('')
    print(("needed: " + str(solution.levelSkeleton.getVoileLengthNeeded(constraints['ratio']))))
    f = open(filename,'w')
    f.write("in x: " + str(fitness['lengthX']) + " in y: " + str(fitness['lengthY']))
    f.write("needed: " + str(solution.levelSkeleton.getVoileLengthNeeded(constraints['ratio'])))
    f.write("covered area: " + str(solution.getAreaCoveredBoxes(constraints['d'])))
    f.write("overlapped area: " + str(solution.getOverlappedArea(constraints['d'])))
    f.close()

    levelSkeleton = solution.levelSkeleton
    for wallSkeleton in levelSkeleton.wallSkeletons:
        if not wallSkeleton.iscolumnParent:
            for voileSkeleton in wallSkeleton.getAllVoiles():
                if voileSkeleton.end - voileSkeleton.start > wallSkeleton.vecLength.magn():
                    print(("problem: voile is ", voileSkeleton.end - voileSkeleton.start, wallSkeleton.vecLength.magn()))
    ReserveWallS = []
    for wallskeleton in solution.levelSkeleton.wallSkeletons:
        if wallskeleton.iscolumnParent:
            ReserveWallS.append(wallskeleton)
    print("yo here number of columns", len(ReserveWallS))

    return solution


