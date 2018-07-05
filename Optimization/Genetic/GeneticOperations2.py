import random
import timeit

from Optimization.Solution import Solution
from Skeleton.LevelSkeleton import LevelSkeleton


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


def mutate(solution):
    levelSkeleon = solution.levelSkeleton

