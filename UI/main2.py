import os
import sys
# from Optimization.Genetic import GeneticOperations2
from Geometry.Geom2D import Pnt, Ellip, Poly
from Geometry.ShapeToPoly import getPolygonesFromShape
from Ifc.IfcUtils import getSpaceShapesFromIfc
from Optimization.Genetic import GeneticOperations2
from Optimization.Genetic.GeneticAlgorithm import search
from Skeleton.LevelSkeleton import LevelSkeleton
from Structures.Level import Level
from Ifc import IfcUtils
from UI import Plotter
from shapely.geometry import Point


class Color(object):

    def __init__(self, red, green, blue):
        super(Color, self).__init__()
        self.r = red
        self.g = green
        self.b = blue

    def red(self):
        return self.r

    def green(self):
        return self.g

    def blue(self):
        return self.b


class Launcher(object):
    levels = []
    skeletonLevels = []
    viewerTabs = {}

    def __init__(self, parent=None, wallShapes=None, slabShapes=None):
        super(Launcher, self).__init__()
        self.constraints = {
            "ecc_w": -0.5,
            "area_w": 1,
            "length_w": 1,
            "ratio": 1,
            "d": 1,
        }
        self.levels = Level.generateLevelsFromShapes(wallShapes, slabShapes)
        print("INFO INIT: DONE GENERATING LEVELS FROM SHAPES")
        self.levels.sort(key=lambda lvl: lvl.getHeight())

        self.skeletonLevels = [LevelSkeleton.createSkeletonFromLevel(level) for level in self.levels]
        self.levelsHash = dict(list(zip(self.levels, self.skeletonLevels)))
        self.skeletonLevelsHash = dict(list(zip(self.skeletonLevels, self.levels)))
        print("INFO INIT: DONE GENERATING LEVELSKELETONS FROM LEVELS")
        baseSlabHeight = 0
        for level in self.levels:
            if not len(self.levelsHash[level].getPolys()):  # or level.getHeight() <= 0:
                baseSlabHeight = level.getHeight()
            else:
                break

        for i, levelSkeleton in enumerate(self.skeletonLevels):
            prevLevels = self.skeletonLevelsHash[levelSkeleton].getRightLowerLevels()
            if not prevLevels:
                continue

            prevLevels = [self.levelsHash[level] for level in prevLevels if level.getHeight() > baseSlabHeight]
            if not len(prevLevels):
                continue
            levelSkeleton.restrictLevelUsableWalls(prevLevels)

        self.levels = [level for level in self.levels if len(self.levelsHash[level].getPolys())]
        for level in self.levels:
            level.relatedLevels = self.levels
            level.rlowerLevels = None
        self.skeletonLevels = [levelSkeleton for levelSkeleton in self.skeletonLevels if len(levelSkeleton.getPolys())]
        self.solutions = {}

        self.selectedRow = 1
        self.pend = True

    def reinit_skeletons(self):
        self.skeletonLevels = [LevelSkeleton.createSkeletonFromLevel(level) for level in self.levels]
        self.levelsHash = dict(list(zip(self.levels, self.skeletonLevels)))
        self.skeletonLevelsHash = dict(list(zip(self.skeletonLevels, self.levels)))
        print("INFO INIT: DONE GENERATING LEVELSKELETONS FROM LEVELS")
        baseSlabHeight = 0
        for level in self.levels:
            if not len(self.levelsHash[level].getPolys()):  # or level.getHeight() <= 0:
                baseSlabHeight = level.getHeight()
            else:
                break

        for i, levelSkeleton in enumerate(self.skeletonLevels):
            prevLevels = self.skeletonLevelsHash[levelSkeleton].getRightLowerLevels()
            if not prevLevels:
                continue

            prevLevels = [self.levelsHash[level] for level in prevLevels if level.getHeight() > baseSlabHeight]
            if not len(prevLevels):
                continue
            levelSkeleton.restrictLevelUsableWalls(prevLevels)

        self.levels = [level for level in self.levels if len(self.levelsHash[level].getPolys())]
        self.skeletonLevels = [levelSkeleton for levelSkeleton in self.skeletonLevels if len(levelSkeleton.getPolys())]
        self.solutions = {}

    def showLowerFun(self):
        if self.selectedRow is not None:
            from matplotlib import pyplot as plt
            levelSkeleton = self.skeletonLevels[self.selectedRow]
            if levelSkeleton in self.solutions:
                levelSkeleton = self.solutions[levelSkeleton].levelSkeleton
            polys, colors = self.getPolygonsFromLevelSkeletons(levelSkeleton)
            colors = [[c.red() / 255., c.green() / 255., c.blue() / 255., 0.8] for c in colors]
            c = colors[-1]
            # Plotter.plotPolys(polys, self.selectedRow, "plan", colors)
            # plt.savefig('try1.png', bbox_inches='tight')
            polys = [poly.poly for poly in polys]
            alphas = [1 for poly in polys]
            c1 = levelSkeleton.getCenterFromSlab()
            c2 = levelSkeleton.getCenterFromShear()
            polys += [Point(c1.x(), c1.y()).buffer(0.1), Point(c2.x(), c2.y()).buffer(0.1)]
            colors += [[0, 1, 0], [1, 0, 0]]
            alphas += [1, 1]
            Plotter.plotShapely(polys, colors, alphas, 30, title="plan")
            boxes = [voileSkeleton.getSurrondingBox(self.constraints['d'])
                     for wallSkeleton in levelSkeleton.wallSkeletons
                     for voileSkeleton in wallSkeleton.getAllVoiles()]
            colors += [[0.5, 1, 0.5] for box in boxes]
            polys += boxes
            alphas += [0.2 for poly in boxes]

            Plotter.plotShapely(polys, colors, alphas, 20)
            plt.show()
            # plt.savefig('try2.png', bbox_inches='tight')
            # self.draw(polys)

    def multiSearch(self, diroot='saved', layers=None, iterations=1):

        def mygen2():
            c = {
                "rad_w": 0,
                "ecc_w": -0.5,
                "area_w": 1,
                "length_w": 1,
                "ratio": 1,
                "d": 1,
            }
            area_w = [0.1, 0.5, 1, 1.5, 2]
            length_w = [0.1, 0.5, 1, 1.5, 2]
            ecc_w = [-0.1, -1, -1.5]
            for aw in area_w:
                c['area_w'] = aw
                yield c
            c['area_w'] = 1
            for lw in length_w:
                c['length_w'] = lw
                yield c
            c['length_w'] = 1
            for ew in ecc_w:
                c['ecc_w'] = ew
                yield c

        def mygenprov():
            c = {
                "rad_w": 0,
                "ecc_w": -0.5,
                "area_w": 1,
                "length_w": 1,
                "ratio": 1,
                "d": 1,
            }
            yield c

        def mygen():
            c = {
                "rad_w": 0,
                "ecc_w": -0.5,
                "area_w": 1,
                "length_w": 1,
                "ratio": 1,
                "d": 1,
            }
            area_w = [1.5, 2, 4]
            d_ratios = [0.25, 0.5, 0.75]
            for d in d_ratios:
                c['d'] = d
                for w in area_w:
                    c['area_w'] = w
                    yield c



        count = 1
        for consts in mygenprov():
            dirname = diroot+'/constraints' + str(count) + '/'
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            open(dirname + 'constraints.txt', 'w').write("Torsional radius weight: " +
                                                         str(consts['rad_w']) +
                                                         "\nEccentricity weight: " +
                                                         str(consts['ecc_w']) +
                                                         "\nShear Wall length weight: " +
                                                         str(consts['length_w']) +
                                                         "\nShear Wall cover area weight: " +
                                                         str(consts['area_w']) +
                                                         "\nArea Distance ratio: " +
                                                         str(consts['d']))
            for iteration in range(0, iterations):
                dirIt = dirname + 'iteration' + str(iteration+1) + '/'
                self.constraints = consts
                self.reinit_skeletons()
                self.solutions = {}
                if layers is None:
                    skeletonLevels = self.skeletonLevels
                else:
                    skeletonLevels = self.skeletonLevels[:layers]
                for levelSkeleton in skeletonLevels[::-1]:
                    level = self.skeletonLevelsHash[levelSkeleton]
                    prevs = [self.solutions[self.levelsHash[p]].levelSkeleton for p in level.getUpperLevels()
                             if self.levelsHash[p] in self.solutions]
                    print(("PREVS LENGTH IS", len(prevs)))
                    if len(prevs):
                        levelSkeleton.copyLevelsVoiles(prevs)
                    i = self.skeletonLevels.index(levelSkeleton)
                    solution = search(levelSkeleton, filename="level" + str(i), constraints=self.constraints)
                    self.solutions[levelSkeleton] = solution

                print((self.solutions))
                self.saveSkeletons(dirIt, consts, layers)
            count += 1

    def saveSkeletons(self, root, consts, layers=None):
        print((self.skeletonLevels))
        if self.skeletonLevels is None:
            skeletonLevels = self.skeletonLevels
        else:
            skeletonLevels = self.skeletonLevels[:layers]

        for selectedRow in range(len(skeletonLevels)):
            lv = "level" + str(1 + selectedRow)
            froot = root + lv + '/'
            if not os.path.exists(froot):
                os.makedirs(froot)


            from matplotlib import pyplot as plt
            levelSkeleton = self.skeletonLevels[selectedRow]
            print(levelSkeleton)
            solution = self.solutions[levelSkeleton]
            if levelSkeleton in self.solutions:
                levelSkeleton = self.solutions[levelSkeleton].levelSkeleton
            polys, colors = self.getPolygonsFromLevelSkeletons(levelSkeleton)
            colors = [[c.red() / 255., c.green() / 255., c.blue() / 255., 0.8] for c in colors]
            # Plotter.plotPolys(polys, selectedRow, "plan", colors)
            polys = [poly.poly for poly in polys]
            alphas = [1 for poly in polys]
            c1 = levelSkeleton.getCenterFromSlab()
            c2 = levelSkeleton.getCenterFromShear()
            polys += [Point(c1.x(), c1.y()).buffer(0.1), Point(c2.x(), c2.y()).buffer(0.1)]
            colors += [[0, 1, 0], [1, 0, 0]]
            alphas += [1, 1]
            Plotter.plotShapely(polys, colors, alphas, 30, title="plan")
            plt.savefig(froot + 'layout.png', bbox_inches='tight')
            plt.clf()
            boxes = [voileSkeleton.getSurrondingBox(self.constraints['d'])
                     for wallSkeleton in levelSkeleton.wallSkeletons
                     for voileSkeleton in wallSkeleton.getAllVoiles()]
            colors += [[0.5, 1, 0.5] for box in boxes]
            polys += boxes
            alphas += [0.2 for poly in boxes]
            Plotter.plotShapely(polys, colors, alphas, 20)
            # plt.show()

            plt.savefig(froot + 'layout_ranges.png', bbox_inches='tight')
            plt.clf()
            fitness = solution.getFitness(constraints=self.constraints)
            constraints = self.constraints
            f = open(froot + 'properties.txt', 'w')
            f.write("constraints: \n")
            f.write("Torsional radius weight: " +
                                                         str(consts['rad_w']) +
                                                         "\nEccentricity weight: " +
                                                         str(consts['ecc_w']) +
                                                         "\nShear Wall length weight: " +
                                                         str(consts['length_w']) +
                                                         "\nShear Wall cover area weight: " +
                                                         str(consts['area_w']) +
                                                         "\nArea Distance ratio: " +
                                                         str(consts['d']))
            f.write("\n\nslab center: " + str(c1) +
                    "\necc center: " + str(c2) +
                    "\nlength X: " + str(fitness['lengthX']) +
                    "\nlength Y: " + str(fitness['lengthY']))
            f.write("needed: " +
                    str(solution.levelSkeleton.getVoileLengthNeeded(constraints['ratio'])))
            f.write("covered area: " + str(solution.getAreaCoveredBoxes(constraints['d'])))
            f.write("overlapped area: " + str(solution.getOverlappedArea(constraints['d'])))

    def getPolygonsFromLevels(self, levels):
        polys = []
        for level in levels:
            polys += self.getPolygonsFromLevelSkeletons(
                LevelSkeleton.createSkeletonFromLevel(level))
        return polys

    def getPolygonsFromLevelSkeletons(self, levelSkeleton):
        polygons = [wallSkeleton.poly.copy() for wallSkeleton in levelSkeleton.wallSkeletons]
        colors = [Color(220, 220, 220) for wallSkeleton in levelSkeleton.wallSkeletons]
        polygons += [voileSkeleton.poly.copy()
                     for wallSkeleton in levelSkeleton.wallSkeletons
                     for voileSkeleton in wallSkeleton.getAllVoiles()]

        colors += [Color(255, 0, 0)
                   for wallSkeleton in levelSkeleton.wallSkeletons
                   for voileSkeleton in wallSkeleton.getAllVoiles()]
        if not len(polygons):
            return
        polys = (polygons, colors)
        center = Pnt.createPointFromShapely(levelSkeleton.slabSkeleton.poly.centroid())
        return polys
        # ellipses = ([Ellip(center, 0.5)], [QtGui.QColor(0, 255, 0)])
        # self.draw(polys,ellipses)




