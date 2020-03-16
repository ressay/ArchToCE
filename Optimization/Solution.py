import random
import timeit

from shapely.ops import cascaded_union

from Optimization.Genetic.Evaluator import calculateFitnessSolution
from Skeleton.LevelSkeleton import LevelSkeleton


class Solution(object):

    maxDisBetweenVoiles = 8

    def __init__(self,levelSkeleton):
        super(Solution, self).__init__()
        self.areaCoveredBoxes = None
        self.levelSkeleton = levelSkeleton
        self.fitness = None
        self.validPoints = None
        self.nonValidPoints = None
        self.validShapelyCircles = None
        self.areaCovered = None
        self.validBoxes = None
        self.nonValidBoxes = None
        self.areaCoveredBoxes2 = None
        self.validBoxes2 = None
        self.nonValidBoxes2 = None

    def getFitness(self, constraints=None):
        if self.fitness is None:
            self.fitness = calculateFitnessSolution(self,constraints)
        return self.fitness

    def reInitFitness(self):
        self.fitness = None
        self.validPoints = None
        self.nonValidPoints = None
        self.areaCovered = None
        self.validBoxes = None
        self.nonValidBoxes = None
        self.areaCoveredBoxes = None
        self.areaCoveredBoxes2 = None
        self.validBoxes2 = None
        self.nonValidBoxes2 = None

    @staticmethod
    def createRandomSolutionFromSkeleton(levelSkeleton, ratio):
        ratio = levelSkeleton.getRatio(ratio)
        for wallSkeleton in levelSkeleton.wallSkeletons:
            wallSkeleton.attachVoile(wallSkeleton.createRandomVoileFromRatio(ratio))
        return Solution(levelSkeleton)


    @staticmethod
    def createRandomSolutionFromSkeleton2(levelS, ratio):
        # s = timeit.default_timer()
        walls = [wallSkeleton.copyWithoutVoiles() for wallSkeleton in levelS.wallSkeletons]
        # e = timeit.default_timer()
        # print ("time it took copy1: " + str(e - s))
        levelSkeleton = LevelSkeleton(walls,levelS.slabSkeleton.copy(),levelS.level)

        voilesfixedLength = levelSkeleton.getVoilesTotalLength()
        totalLength = levelSkeleton.getWallsTotalLength() - voilesfixedLength
        needed = levelSkeleton.getVoileLengthNeeded(ratio)*2 - voilesfixedLength
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
            totalLength -= (wallSkeleton.vecLength.magn() - wallSkeleton.getVoilesLength())
            wallSkeleton.attachVoiles(voiles)
            needed -= length


        # print("total length left: " + str(totalLength) + " needed left: " + str(needed))
        # e1 = timeit.default_timer()
        # print ("time it took loop: " + str(e1 - s1))
        return Solution(levelSkeleton)

    def getValidVoilesPoints(self):
        if not self.validPoints:

            allVoiles = [voile for wallSkeleton in self.levelSkeleton.wallSkeletons
                         for voile in wallSkeleton.getAllVoiles()]

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
                         for voile in wallSkeleton.getAllVoiles()]
            self.nonValidPoints = [pnt for voileSkeleton in allVoiles
                                for index, pnt in enumerate(voileSkeleton.getPointsList())
                                if not voileSkeleton.isPointValid[index]]

        return self.nonValidPoints

    def getValidVoilesBoxes(self, ratio):
        if not self.validBoxes:
            allVoiles = [voile for wallSkeleton in self.levelSkeleton.wallSkeletons
                         for voile in wallSkeleton.getAllVoiles()]
            acceptedBoxes = []
            done = [False for v in allVoiles]
            for cpt,voil in enumerate(allVoiles):
                box1 = voil.getSurrondingBox(ratio)
                for i in range(cpt+1,len(allVoiles)):
                    if not done[i] or not done[cpt]:
                        box2 = allVoiles[i].getSurrondingBox(ratio)
                        if box1.intersects(box2):
                            if not done[cpt]:
                                acceptedBoxes.append(box1)
                                done[cpt] = True
                            if not done[i]:
                                acceptedBoxes.append(box2)
                                done[i] = True
            self.validBoxes = acceptedBoxes
            self.nonValidBoxes = [voil.getSurrondingBox(ratio) for i,voil in enumerate(allVoiles)
                                                            if not done[i]]
        return self.validBoxes

    def getValidVoilesBoxesBis(self):

        def boxesOr(a,b):
            return [(x or y) for (x,y) in zip(a,b)]

        def intersect(boxes1,boxes2):
            result1 = [0,0,0,0]
            result2 = [0,0,0,0]
            for i,box in enumerate(boxes1):
                for j,box2 in enumerate(boxes2):
                    if box.intersects(box2):
                        result1[i] = 1
                        result2[j] = 1
            return result1,result2

        if not self.validBoxes2:
            allVoiles = [voile for wallSkeleton in self.levelSkeleton.wallSkeletons
                         for voile in wallSkeleton.getAllVoiles()]
            done = [[0,0,0,0] for v in allVoiles]
            for cpt,voil in enumerate(allVoiles):
                boxes1 = voil.getSurrondingBoxes()
                for i in range(cpt+1,len(allVoiles)):
                    boxes2 = allVoiles[i].getSurrondingBoxes()
                    r1,r2 = intersect(boxes1,boxes2)
                    done[cpt] = boxesOr(done[cpt],r1)
                    done[i] = boxesOr(done[i],r2)


            self.validBoxes2 = [box for i,voil in enumerate(allVoiles)
                                for box in voil.getSurrondingBoxes(done[i])]
            self.nonValidBoxes2 = []
        return self.validBoxes2
    
    def getAreaCoveredBoxesBis(self):
        if not self.areaCoveredBoxes2:
            pntsArray = self.getValidVoilesBoxesBis()
            a = cascaded_union(pntsArray)
            a = a.intersection(self.levelSkeleton.slabSkeleton.poly.poly)
            self.areaCoveredBoxes2 = a.area
        return self.areaCoveredBoxes2

    def getNonValidVoilesBoxesBis(self):
        if not self.nonValidBoxes2:
            self.getValidVoilesBoxesBis()
        return self.nonValidBoxes2

    def getAreaCoveredBoxes(self, d_ratio):
        if not self.areaCoveredBoxes:
            pntsArray = self.getValidVoilesBoxes(d_ratio)
            a = cascaded_union(pntsArray)
            # a = a.intersection(self.levelSkeleton.slabSkeleton.poly.poly)
            self.areaCoveredBoxes = a.area
        return self.areaCoveredBoxes

    def getOverlappedArea(self, d_ratio):
        coveredArea = self.getAreaCoveredBoxes(d_ratio)
        levelSkeleton = self.levelSkeleton
        area = sum(voileSkeleton.getSurrondingBox(d_ratio).area for wallSkeleton in levelSkeleton.wallSkeletons
                   for voileSkeleton in wallSkeleton.getAllVoiles())
        return area - coveredArea

    def getNonValidVoilesBoxes(self, d_ratio):
        if not self.nonValidBoxes:
            self.getValidVoilesBoxes(d_ratio)
        return self.nonValidBoxes


