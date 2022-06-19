from Optimization.TabuSearch.AxesSolution import AxesSolution
import random
import copy
import math
from shapely.geometry import point, linestring
import timeit


def random_solution(Axes,Slab) -> AxesSolution:
    # create axes randomly with your constraints and add them to the list
    haxes = Axes[0]
    vaxes = Axes[1]
    a = len(haxes)
    b = len(vaxes)
    R_x = round(Slab.poly.MaxCoords().x())
    L_x = round(Slab.poly.MinCoords().x())
    U_y = round(Slab.poly.MaxCoords().y())
    D_y = round(Slab.poly.MinCoords().y())
    print(L_x, D_y, R_x, U_y)

    start = timeit.default_timer()
    Hcondition = False
    while not Hcondition:
        A = random.randint(2, a)
        print("random number of Haxes",A,"from",a)
        Haxes = random.sample(haxes, A)
        Hcondition = AxesSolution(Haxes).HDistanceCondition(U_y, D_y)[0]
    stop = timeit.default_timer()
    print(("time it took random horizontal sol: " + str(round(stop - start,2))))

    start = timeit.default_timer()
    Vcondition = False
    while not Vcondition:
        B = random.randint(2, b)
        print("random number of Vaxes",B,"from",b)
        Vaxes = random.sample(vaxes, B)
        Vcondition = AxesSolution(Vaxes).VDistanceCondition(R_x, L_x)[0]
    stop = timeit.default_timer()
    print(("time it took random vertical sol: " + str(round(stop - start,2))))

    axes = [[], []]
    axes[0] = Haxes
    axes[1] = Vaxes
    print(" Haxis solution:")
    for axis in axes[0]:
        print(axis)
    print(" Vaxis solution:")
    for axis in axes[1]:
        print(axis)
    return AxesSolution(axes)


def stopping_condition(solution: AxesSolution) -> bool:
    # check here if solution is good enough stop, otherwise continue search

    return False


def get_neighbors(solution: AxesSolution, Slab, Axes) -> list:
    # mutate your solution with different mutations here, create many mutated solutions and add them to neighbors
    neighbors = []
    Sol = copy.deepcopy(solution.axes)
    AvailableHaxes = []
    AvailableVaxes = []
    R_x = round(Slab.poly.MaxCoords().x())
    L_x = round(Slab.poly.MinCoords().x())
    U_y = round(Slab.poly.MaxCoords().y())
    D_y = round(Slab.poly.MinCoords().y())
    for Haxe in Axes[0]:
        if Haxe not in solution.axes[0]: AvailableHaxes.append(Haxe)
    for Vaxe in Axes[1]:
        if Vaxe not in solution.axes[1]: AvailableVaxes.append(Vaxe)

    # Adding/ moving horizontal axis
    for Haxe in AvailableHaxes:

        Sol[0].append(Haxe)
        condition,first,second,i=AxesSolution(Sol[0]).HDistanceCondition(U_y,D_y)
        if i==0:
            Sol[0].remove(first)
        condition, first, second, i = AxesSolution(Sol[0]).HDistanceCondition(U_y, D_y)
        if i==0:
            Sol[0].remove(first)
        neighbors.append(AxesSolution(Sol))
        Sol = copy.deepcopy(solution.axes)

    # Adding/ moving Vertical axis
    for Vaxe in AvailableVaxes:
        Sol[1].append(Vaxe)
        condition,first,second,i = AxesSolution(Sol[1]).VDistanceCondition(R_x,L_x)
        if i==0:
            Sol[1].remove(first)
        condition, first, second, i = AxesSolution(Sol[1]).VDistanceCondition(R_x, L_x)
        if i == 0:
            Sol[1].remove(first)
        neighbors.append(AxesSolution(Sol))
        Sol = copy.deepcopy(solution.axes)

    # Removing horizontal axis
    for Haxe in Sol[0]:
        Sol[0].remove(Haxe)
        neighbors.append(AxesSolution(Sol))
        Sol = copy.deepcopy(solution.axes)

    # Removing vertical axis
    for Vaxe in Sol[1]:
        Sol[1].remove(Vaxe)
        neighbors.append(AxesSolution(Sol))
        Sol = copy.deepcopy(solution.axes)

    return neighbors


