import math
import timeit

from shapely.ops import cascaded_union

from Geometry.Geom2D import Pnt

def distance(p1,p2):
    p = p1 - p2
    return p.magn()


class EvaluationData(object):
    def __init__(self,dis, size, totalLengthX, totalLengthY, lengthX, lengthY):
        super(EvaluationData, self).__init__()
        self.dis = dis
        self.size = size
        self.totalLengthX = totalLengthX
        self.totalLengthY = totalLengthY
        self.lengthX = lengthX
        self.lengthY = lengthY
        self.sumLiX = 0
        self.sumLiY = 0
        self.sumLixi = 0
        self.sumLiyi = 0
        self.vecUni = 0

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
        totalLengthX = abs(wallSkeleton.vecLength.x())
        totalLengthY = abs(wallSkeleton.vecLength.y())
        lengthX = 0
        lengthY = 0
        vec = Pnt(0,0)
        for voileSkeleton in wallSkeleton.getAllVoiles():
            # for voileSkeleton in voiles:
            # print ("looping")
            centerV = voileSkeleton.poly.centroid()
            centerV = Pnt(centerV.x, centerV.y)
            v = centerV - self.center
            vec += v*voileSkeleton.getLength()
            dis += distance(centerV, self.center)
            lengthX += voileSkeleton.getLengthX()
            lengthY += voileSkeleton.getLengthY()
            # length += (voileSkeleton.end - voileSkeleton.start)
            size += 1
        wallSkeleton.evalData = EvaluationData(dis, size, totalLengthX,totalLengthY,lengthX,lengthY)
        sumLi1,sumLi2,sumLixi,sumLiyi = wallSkeleton.getSums()
        wallSkeleton.evalData.sumLiX = sumLi1
        wallSkeleton.evalData.sumLiY = sumLi2
        wallSkeleton.evalData.sumLixi = sumLixi
        wallSkeleton.evalData.sumLiyi = sumLiyi
        wallSkeleton.evalData.vecUni = vec
        return wallSkeleton.evalData



def calculateFitnessSolution(solution, constraints=None):
    levelSkeleton = solution.levelSkeleton
    wallEvaluator = WallEvaluator(levelSkeleton)

    if constraints is not None:
        rad_w, ecc_w, area_w, length_w = constraints['rad_w'], constraints['ecc_w'],\
                                         constraints['area_w'], constraints['length_w']
    else:
        rad_w, ecc_w, area_w, length_w = 0.5, -0.5, 1, 1
    size = 0
    dis = 0
    totalX = 0
    totalY = 0
    lengthX = 0
    lengthY = 0
    needed = levelSkeleton.getVoileLengthNeeded(constraints['ratio'])
    # here
    centerV = levelSkeleton.slabSkeleton.poly.centroid()
    centerV = Pnt(centerV.x, centerV.y)
    vecUni = Pnt(0,0)
    for wallSkeleton in levelSkeleton.wallSkeletons:
        # print "attached voiles : " + str(len(wallSkeleton.attachedVoiles))
        evalData = wallEvaluator.calculateFitnessWall(wallSkeleton)
        d,s,lx,ly = evalData.dis,evalData.size,evalData.totalLengthX,evalData.totalLengthY
        dis += d
        size += s
        totalX += lx
        totalY += ly
        lengthX += evalData.lengthX
        lengthY += evalData.lengthY
        vecUni += evalData.vecUni
    cntr = levelSkeleton.getCenterFromShear()
    Rx, Ry = levelSkeleton.getTorsionalRadius(centerV)
    momentx, momenty = levelSkeleton.slabSkeleton.poly.momentX(), levelSkeleton.slabSkeleton.poly.momentY()
    if momentx < 0 or momenty < 0:
        print((momentx, momenty))
        eval(input())
    radiuses = (Rx + Ry)/(abs(Rx-Ry)+0.000001) #abs(1-(Ry/(momentx+momenty))) + abs(1-(Rx/(momentx+momenty)))

    area = solution.getAreaCoveredBoxes(constraints['d'])
    coeffs = {
        'rad': rad_w,
        'sym': ecc_w,
        'lengthShearX': length_w/2.,
        'lengthShearY': length_w/2.,
        # 'overlapped': -1,
        # 'unif': 0,
        'area': area_w
    }

    def getScoreLength(lengthA,total):
        if lengthA < needed:
            scoreLengthA = math.pow(lengthA/needed,3)
        else:
            scoreLengthA = 1 - (lengthA - needed)/needed
        return scoreLengthA

    scoreLengthX = getScoreLength(lengthX,totalX)
    scoreLengthY = getScoreLength(lengthY,totalY)
    areaNorm = sum(voileSkeleton.getSurrondingBox(constraints['d']).area for wallSkeleton in levelSkeleton.wallSkeletons
               for voileSkeleton in wallSkeleton.getAllVoiles())
    if areaNorm == 0:
        areaNorm = -1
        ar = -1
    else:
        ar = math.sqrt(areaNorm)
    fitV = {
        'radX': Rx,
        'radY': Ry,
        'rad': radiuses,
        'sym': max([0,distance(cntr,centerV)/ar]),
        'lengthShearX': scoreLengthX,
        'lengthShearY': scoreLengthY,
        'unif': vecUni.magn(),
        'area': area/levelSkeleton.getSlabArea(),
        'overlapped': max([0,solution.getOverlappedArea(constraints['d'])/areaNorm]),
        'lengthX': lengthX,
        'lengthY': lengthY
        }
    fitness = 0
    for key in coeffs:
        fitness += fitV[key]*coeffs[key]
    fitV['totalScore'] = fitness
    # fitness = fitV['area']
    return fitV


def calculateFitnessPopulation(population, constraints=None):
    fitnesses = []
    for solution in population:
        # print("calculating:")
        fitnesses.append(solution.getFitness(constraints)['totalScore'])

    return fitnesses