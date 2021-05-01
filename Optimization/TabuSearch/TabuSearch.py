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
    random.seed(5)

    Hcondition=False
    while not Hcondition:
        A = random.randint(3, a)
        print("random number of Haxes",A,"from",a)
        Haxes=random.sample(haxes,A)
        Hcondition=AxesSolution(Haxes).HDistanceCondition()[0]

    Vcondition=False
    while not Vcondition:
        B = random.randint(3, b)
        print("random number of Vaxes",B,"from",b)
        Vaxes=random.sample(vaxes,B)
        Vcondition=AxesSolution(Vaxes).VDistanceCondition()[0]

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
            Sol[1].append(Vaxe)
            Sol[0].append(Haxe)

            if not AxesSolution(Sol[0]).HDistanceCondition()[0]:
                if Haxe == AxesSolution(Sol[0]).HDistanceCondition()[1]:
                    Sol[0].remove(AxesSolution(Sol[0]).HDistanceCondition()[2])
                else:
                    Sol[0].remove(AxesSolution(Sol[0]).HDistanceCondition()[1])
            if not AxesSolution(Sol[1]).VDistanceCondition()[0]:
                if Haxe == AxesSolution(Sol[1]).VDistanceCondition()[1]:
                    Sol[1].remove(AxesSolution(Sol[1]).VDistanceCondition()[2])
                else:
                    Sol[1].remove(AxesSolution(Sol[1]).VDistanceCondition()[1])

                neighbors.append(AxesSolution(Sol))
                Sol = copy.deepcopy(solution.axes)

    return neighbors


def fitness(solution: AxesSolution,Slab) -> float:
    # evaluate here how good is this axes distribution

    R_x = round(Slab.poly.MaxCoords().x())
    L_x = round(Slab.poly.MinCoods().x())
    U_y = round(Slab.poly.MaxCoords().y())
    D_y = round(Slab.poly.MinCoods().y())
    x,X,y,Y=solution.get_DistancesFromEdges(R_x,L_x,U_y,D_y)

    Cond1 = 1 # if the axis contains columns in the intersection or not
    Cond2 = len(solution.axes[0])/((U_y-D_y)/4+1)+len(solution.axes[1])/((R_x-L_x)/4+1)


    score=(1/x+1/X+1/y+1/Y)*Cond1+Cond2




    return score


def tabu_search(potentialColumns,Axes,slab,limit=10000) -> AxesSolution:
    sbest = random_solution(Axes)
    best_candidate = sbest
    # I did not implement tabu list here, but this should be good enough to start and test your code.

    iteration = 0
    while iteration < limit :
        print("Iteration",iteration)
        neighbors = get_neighbors(best_candidate,Axes)

        best_candidate = neighbors[0]
        for candidate in neighbors:
            if fitness(candidate,slab) > fitness(best_candidate,slab):
                best_candidate = candidate

        if fitness(best_candidate,slab) > fitness(sbest,slab):
            print("fitness:",fitness(best_candidate,slab))
            sbest = best_candidate
        iteration+=1
    # for neighbor in neighbors:
    #     print("Neighbor n°:", neighbors.index(neighbor))
    #     Neighbor=neighbor.axes
    #     fit=fitness(neighbor,slab)
    #     print("fitness:",fit,"\nneighbor Haxis solution:")
    #     for axis in Neighbor[0]:
    #         print(axis.bounds)
    #     print("neighbor Vaxis solution:")
    #     for axis in Neighbor[1]:
    #         print(axis.bounds)

    return sbest