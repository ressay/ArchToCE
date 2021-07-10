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
    wallSkeletons1 = []
    wallSkeletons2 = []
    reserve1 = []
    reserve2 = []

    for wallskeleton in levelS1.wallSkeletons:
        if not wallskeleton.iscolumnParent:
            wallSkeletons1.append(wallskeleton)
        else:reserve1.append(wallskeleton)

    for wallskeleton in levelS2.wallSkeletons:
        if not wallskeleton.iscolumnParent:
            wallSkeletons2.append(wallskeleton)
        else:reserve2.append(wallskeleton)

    for wall1,wall2 in zip(wallSkeletons1,wallSkeletons2):
        rand = random.uniform(0,1)
        if rand < 0.5:
            resultWalls1.append(wall1)
            resultWalls2.append(wall2)
        else:
            resultWalls1.append(wall2)
            resultWalls2.append(wall1)

    for wall in reserve1: resultWalls1.append(wall)
    for wall in reserve2: resultWalls2.append(wall)

    s1 = Solution(LevelSkeleton(resultWalls1,levelS1.slabSkeleton,levelS1.level))
    s2 = Solution(LevelSkeleton(resultWalls2,levelS1.slabSkeleton,levelS1.level))
    return s1,s2


def mutate(solution,mutationSize=None):
    solution.reInitFitness()
    levelSkeleton = solution.levelSkeleton
    # select random wall:
    Walls = []
    Columns = []
    for wallskeleton in levelSkeleton.wallSkeletons:
        if not wallskeleton.iscolumnParent:
            Walls.append(wallskeleton)
        else: Columns.append(wallskeleton)
    wallsNumber = len(Walls)
    rand = int(random.uniform(0,wallsNumber-0.1))
    newWall = Walls[rand].copy()
    Walls[rand] = newWall
    if not mutationSize:
        mutationSize = int(random.uniform(1,21))
    if random.uniform(0,1) < 0.5:
        mutateWall(newWall,True,mutationSize)
    else:
        mutateWall(newWall,False,mutationSize)

    levelSkeleton.wallSkeletons = []
    for wall in Walls: levelSkeleton.wallSkeletons.append(wall)
    for Column in Columns:
        levelSkeleton.wallSkeletons.append(Column)


def mutateWall(wallSkeleton,positive=True,mutationSize=1):
    if WallSkeleton.miniVoileLength > wallSkeleton.vecLength.magn():
        return
    # wallSkeleton.reInitFitness()
    if positive or len(wallSkeleton.attachedVoiles) == 0:
        r = random.uniform(0,1)
        if r < 0.5 or len(wallSkeleton.attachedVoiles) == 0: #add new shear wall
            if wallSkeleton.vecLength.magn() == WallSkeleton.miniVoileLength:
                start = 0
                end = wallSkeleton.vecLength.magn()
            else:
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
