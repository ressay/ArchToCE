import math

from Geometry.Geom2D import Pnt

def distance(p1,p2):
    p = p1 - p2
    return p.magn()


class EvaluationData(object):
    def __init__(self,dis, size, length):
        super(EvaluationData, self).__init__()
        self.dis = dis
        self.size = size
        self.length = length
        self.sumLiX = 0
        self.sumLiY = 0
        self.sumLixi = 0
        self.sumLiyi = 0

class WallEvaluator(object):
    def __init__(self,levelSkeleton):
        super(WallEvaluator, self).__init__()
        center = levelSkeleton.slabSkeleton.poly.centroid()
        self.center = Pnt(center.x, center.y)

    def calculateFitnessWall(self,wallSkeleton):
        if wallSkeleton.evalData:
            return wallSkeleton.evalData
        size = 0
        dis = 0
        length = 0

        for voileSkeleton in wallSkeleton.attachedVoiles:
            # for voileSkeleton in voiles:
            # print ("looping")
            centerV = voileSkeleton.poly.centroid()
            centerV = Pnt(centerV.x, centerV.y)
            dis += distance(centerV, self.center)
            length += (voileSkeleton.end - voileSkeleton.start)
            size += 1
        wallSkeleton.evalData = EvaluationData(dis, size, length)
        sumLi1,sumLi2,sumLixi,sumLiyi = wallSkeleton.getSums()
        wallSkeleton.evalData.sumLiX = sumLi1
        wallSkeleton.evalData.sumLiY = sumLi2
        wallSkeleton.evalData.sumLixi = sumLixi
        wallSkeleton.evalData.sumLiyi = sumLiyi
        return wallSkeleton.evalData

def calculateFitnessSolution(solution):
    levelSkeleton = solution.levelSkeleton
    wallEvaluator = WallEvaluator(levelSkeleton)
    # print ("before looping")
    # voiles = [voile for wallSkeleton in levelSkeleton.wallSkeletons
    #                       for voile in wallSkeleton.attachedVoiles]
    size = 0
    dis = 0
    length = 0
    sumLiX = 0
    sumLiY = 0
    sumLixi = 0
    sumLiyi = 0
    for wallSkeleton in levelSkeleton.wallSkeletons:
        # print "attached voiles : " + str(len(wallSkeleton.attachedVoiles))
        evalData = wallEvaluator.calculateFitnessWall(wallSkeleton)
        d,s,l = evalData.dis,evalData.size,evalData.length
        dis += d
        size += s
        length += l

    cntr = levelSkeleton.getCenterFromShear()
    centerV = levelSkeleton.slabSkeleton.poly.centroid()
    centerV = Pnt(centerV.x, centerV.y)
    fitness = -distance(cntr,centerV)
    return fitness


def calculateFitnessPopulation(population):
    fitnesses = []
    for solution in population:
        # print("calculating:")
        fitnesses.append(solution.getFitness())

    return fitnesses