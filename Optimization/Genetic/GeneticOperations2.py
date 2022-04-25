import random

from Optimization.Solution import Solution
from Skeleton.LevelSkeleton import LevelSkeleton
from Skeleton.VoileSkeleton import VoileSkeleton
from Skeleton.WallSkeleton import WallSkeleton
import copy
import itertools

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
    a = s1.levelSkeleton.ScoreOfUnacceptableVoiles()
    b = s2.levelSkeleton.ScoreOfUnacceptableVoiles()
    # print(a,b)
    if 0<a[0]<0.9:
        s1 = fixShortbeam(s1,a)
    if 0<b[0]<0.9:
        s1 = fixShortbeam(s2,b)
    return s1,s2

def fixShortbeam(solution, problemwalls):
    # print('here defective walls', problemwalls)
    # levelS = solution.levelSkeleton
    ProblemWallS= []
    ProblemVoiles = []
    ProblemWallS.append(problemwalls[1][2])
    ProblemVoiles.append(problemwalls[1][1])
    combinations = []
    # print('1')
    # for L in range(1, len(problemwalls[1][0])+1):
    #     for subset in itertools.combinations(problemwalls[1][0],L):
    #         print('2', subset)
    #         fixedVoiles = []
    #         fixedWallSkeletons = []
    #         for i in subset:
    newSolution = copy.copy(solution)
    List = []
    for j in range(len(problemwalls[1][0])):
        List.append(j)
    for i in range(len(problemwalls[1][0])):
        # print(i)
        ProblemWallS = []
        ProblemVoiles = []
        ProblemWallS.append(problemwalls[1][2])
        ProblemVoiles.append(problemwalls[1][1])
        # print(ProblemWallS[0][0])
        # print(ProblemVoiles[0][0])
                # for wallskelton in solution.levelSkeleton.wallSkeletons:
                #     if solution.levelSkeleton.wallSkeletons.index(wallskelton) != ProblemWallS[i]:
                #         fixedWallSkeletons.append(wallskelton)
                #     else:
                #         for voileS in wallskelton.getAllvoiles():
                #             if wallskelton.getAllvoiles().index(voileS) != ProblemVoiles[i]:
                #                 fixedVoiles.append(voileS)
                #         print('2')
                #         fixedWallSkeletons.append((WallSkeleton(fixedVoiles)))
                # fixedsolution = Solution(LevelSkeleton(fixedWallSkeletons,solution.levelSkeleton.slabSkeleton
                #                                        ,solution.levelSkeleton.level))
                # print('3')
                # print(fixedsolution.levelSkeleton.ScoreOfUnacceptableVoiles()[0])
        a = ProblemWallS[0][0]
        b = ProblemVoiles[0][0]
        # print('here score of before',newSolution.levelSkeleton.wallSkeletons[a], a ,b)
        wallS = newSolution.levelSkeleton.wallSkeletons[a]
        # print('passed')
        wallS.removeVoile(b)
        # print('here score of after', newSolution.levelSkeleton.ScoreOfUnacceptableVoiles())
        if newSolution.levelSkeleton.ScoreOfUnacceptableVoiles()[0]>0.9:
            # print('YES FIXED')
            return newSolution
        else: problemwalls = newSolution.levelSkeleton.ScoreOfUnacceptableVoiles()

def mutate(solution,mutationSize=None):
    # aliasSolution = copy.copy(solution)
    # aliasSolution.reInitFitness()
    solution.reInitFitness()
    # levelSkeleton = aliasSolution.levelSkeleton
    # select random wall:
    levelSkeleton = solution.levelSkeleton
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
    if levelSkeleton.ScoreOfUnacceptableVoiles()[0]<0.9:
        solution = fixShortbeam(solution, levelSkeleton.ScoreOfUnacceptableVoiles())
    return solution

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
