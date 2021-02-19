import random

from Optimization.Solution import Solution
from Skeleton.LevelSkeleton import LevelSkeleton
from Skeleton.VoileSkeleton import VoileSkeleton
from Skeleton.WallSkeleton import WallSkeleton


def cross(solution1,solution2):
    levelS1 = solution1.levelSkeleton
    levelS2 = solution2.levelSkeleton
    resultWalls1 = []
    resultWalls2 = []
    for wall1,wall2 in zip(levelS1.wallSkeletons,levelS2.wallSkeletons):
        w1,w2 = crossWalls(wall1,wall2,random.uniform(0,1))
        resultWalls1.append(w1)
        resultWalls2.append(w2)
    s1 = Solution(LevelSkeleton(resultWalls1,levelS1.slabSkeleton,levelS1.level))
    s2 = Solution(LevelSkeleton(resultWalls2,levelS1.slabSkeleton,levelS1.level))
    return s1,s2

def merge(solution1,solution2):
    levelS1 = solution1.levelSkeleton
    levelS2 = solution2.levelSkeleton
    resultWalls = []
    for wall1,wall2 in zip(levelS1.wallSkeletons,levelS2.wallSkeletons):
        resultWalls.append(mergeWalls(wall1,wall2))
    return Solution(LevelSkeleton(resultWalls,levelS1.slabSkeleton,levelS1.level))

def mergeVoile(voiles,voile):
    i = 0
    toDelete = []
    for v in voiles:
        if v.start <= voile.start < v.end:
            # voiles.remove(v)
            # del voiles[i]
            toDelete.append(i)
            voile = VoileSkeleton(v.parentWall,v.start,max(v.end,voile.end))
            # return mergeVoile(voiles,v)
        elif voile.start <= v.start < voile.end:
            # voiles.remove(v)
            # del voiles[i]
            toDelete.append(i)
            voile = VoileSkeleton(v.parentWall, voile.start, max(v.end, voile.end))
            # return mergeVoile(voiles,v)
        i += 1
    for i in sorted(toDelete,reverse=True):
        del voiles[i]
    voiles.append(voile)
    return voiles

def mergeVoiles(voiles1,voiles2):
    result = list(voiles1)
    for voile in voiles2:
        mergeVoile(result,voile)
    return result

def mergeWalls(wallSkeleton1 ,wallSkeleton2):
    #select random space from both walls
    voiles1 = wallSkeleton1.getVoilesBetween()
    voiles2 = wallSkeleton2.getVoilesBetween()
    resVoiles = mergeVoiles(voiles1,voiles2)
    resWall = WallSkeleton(wallSkeleton1.poly.copy())
    for voile in resVoiles:
        resWall.attachVoile(voile)
    return resWall

def crossWalls(wallSkeleton1 ,wallSkeleton2,crossPoint=0.5):
    print("cross Point: " + str(crossPoint))
    #select random space from both walls
    voiles1 = wallSkeleton1.getVoilesBetween(0, crossPoint)
    voiles2 = wallSkeleton2.getVoilesBetween(crossPoint, 1)
    resVoiles = mergeVoiles(voiles1, voiles2)
    resWall1 = WallSkeleton(wallSkeleton1.poly.copy())
    for voile in resVoiles:
        resWall1.attachVoile(voile)

    voiles1 = wallSkeleton2.getVoilesBetween(0, crossPoint)
    voiles2 = wallSkeleton1.getVoilesBetween(crossPoint, 1)
    resVoiles = mergeVoiles(voiles1, voiles2)
    resWall2 = WallSkeleton(wallSkeleton1.poly.copy())
    for voile in resVoiles:
        resWall2.attachVoile(voile)
    return resWall1,resWall2
