from Geometry.Geom2D import Pnt

def distance(p1,p2):
    p = p1 - p2
    return p.magn()


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
        length = 0
        for voileSkeleton in wallSkeleton.attachedVoiles:
            # for voileSkeleton in voiles:
            # print ("looping")
            centerV = voileSkeleton.poly.centroid()
            centerV = Pnt(centerV.x, centerV.y)
            dis += distance(centerV, self.center)
            length += (voileSkeleton.end - voileSkeleton.start)
            size += 1
        wallSkeleton.evalData = dis, size, length
        return dis, size, length

def calculateFitnessSolution(solution):
    fitness = 0
    levelSkeleton = solution.levelSkeleton
    wallEvaluator = WallEvaluator(levelSkeleton)
    # print ("before looping")
    # voiles = [voile for wallSkeleton in levelSkeleton.wallSkeletons
    #                       for voile in wallSkeleton.attachedVoiles]
    size = 0
    dis = 0
    length = 0
    for wallSkeleton in levelSkeleton.wallSkeletons:
        # print "attached voiles : " + str(len(wallSkeleton.attachedVoiles))
        d,s,l = wallEvaluator.calculateFitnessWall(wallSkeleton)
        dis += d
        size += s
        length += l


    fitness = length
    return fitness


def calculateFitnessPopulation(population):
    fitnesses = []
    for solution in population:
        # print("calculating:")
        fitnesses.append(solution.getFitness())

    return fitnesses