from Optimization.TabuSearch.AxesSolution import AxesSolution
import random
import time


def random_solution(haxes,vaxes,potentialColumns) -> AxesSolution:
    # create axes randomly with your constraints and add them to the list
    axes = []
    hmindist=0

    random.seed(5)
    a = len(haxes)
    while hmindist<2.5 :
        aa = random.randint(2, a)
        print("random number of haxes",aa,a)
        axes=random.sample(haxes,aa)

        hmindist = AxesSolution(axes).HminimumDistance()

    return axes


def stopping_condition(solution: AxesSolution) -> bool:
    # check here if solution is good enough stop, otherwise continue search

    return False


def get_neighbors(solution: AxesSolution) -> list:
    neighbors = []

    # mutate your solution with different mutations here, create many mutated solution and add them to neighbors

    return neighbors


def fitness(solution: AxesSolution) -> float:
    # evaluate here how good is this axes distribution

    return 0


def tabu_search(potentialColumns,haxes,vaxes,limit=10000) -> AxesSolution:
    sbest = random_solution(haxes,vaxes,potentialColumns)
    best_candidate = sbest

    # I did not implement tabu list here, but this should be good enough to start and test your code.

    # iteration = 0
    # while iteration < limit and not stopping_condition(sbest):
    #     neighbors = get_neighbors(best_candidate)
    #     best_candidate = neighbors[0]
    #
    #     for candidate in neighbors:
    #         if fitness(candidate) > fitness(best_candidate):
    #             best_candidate = candidate
    #
    #     if fitness(best_candidate) > fitness(sbest):
    #         sbest = best_candidate
    #
    #     iteration+=1

    return sbest
