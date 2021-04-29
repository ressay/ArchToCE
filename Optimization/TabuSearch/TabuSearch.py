from Optimization.TabuSearch.AxesSolution import AxesSolution
import random
import copy
import time


def random_solution(Axes) -> AxesSolution:
    # create axes randomly with your constraints and add them to the list
    haxes = Axes[0]
    vaxes = Axes[1]
    a = len(haxes)
    b= len(vaxes)
    # random.seed(5)

    Hcondition=False
    while not Hcondition:
        A = random.randint(3, a)
        print("random number of Haxes",A,"from",a)
        Haxes=random.sample(haxes,A)
        Hcondition=AxesSolution(Haxes).HDistanceCondition()

    Vcondition=False
    while not Vcondition:
        B = random.randint(3, b)
        print("random number of Vaxes",B,"from",b)
        Vaxes=random.sample(vaxes,B)
        Vcondition=AxesSolution(Vaxes).VDistanceCondition()

    axes=[[],[]]
    axes[0] = Haxes
    axes[1] = Vaxes
    return AxesSolution(axes)


def stopping_condition(solution: AxesSolution) -> bool:
    # check here if solution is good enough stop, otherwise continue search

    return False


def get_neighbors(solution: AxesSolution,Axes) -> list:
    # mutate your solution with different mutations here, create many mutated solutions and add them to neighbors
    neighbors = []
    Sol=copy.deepcopy(solution.axes)
    AvailableHaxes = []
    AvailableVaxes = []
    for Haxe in Axes[0]:
        if Haxe not in solution.axes[0]: AvailableHaxes.append(Haxe)
    for Vaxe in Axes[1]:
        if Vaxe not in solution.axes[1]: AvailableVaxes.append(Vaxe)

    for Haxe in AvailableHaxes:
        for Vaxe in AvailableVaxes:
            Sol[0].append(Haxe)
            Sol[1].append(Vaxe)
            neighbors.append(Sol)
            Sol=copy.deepcopy(solution.axes)

    return neighbors


def fitness(solution: AxesSolution,Slab) -> float:
    # evaluate here how good is this axes distribution
    Max_x = round(Slab.poly.MaxCoords().x())
    Max_y = round(Slab.poly.MaxCoords().y())
    Min_x = round(Slab.poly.MinCoods().x())
    Min_y = round(Slab.poly.MinCoods().y())

    return 0


def tabu_search(potentialColumns,Axes,slab,limit=10000) -> AxesSolution:
    sbest = random_solution(Axes)
    best_candidate = sbest
    # I did not implement tabu list here, but this should be good enough to start and test your code.

    # iteration = 0
    # while iteration < limit and not stopping_condition(sbest):
    neighbors = get_neighbors(best_candidate,Axes)
    #     best_candidate = neighbors[0]
    #
    #     for candidate in neighbors:
    #         if fitness(candidate) > fitness(best_candidate):
    #             best_candidate = candidate
    #
    #     if fitness(best_candidate) > fitness(sbest):
    #         sbest = best_candidate
    for neighbor in neighbors:
        print("Neighbor n°:", neighbors.index(neighbor))
        print("neighbor Haxis solution:")
        for axis in neighbor[0]:
            print(axis.bounds)
        print("neighbor Vaxis solution:")
        for axis in neighbor[1]:
            print(axis.bounds)
        # iteration+=1

    return sbest


