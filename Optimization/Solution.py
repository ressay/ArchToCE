import random
import timeit

from shapely.ops import cascaded_union

from Optimization.Genetic.Evaluator import calculateFitnessSolution
from Skeleton.LevelSkeleton import LevelSkeleton


class Solution(object):

    maxDisBetweenVoiles = 8

    def __init__(self,levelSkeleton):
        super(Solution, self).__init__()
        self.levelSkeleton = levelSkeleton
        self.fitness = None
        self.validPoints = None
        self.nonValidPoints = None
        self.validShapelyCircles = None
        self.areaCovered = None

    def getFitness(self):
        if self.fitness is None:
            self.fitness = calculateFitnessSolution(self)
        return self.fitness

    def reInitFitness(self):
        self.fitness = None
        self.validPoints = None
        self.nonValidPoints = None
        self.areaCovered = None

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

    def getValidVoilesPoints(self):
        if not self.validPoints:

            allVoiles = [voile for wallSkeleton in self.levelSkeleton.wallSkeletons
                         for voile in wallSkeleton.attachedVoiles]

            for cpt,voileSkeleton in enumerate(allVoiles):
                for i in range(cpt+1,len(allVoiles)):

                    for cpt1,p1 in enumerate(voileSkeleton.getPointsList()):
                        # if not voileSkeleton.isPointValid[cpt1]:
                        for cpt2, p2 in enumerate(allVoiles[i].getPointsList()):
                            vec = p1 - p2
                            if vec.magn() < Solution.maxDisBetweenVoiles:
                                voileSkeleton.setPointValid(cpt1)
                                allVoiles[i].setPointValid(cpt2)
            self.validPoints = [pnt for vs in allVoiles
                                for index, pnt in enumerate(vs.getPointsList())
                                if vs.isPointValid[index]]
            self.validShapelyCircles = [pnt.pnt.buffer(Solution.maxDisBetweenVoiles/2) for pnt in self.validPoints]

        return self.validPoints

    def getValidVoilesShapelyPoints(self):
        if not self.validPoints:
            self.getValidVoilesPoints()
        return self.validShapelyCircles

    def getAreaCovered(self):
        if not self.areaCovered:
            pntsArray = self.getValidVoilesShapelyPoints()
            a = cascaded_union(pntsArray)
            self.areaCovered = a.area
        return self.areaCovered

    def getNonValidVoilesPoints(self):
        if not self.nonValidPoints:
            validPoints = self.getValidVoilesPoints()
            allVoiles = [voile for wallSkeleton in self.levelSkeleton.wallSkeletons
                         for voile in wallSkeleton.attachedVoiles]
            self.nonValidPoints = [pnt for voileSkeleton in allVoiles
                                for index, pnt in enumerate(voileSkeleton.getPointsList())
                                if not voileSkeleton.isPointValid[index]]

        return self.nonValidPoints