def fitness(solution: AxesSolution,Axes,Slab,potentialC) -> float:
    # evaluate here how good is this axes distribution

    R_x = round(Slab.poly.MaxCoords().x())
    L_x = round(Slab.poly.MinCoords().x())
    U_y = round(Slab.poly.MaxCoords().y())
    D_y = round(Slab.poly.MinCoords().y())
    x,X,y,Y=solution.get_DistancesFromEdges(R_x,L_x,U_y,D_y)
    slab_len = abs(U_y - D_y)
    slab_wid = abs(R_x-L_x)
    intersections=[]

    p = 0
    for Vaxis in solution.axes[1]:
        for Haxis in solution.axes[0]:
            intersection = linestring.BaseGeometry.intersection(Haxis,Vaxis)
            if intersection not in intersections: intersections.append(intersection)
        for intersection in intersections:
            if intersection not in potentialC:
                p=p+1
    # print("here p",p)
    # score1 = 1 / (x + X + y + Y)
    # score2 = math.pow(1/p,3)
    # score3 = len(solution.axes[0])/((U_y-D_y)/4+1)+len(solution.axes[1])/((R_x-L_x)/4+1)
    # score = (score1+score3)*score2
    desiredHaxes = (U_y-D_y)/4+1
    desiredVaxes = (R_x-L_x)/4+1
    maxH_error=max(abs(len(Axes[0])-desiredHaxes),abs(desiredHaxes-2))
    maxV_error=max(abs(len(Axes[1])-desiredVaxes),abs(desiredVaxes-2))

    score1 = 0.5*abs(len(solution.axes[0])-desiredHaxes)/maxH_error+\
             0.5*abs(len(solution.axes[1])-desiredVaxes)/maxV_error
    score2 = 0.25*((y+Y)/(0.5*slab_len)+(x+X)/(0.5*slab_wid))
    score3 = p/len(intersections)
    score4 = solution.get_equidistance()

    # print("score1:",score1,"score2:",score2,"score3:",score3)
    fitness= 1/(1+0.5*score1+score2+3*score3+0.1*score4)
    return fitness


def tabu_search(potentialColumns,Axes,slab,limit=10000) -> AxesSolution:
    limit = 10
    PotentialC=potentialColumns
    sbest = random_solution(Axes,slab)
    best_candidate = sbest
    # I did not implement tabu list here, but this should be good enough to start and test your code.
    # print("Haxis solution:")
    # for axis in sbest.axes[0]:
    #     print(axis)
    # print("Vaxis solution:")
    # for axis in sbest.axes[0]:
    #     print(axis)
    iteration = 0
    while iteration < limit:

        print("Iteration",iteration)
        start = timeit.default_timer()
        neighbors = get_neighbors(best_candidate,slab,Axes)
        stop = timeit.default_timer()
        print(("time it took neighbors: " + str(round(stop - start,2))))

        start = timeit.default_timer()
        best_candidate = neighbors[0]
        for candidate in neighbors:
            if fitness(candidate,Axes,slab,PotentialC) > fitness(best_candidate,Axes,slab,PotentialC):
                best_candidate = candidate
        stop = timeit.default_timer()
        print(("time it took best neighbor: " + str(round(stop - start,2))))

        if fitness(best_candidate,Axes,slab,PotentialC) > fitness(sbest,Axes,slab,PotentialC):
            print("fitness:",fitness(best_candidate,Axes,slab,PotentialC))
            sbest = best_candidate


            # print("new Haxis solution:")
            # for axis in sbest.axes[0]:
            #     print(axis)
            # print("new Vaxis solution:")
            # for axis in sbest.axes[1]:
            #     print(axis)
        iteration += 1
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