def createShapes(file):
    wall_shapes = IfcUtils.getWallShapesFromIfc(file)
    # wall_shapes = IfcUtils.getSlabShapesFromIfc("IFCFiles/projet.ifc")
    wShapes = []
    for wall, shape in wall_shapes:
        wShapes.append(shape)

    slab_shapes = IfcUtils.getSlabShapesFromIfc(file)
    sShapes = []
    for wall, shape in slab_shapes:
        sShapes.append(shape)

    return wShapes, sShapes


def main():
    file = "../IFCFiles/ifc_adv1.ifc"
    wShapes, sShapes = createShapes(file)
    space_shapes = getSpaceShapesFromIfc(file)
    for _, shape in space_shapes:
        polygons = getPolygonesFromShape(shape)
        print("shape is ************************************")
        for polygon in polygons:
            print("polygon:")
            for pnt in polygon.points:
                print(("point is: (%.2f, %.2f, %.2f) " % (pnt.x, pnt.y, pnt.z)))
    launcher = Launcher(wallShapes=wShapes, slabShapes=sShapes)
    launcher.multiSearch('saveAdv', iterations=1)

    # file = "../IFCFiles/villa1.ifc"
    # wShapes, sShapes = createShapes(file)
    # launcher = Launcher(wallShapes=wShapes, slabShapes=sShapes)
    # launcher.multiSearch('saved3oldEcc')
    # file = "../IFCFiles/villa2.ifc"
    # wShapes, sShapes = createShapes(file)
    # launcher = Launcher(wallShapes=wShapes, slabShapes=sShapes)
    # launcher.multiSearch('saved4oldEcc', 1)
    # file = "../IFCFiles/Immeuble39.ifc"
    # wShapes, sShapes = createShapes(file)
    # launcher = Launcher(wallShapes=wShapes, slabShapes=sShapes)
    # launcher.multiSearch('saved5oldEcc', 2)
    # file = "../IFCFiles/Immeuble2.ifc"
    # wShapes, sShapes = createShapes(file)
    # launcher = Launcher(wallShapes=wShapes, slabShapes=sShapes)
    # launcher.multiSearch('saved6oldEcc')

if __name__ == '__main__':
    main()
