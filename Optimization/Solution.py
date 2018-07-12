import random
import timeit

from Optimization.Genetic.Evaluator import calculateFitnessSolution
from Skeleton.LevelSkeleton import LevelSkeleton


class Solution(object):
    def __init__(self,levelSkeleton):
        super(Solution, self).__init__()
        self.levelSkeleton = levelSkeleton
        self.fitness = None

    def getFitness(self):
        if self.fitness is None:
            self.fitness = calculateFitnessSolution(self)
        return self.fitness

    def reInitFitness(self):
        self.fitness = None

    @staticmethod
    def createRandomSolutionFromSkeleton(levelSkeleton):
        ratio = levelSkeleton.getRatio()
        for wallSkeleton in levelSkeleton.wallSkeletons:
            wallSkeleton.attachVoile(wallSkeleton.createRandomVoileFromRatio(ratio))
        return Solution(levelSkeleton)


    @staticmethod
    def createRandomSolutionFromSkeleton2(levelS):
        # s = timeit.default_timer()
        walls = [wallSkeleton.copyWithoutVoiles() for wallSkeleton in levelS.wallSkeletons]
        # e = timeit.default_timer()
        # print ("time it took copy1: " + str(e - s))
        levelSkeleton = LevelSkeleton(walls,levelS.slabSkeleton.copy(),levelS.level)


        totalLength = levelSkeleton.getWallsTotalLength()
        needed = levelSkeleton.getVoileLengthNeeded()
        # print("needed : " + str(needed) + " total length: " + str(totalLength))
        size = len(levelSkeleton.wallSkeletons)
        indexes = range(size)
        # s1 = timeit.default_timer()
        while len(indexes) > 0 and needed > 0:
            ind = int(random.uniform(0,len(indexes)-0.1))
            rand = indexes[ind]
            del indexes[ind]
            wallSkeleton = levelSkeleton.wallSkeletons[rand]
            # s = timeit.default_timer()
            length, voiles = wallSkeleton.createRandomVoilesFromLengthNeeded(totalLength, needed)
            # e = timeit.default_timer()
            # print ("time it took create voiles: " + str(e - s))
            wallSkeleton.attachVoiles(voiles)
            needed -= length
            totalLength -= wallSkeleton.vecLength.magn()

        # print("total length left: " + str(totalLength) + " needed left: " + str(needed))
        # e1 = timeit.default_timer()
        # print ("time it took loop: " + str(e1 - s1))
        return Solution(levelSkeleton)


