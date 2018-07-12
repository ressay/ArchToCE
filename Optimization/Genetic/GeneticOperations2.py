import random
import timeit

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
        rand = random.uniform(0,1)
        if rand < 0.5:
            resultWalls1.append(wall1)
            resultWalls2.append(wall2)
        else:
            resultWalls1.append(wall2)
            resultWalls2.append(wall1)

    s1 = Solution(LevelSkeleton(resultWalls1,levelS1.slabSkeleton,levelS1.level))
    s2 = Solution(LevelSkeleton(resultWalls2,levelS1.slabSkeleton,levelS1.level))
    return s1,s2


def mutate(solution,mutationSize=None):
    solution.reInitFitness()
    levelSkeleton = solution.levelSkeleton
    # select random wall:
    rand = int(random.uniform(0,len(levelSkeleton.wallSkeletons)-0.1))
    newWall = levelSkeleton.wallSkeletons[rand].copy()
    levelSkeleton.wallSkeletons[rand] = newWall
    if not mutationSize:
        mutationSize = int(random.uniform(1,21))
    if random.uniform(0,1) < 0.5:
        mutateWall(newWall,True,mutationSize)
    else:
        mutateWall(newWall,False,mutationSize)


def mutateWall(wallSkeleton,positive=True,mutationSize=1):
    # wallSkeleton.reInitFitness()
    if positive or len(wallSkeleton.attachedVoiles) == 0:
        r = random.uniform(0,1)
        if r < 0.5 or len(wallSkeleton.attachedVoiles) == 0: #add new shear wall
            start = int(random.uniform(0,wallSkeleton.vecLength.magn()-WallSkeleton.miniVoileLength))
            end = start + WallSkeleton.miniVoileLength
            wallSkeleton.attachVoile(VoileSkeleton(wallSkeleton,start,end))
        else: # change shear wall size
            rand = int(random.uniform(0,len(wallSkeleton.attachedVoiles)-0.1))
            selectedVoile = wallSkeleton.getVoile(rand)
            start = selectedVoile.start
            end = selectedVoile.end
            if r < 0.75:
                start = max(0,start-mutationSize*WallSkeleton.discreteFactor)
            else:
                end = min(wallSkeleton.vecLength.magn(),end + mutationSize*WallSkeleton.discreteFactor)

            v = VoileSkeleton(wallSkeleton,start,end)
            wallSkeleton.attachVoile(v)
    else:
        r = random.uniform(0,1)
        if r < 0.5:  # remove shear wall
            rand = int(random.uniform(0, len(wallSkeleton.attachedVoiles) - 0.1))
            wallSkeleton.removeVoile(rand)
        else:  # change shear wall size
            rand = int(random.uniform(0, len(wallSkeleton.attachedVoiles) - 0.1))
            selectedVoile = wallSkeleton.getVoile(rand)
            start = selectedVoile.start
            end = selectedVoile.end
            if r < 0.75:
                start = start + mutationSize * WallSkeleton.discreteFactor
            else:
                end = end - mutationSize * WallSkeleton.discreteFactor
            wallSkeleton.removeVoile(rand)
            if end - start >= WallSkeleton.miniVoileLength:
                v = VoileSkeleton(wallSkeleton, start, end)
                wallSkeleton.attachVoile(v)