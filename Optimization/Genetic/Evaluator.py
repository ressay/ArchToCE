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
            size += 1
        wallSkeleton.evalData = EvaluationData(dis, size, totalLengthX,totalLengthY,lengthX,lengthY)
        sumLi1,sumLi2,sumLixi,sumLiyi = wallSkeleton.getSums()
        wallSkeleton.evalData.sumLiX = sumLi1
        wallSkeleton.evalData.sumLiY = sumLi2
        wallSkeleton.evalData.sumLixi = sumLixi
        wallSkeleton.evalData.sumLiyi = sumLiyi
        wallSkeleton.evalData.vecUni = vec
        return wallSkeleton.evalData

def calculateFitnessSolution(solution, constraints=None, comb = [0,0,0,0]):
    # ReserveWallS = []
    # for wallskeleton in solution.levelSkeleton.wallSkeletons:
    #     if wallskeleton.iscolumnParent:
    #         ReserveWallS.append(wallskeleton)
    # for wallskeleton in ReserveWallS: solution.levelSkeleton.wallSkeletons.remove(wallskeleton)

    levelSkeleton = solution.levelSkeleton
    wallEvaluator = WallEvaluator(levelSkeleton)

    if constraints is not None:
        rad_w, ecc_w, area_w, length_w = constraints['rad_w'], constraints['ecc_w'],\
                                         constraints['area_w'], constraints['length_w']
    else:
        rad_w, ecc_w, area_w, length_w = 0, -0.5, 1, 1
    size = 0
    dis = 0
    totalX = 0
    totalY = 0
    lengthX = 0
    lengthY = 0
    needed = levelSkeleton.getVoileLengthNeeded(constraints['ratio'])

    centerV = levelSkeleton.slabSkeleton.poly.centroid()
    centerV = Pnt(centerV.x, centerV.y)
    vecUni = Pnt(0, 0)

    for wallSkeleton in levelSkeleton.wallSkeletons:
        # print "attached voiles : " + str(len(wallSkeleton.attachedVoiles))
        evalData = wallEvaluator.calculateFitnessWall(wallSkeleton)
        d, s, lx, ly = evalData.dis, evalData.size, evalData.totalLengthX, evalData.totalLengthY
        dis += d
        size += s
        totalX += lx
        totalY += ly
        if not wallSkeleton.iscolumnParent:
            lengthX += evalData.lengthX
            lengthY += evalData.lengthY
        vecUni += evalData.vecUni
    # print("columns direction length", toAddYneeded, toAddXneeded)
    # print("total here", lengthY, lengthX)
    cntr = levelSkeleton.getCenterFromShear()
    Rx, Ry = levelSkeleton.getTorsionalRadius(centerV)
    momentx, momenty = levelSkeleton.slabSkeleton.poly.momentX(), levelSkeleton.slabSkeleton.poly.momentY()
    if momentx < 0 or momenty < 0:
        print((momentx, momenty))
        eval(input())
    # radiuses = (Rx + Ry)/(abs(Rx-Ry)+0.000001) #abs(1-(Ry/(momentx+momenty))) + abs(1-(Rx/(momentx+momenty)))
    rx = math.sqrt(momentx/levelSkeleton.slabSkeleton.poly.area())   # Torsional radius
    ry = math.sqrt(momenty/levelSkeleton.slabSkeleton.poly.area())
    radiuses= (Rx/rx + Ry/ry)*0.5
    scoreDist = levelSkeleton.ScoreOfUnacceptableVoiles()[0]
    # scoreDist = 0
    a = solution.getOverlappedArea(constraints['d'])

    effectiveArea = solution.getEffectiveArea()
    overlappedArea = solution.geteffectiveOverlappedArea(effectiveArea)

    ex = abs(cntr.x() - centerV.x())
    ey = abs(cntr.y() - centerV.y())
    coeffs = {
        'rad': comb[2],
        'sym': comb[0],
        'lengthShearX': 0,
        'lengthShearY': 0,
        'overlapped': 0 ,
        # 'unif': 0,
        'area': comb[1],
        'distance': 0,
        'distribution': comb[3],
    }
    # print('this combination is', comb)
    def getScoreLength(lengthA,total):
        if lengthA > needed:
            scoreLengthA = math.pow(needed/lengthA,3)
        else:
            scoreLengthA = 1 - (needed - lengthA)/needed
        return scoreLengthA

    def getScoreArea(area, slabArea):
        if area:
            if  area > 0.2*slabArea:
                scoreArea = math.pow(0.02*slabArea/area,3)
            else:
                scoreArea = 1- (0.2*slabArea-area)/(0.2*slabArea)
            return  scoreArea
        else: return 0

    def getScoreOverlapped(overlapped, totalArea):
        if totalArea >= overlapped:
            return 1-overlapped/totalArea
        else: return 0

    def getScoreSymEcc(ex,ey,Rx,Ry):
        if Ry==0: Ry=0.1
        if Rx==0: Rx=0.1
        return 0.5*(2 - ex/(0.3*Rx) - ey/(0.3*Ry))

    def getDistrubtionScore(lx,ly,LX,LY):
        if ly and lx:
            if ly > lx:
                s1 = abs(lx/ly)
            else:
                s1 = abs(ly/lx)
        else:s1 = -1
        return s1

    LX = levelSkeleton.slabSkeleton.poly.MaxCoords().x()-levelSkeleton.slabSkeleton.poly.MinCoords().x()
    LY = levelSkeleton.slabSkeleton.poly.MaxCoords().y()-levelSkeleton.slabSkeleton.poly.MinCoords().y()
    scoreLengthX = getScoreLength(lengthX,totalX)
    scoreLengthY = getScoreLength(lengthY,totalY)
    scoreArea = getScoreArea(effectiveArea,levelSkeleton.slabSkeleton.poly.area())
    scoreOverlapped = getScoreOverlapped(overlappedArea,effectiveArea)
    SymScore = getScoreSymEcc(ex,ey,Rx,Ry)
    distributionScore = getDistrubtionScore(lengthX,lengthY,LX,LY)

    # print("\nscore length", scoreLengthX, scoreLengthY)

    # print("effective inslab area:", effectiveArea," score:", scoreArea)
    # print("overlapped area", overlappedArea," score:",scoreOverlapped)
    # print("eccentricty", SymScore)
    # print("Distance score", scoreDist)
    # print("radius score", radiuses)
    # print('distributionScore', distributionScore)

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
        'sym': SymScore,                                   #max([0,distance(cntr,centerV)/ar]),
        'lengthShearX': scoreLengthX,
        'lengthShearY': scoreLengthY,
        'unif': vecUni.magn(),
        'area': scoreArea,                                 #area/levelSkeleton.getSlabArea(),
        'overlapped': scoreOverlapped,
        'lengthX': lengthX,
        'lengthY': lengthY,
        'distance': scoreDist,
        'distribution': distributionScore
        }
    fitness = 0
    for key in coeffs:
        # print("fitness of",key,':',fitV[key]*coeffs[key] )
        fitness += fitV[key]*coeffs[key]
    fitV['totalScore'] = fitness
    return fitV


def calculateFitnessPopulation(population, constraints=None, comb = [0,0,0,0]):
    fitnesses = []
    for solution in population:
        # print("calculating:")
        fitnesses.append(solution.getFitness(constraints, comb)['totalScore'])
    return fitnesses