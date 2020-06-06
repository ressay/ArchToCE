import os
import sys
import inspect
from random import random

from Code import *

from Geometry.Geom2D import Pnt, Ellip, Poly
from Optimization.Genetic import GeneticOperations2
from Optimization.Genetic.GeneticAlgorithm import search
from Skeleton.LevelSkeleton import LevelSkeleton
from Skeleton.StoreySkeleton import StoreySkeleton
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
        self.levelsHash = dict(zip(self.levels, self.skeletonLevels))
        self.skeletonLevelsHash = dict(zip(self.skeletonLevels, self.levels))
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

        self.storey_mode = False
        self.levels = [level for level in self.levels if len(self.levelsHash[level].getPolys())]
        self.skeletonLevels = [levelSkeleton for levelSkeleton in self.skeletonLevels if len(levelSkeleton.getPolys())]
        self.storeySkeletons = []
        heights = []
        for levelSkeleton in self.skeletonLevels:
            height = levelSkeleton.level.getHeight()
            if height not in heights:
                skeletons = [levelSkeleton]
                heights.append(height)
                for ls in self.skeletonLevels:
                    if ls.level.getHeight() == height:
                        skeletons.append(ls)

                self.storeySkeletons.append(StoreySkeleton(skeletons))
        self.solutions = {}
        self.solutions = {}

        self.selectedRow = 1
        self.pend = True

        # Vertical Loads
        Sdiv = SlabDivision(self.storeySkeletons[0])
        # Sdiv.importWalls(self.skeletonLevels[0])
        # Seg = Sdiv.createSlabSegments()
        # f2 = plt.figure(3,)
        # for segment in Sdiv.createSlabSegments():
        #     segment.End1.plotEnd()
        #     segment.End2.plotEnd()
        #     segment.PlotSeg()

        for room in Sdiv.rooms:
            # 0x7fd0cba0b9e0 >
            print("room", room)
            fig, ax = plt.subplots()
            color = (random(), random(), random())
            color2 = (random(), random(), random())
            for segment in room.get_segments():
                e1, e2 = segment.End1.PntCoord, segment.End2.PntCoord
                pnt1 = Pnt(e1.x, e1.y)
                pnt2 = Pnt(e2.x, e2.y)
                c = color if pnt1.isInPolygon(room.slab_poly) else "r"
                segment.End1.plot(c, (fig, ax))
                c2 = color if pnt2.isInPolygon(room.slab_poly) else "r"
                segment.End2.plot(c2, (fig, ax))
                segment.plot(color, (fig, ax))
            room.plot(color2, figax=(fig, ax))
            # axes = ax.gca()
            ax.set_xlim([-10, 10])
            ax.set_ylim([-8, 8])
            plt.show()







    def reinit_skeletons(self):
        self.skeletonLevels = [LevelSkeleton.createSkeletonFromLevel(level) for level in self.levels]
        self.levelsHash = dict(zip(self.levels, self.skeletonLevels))
        self.skeletonLevelsHash = dict(zip(self.skeletonLevels, self.levels))
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

    def multiSearch(self):

        # def mygen2():
        #     c = {
        #         "rad_w": 1,
        #         "ecc_w": -0.5,
        #         "area_w": 1,
        #         "length_w": 1,
        #         "ratio": 1,
        #         "d": 1,
        #     }
        #     area_w = [0.1, 0.5, 1, 1.5, 2]
        #     length_w = [0.1, 0.5, 1, 1.5, 2]
        #     for aw in area_w:
        #         c['area_w'] = aw
        #         yield c
        #     c['area_w'] = 1
        #     for lw in length_w:
        #         c['length_w'] = lw
        #         yield c

        def mygenprov():
            c = {
                "rad_w": 0.1,
                "ecc_w": -1,
                "area_w": 1,
                "length_w": 1,
                "ratio": 1,
                "d": 1,
            }
            yield c

        # def mygen():
        #     c = {
        #         "rad_w": 0.5,
        #         "ecc_w": -0.5,
        #         "area_w": 1,
        #         "length_w": 1,
        #         "ratio": 1,
        #         "d": 1,
        #     }
        #     ecc_w = [-0.1]
        #     length_ratio = [1.2, 1.5, 2, 0.75, 0.5]
        #     d_ratios = [0.75, 1.25, 1.5]
        #     for w in ecc_w:
        #         c['ecc_w'] = w
        #         yield c
        #
        #     c['ecc_w'] = -0.5

        count = 1
        for consts in mygenprov():
            dirname = 'savedtry/constraints' + str(count) + '/'
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            open(dirname + 'constraints.txt', 'w').write("Torsional radius weight: " +
                                                         str(consts['rad_w']) +
                                                         "Eccentricity weight: " +
                                                         str(consts['ecc_w']) +
                                                         "\nShear Wall length weight: " +
                                                         str(consts['length_w']) +
                                                         "\nShear Wall cover area weight: " +
                                                         str(consts['area_w']))
            self.constraints = consts
            self.reinit_skeletons()
            self.solutions = {}
            for levelSkeleton in self.skeletonLevels[::-1]:
                level = self.skeletonLevelsHash[levelSkeleton]
                prevs = [self.solutions[self.levelsHash[p]].levelSkeleton for p in level.getUpperLevels()
                         if self.levelsHash[p] in self.solutions]
                print("PREVS LENGTH IS", len(prevs))
                if len(prevs):
                    levelSkeleton.copyLevelsVoiles(prevs)
                i = self.skeletonLevels.index(levelSkeleton)
                solution = search(levelSkeleton, filename="level" + str(i), constraints=self.constraints)
                self.solutions[levelSkeleton] = solution
            self.saveSkeletons(dirname)
            count += 1

    def saveSkeletons(self, root):
        for selectedRow in range(len(self.skeletonLevels)):
            lv = "level" + str(1 + selectedRow)
            froot = root + lv + '/'
            if not os.path.exists(froot):
                os.makedirs(froot)


            from matplotlib import pyplot as plt
            levelSkeleton = self.skeletonLevels[selectedRow]
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
            f.write("slab center: " + str(c1) +
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
    file = "../IFCFiles/B09_mod.ifc"
    wShapes, sShapes = createShapes(file)
    launcher = Launcher(wallShapes=wShapes, slabShapes=sShapes)
    # launcher.multiSearch()

if __name__ == '__main__':
    main()
