import os
import sys
from random import random

from OCC.Display.backend import load_backend
from PyQt5 import QtGui, QtWidgets   # change was here
import UI.Show2DWindow as Show2DWindow
# from Optimization.Genetic import GeneticOperations2
from Geometry.Geom2D import Pnt, Ellip, Poly
from Ifc.IfcUtils import getSpaceShapesFromIfc
from Optimization.Genetic import GeneticOperations2
from Optimization.Genetic.GeneticAlgorithm import search
from Skeleton.LevelSkeleton import LevelSkeleton
from Skeleton.WallSkeleton import WallSkeleton
from Skeleton.StoreySkeleton import StoreySkeleton
from Structures.Level import Level
from Ifc import IfcUtils
from UI import Plotter
from shapely.geometry import Point
load_backend("qt-pyqt5")  # here you need to tell OCC.Display to load qt5 backend


class TryApp(QtWidgets.QMainWindow, Show2DWindow.Ui_MainWindow):
    model = QtGui.QStandardItemModel()
    levels = []
    skeletonLevels = []
    viewerTabs = {}

    def __init__(self, parent=None, wallShapes=None, slabShapes=None, spaceShapes=None):
        super(TryApp, self).__init__(parent)
        self.constraints = {
            "ecc_w": -0.5,
            "area_w": 1,
            "length_w": 1,
            "ratio": 1,
            "d": 1,
        }
        self.solutions = {}
        self.selectedRow = 1
        self.storey_mode = False
        self.storeySkeletons = []

        self.setupUi(self)
        self.levels = Level.generateLevelsFromShapes(wallShapes, slabShapes)
        print("INFO INIT: DONE GENERATING LEVELS FROM SHAPES")
        self.levels.sort(key=lambda lvl: lvl.getHeight())


        self.init_skeletons()
        # self.skeletonLevels = [LevelSkeleton.createSkeletonFromLevel(level) for level in self.levels]
        # self.levelsHash = dict(list(zip(self.levels, self.skeletonLevels)))
        # self.skeletonLevelsHash = dict(list(zip(self.skeletonLevels, self.levels)))
        # print("INFO INIT: DONE GENERATING LEVELSKELETONS FROM LEVELS")
        # baseSlabHeight = 0
        # for level in self.levels:
        #     if not len(self.levelsHash[level].getPolys()):  # or level.getHeight() <= 0:
        #         baseSlabHeight = level.getHeight()
        #     else:
        #         break
        #
        # print(("getting lower levels", len(self.skeletonLevels)))
        # for i, levelSkeleton in enumerate(self.skeletonLevels):
        #     prevLevels = self.skeletonLevelsHash[levelSkeleton].getRightLowerLevels()
        #     print(("getting for level", i))
        #     if not prevLevels:
        #         continue
        #
        #     prevLevels = [self.levelsHash[level] for level in prevLevels if level.getHeight() > baseSlabHeight]
        #     if not len(prevLevels):
        #         continue
        #     levelSkeleton.restrictLevelUsableWalls(prevLevels)
        #
        # self.levels = [level for level in self.levels if len(self.levelsHash[level].getPolys())]
        # for level in self.levels:
        #     level.relatedLevels = self.levels
        #
        # self.skeletonLevels = [levelSkeleton for levelSkeleton in self.skeletonLevels if len(levelSkeleton.getPolys())]


        heights = []

        for levelSkeleton in self.skeletonLevels:
            height = levelSkeleton.level.getHeight()
            if height not in heights:
                skeletons = []
                heights.append(height)
                for ls in self.skeletonLevels:
                    if ls.level.getHeight() == height:
                        skeletons.append(ls)

                self.storeySkeletons.append(StoreySkeleton(skeletons))

        self.initListView(self.storey_mode)
        self.listView.setModel(self.model)
        self.listView.clicked.connect(self.listViewSelected)
        self.sol1.clicked.connect(self.sol1CB)
        self.sol2.clicked.connect(self.sol2CB)
        self.merge.clicked.connect(self.mergeCB)
        self.cross.clicked.connect(self.crossCB)
        self.showLower.clicked.connect(self.showLowerFun)

        self.scrollTab = QtWidgets.QScrollArea()

        self.tabWidget.addTab(self.scrollTab, "upperView")

        self.addViewerTab("Walls")
        self.addViewerTab("Slabs")
        self.addViewerTab("All")
        self.addViewerTab("Selected")

        self.tabWidget.removeTab(0)
        self.tabWidget.removeTab(0)

        self.setViewerDisplay("Walls", wallShapes)
        self.setViewerDisplay("Slabs", slabShapes)
        all = wallShapes + slabShapes
        self.setViewerDisplay("All", all)
        self.pend = True

    def init_skeletons(self):
        self.skeletonLevels = [LevelSkeleton.createSkeletonFromLevel(level) for level in self.levels]
        self.levelsHash = dict(list(zip(self.levels, self.skeletonLevels)))
        self.skeletonLevelsHash = dict(list(zip(self.skeletonLevels, self.levels)))
        print(self.levels)
        print(self.skeletonLevels)
        self.levels = [level for level in self.levels if len(self.levelsHash[level].getPolys())]
        for level in self.levels:
            level.relatedLevels = self.levels
        self.skeletonLevels = [levelSkeleton for levelSkeleton in self.skeletonLevels if len(levelSkeleton.getPolys())]

        print("INFO INIT: DONE GENERATING LEVELSKELETONS FROM LEVELS")
        baseSlabHeight = 0
        for level in self.levels:
            if not len(self.levelsHash[level].getPolys()):  # or level.getHeight() <= 0:
                baseSlabHeight = level.getHeight()
            else:
                break

        print(baseSlabHeight)

        for i, levelSkeleton in enumerate(self.skeletonLevels):
            prevLevels = self.skeletonLevelsHash[levelSkeleton].getRightLowerLevels()

            if not prevLevels:
                continue

            prevLevels = [self.levelsHash[level] for level in prevLevels if level.getHeight() >= baseSlabHeight]
            print(prevLevels)
            if not len(prevLevels):
                continue
            levelSkeleton.restrictLevelUsableWalls(prevLevels)


        self.solutions = {}

    def sol1CB(self):
        print(("s1: " + str(self.solutions1[self.selectedRow].getFitness())))
        polys = self.getPolygonsFromLevelSkeletons(self.solutions1[self.selectedRow].levelSkeleton)
        self.draw(polys)

    def sol2CB(self):
        print(("s2: " + str(self.solutions2[self.selectedRow].getFitness())))
        polys = self.getPolygonsFromLevelSkeletons(self.solutions2[self.selectedRow].levelSkeleton)
        self.draw(polys)

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

            polys += boxes
            alphas += [0.2 for poly in boxes]

            Plotter.plotShapely(polys, colors, alphas, 20)

            wallSkeletons = levelSkeleton.wallSkeletons
            axes = WallSkeleton.createAxes(wallSkeletons)[0]
            axes += WallSkeleton.createAxes(wallSkeletons)[1]
            for axe in axes:
                plt.plot(*axe.xy)
            print("AXXXXXXXXXES", axes)


            plt.show()
            # plt.savefig('try2.png', bbox_inches='tight')
            # self.draw(polys)

    def multiSearch(self):

        def mygen2():
            c = {
                "rad_w": 1,
                "ecc_w": -0.5,
                "area_w": 1,
                "length_w": 1,
                "ratio": 1,
                "d": 1,
            }
            area_w = [0.1, 0.5, 1, 1.5, 2]
            length_w = [0.1, 0.5, 1, 1.5, 2]
            for aw in area_w:
                c['area_w'] = aw
                yield c
            c['area_w'] = 1
            for lw in length_w:
                c['length_w'] = lw
                yield c

        def mygenprov():
            c = {
                "rad_w": 0,
                "ecc_w": -0.5,
                "area_w": 2,
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
            area_w = [1.5, 2, 3, 4, 10]
            d_ratios = [0.25, 0.5, 0.75]
            for d in d_ratios:
                c['d'] = d
                for w in area_w:
                    c['area_w'] = w
                    yield c
                    break
                break

        count = 1
        for consts in mygenprov():
            dirname = 'savedWrong/constraints' + str(count) + '/'
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
            self.init_skeletons()
            self.solutions = {}
            for levelSkeleton in self.skeletonLevels[::-1]:
                level = self.skeletonLevelsHash[levelSkeleton]
                prevs = [self.solutions[self.levelsHash[p]].levelSkeleton for p in level.getUpperLevels()
                         if self.levelsHash[p] in self.solutions]
                print(("PREVS LENGTH IS", len(prevs)))
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

    def mergeCB(self):
        self.multiSearch()
        # self.solutions = {}
        # for levelSkeleton in self.skeletonLevels[::-1]:
        #     level = self.skeletonLevelsHash[levelSkeleton]
        #     prevs = [self.solutions[self.levelsHash[p]].levelSkeleton for p in level.getUpperLevels()
        #              if self.levelsHash[p] in self.solutions]
        #     print("PREVS LENGTH IS",len(prevs))
        #     if len(prevs):
        #         levelSkeleton.copyLevelsVoiles(prevs)
        #     i = self.skeletonLevels.index(levelSkeleton)
        #     solution = search(levelSkeleton,filename="level"+str(i), constraints=self.constraints)
        #     self.solutions[levelSkeleton] = solution
        #     self.drawSkeleton(levelSkeleton)

    def crossCB(self):

        s1 = self.solutions1[self.selectedRow]
        s2 = self.solutions2[self.selectedRow]
        s, b = GeneticOperations2.cross(s1, s2)
        # print "s fitness: " + str(s.getFitness())
        polys = self.getPolygonsFromLevelSkeletons(s.levelSkeleton)
        self.draw(polys)

    def addViewerTab(self, name):
        from OCC.Display import qtDisplay
        self.viewerTabs[name] = qtDisplay.qtViewer3d(self)
        self.tabWidget.addTab(self.viewerTabs[name], name)
        self.viewerTabs[name].InitDriver()

    def setViewerDisplay(self, name, shapes):
        display = self.viewerTabs[name]._display
        display.EraseAll()
        self.initDisplayer(display, shapes)

    def initDisplayer(self, display, shapes):
        for shape in shapes:
            display.DisplayShape(shape)

    def initListView(self, storey_mode):
        i = 0
        if not storey_mode:
            for level in self.skeletonLevels:
                item = QtGui.QStandardItem("level " + str(i))
                i += 1
                self.model.appendRow(item)
        else:
            for storey in self.storeySkeletons:
                item = QtGui.QStandardItem("storey " + str(i))
                i += 1
                self.model.appendRow(item)

    def getPolygonsFromLevels(self, levels):
        polys = []
        for level in levels:
            polys += self.getPolygonsFromLevelSkeletons(
                LevelSkeleton.createSkeletonFromLevel(level))
        return polys

    def getPolygonsFromLevelSkeletons(self, levelSkeleton):
        polygons = [wallSkeleton.poly.copy() for wallSkeleton in levelSkeleton.wallSkeletons]
        colors = [QtGui.QColor(220, 220, 220) for wallSkeleton in levelSkeleton.wallSkeletons]
        polygons += [voileSkeleton.poly.copy()
                     for wallSkeleton in levelSkeleton.wallSkeletons
                     for voileSkeleton in wallSkeleton.getAllVoiles()]

        colors += [QtGui.QColor(255, 0, 0)
                   for wallSkeleton in levelSkeleton.wallSkeletons
                   for voileSkeleton in wallSkeleton.getAllVoiles()]
        if not len(polygons):
            return
        polys = (polygons, colors)
        # center = Pnt.createPointFromShapely(levelSkeleton.slabSkeleton.poly.centroid())
        return polys
        # ellipses = ([Ellip(center, 0.5)], [QtGui.QColor(0, 255, 0)])
        # self.draw(polys,ellipses)

    def draw(self, polys=None, ellipses=None):
        from UI.DrawUtils import Window
        self.scrollTab.setWidget(Window(polys, ellipses=ellipses, rect=self.scrollTab.geometry()))

    def drawPolygons(self, shapes):
        from Geometry import ShapeToPoly
        polygons = ShapeToPoly.getShapesBasePolygons(shapes)
        if not len(polygons):
            return

        from UI.DrawUtils import Window
        self.scrollTab.setWidget(Window(polygons, rect=self.scrollTab.geometry()))

    def drawSkeleton(self, levelSkeleton):

        ellipses = []
        if levelSkeleton in self.solutions:
            solution = self.solutions[levelSkeleton]
            polys = self.getPolygonsFromLevelSkeletons(solution.levelSkeleton)
            c1 = solution.levelSkeleton.getCenterFromSlab()
            c2 = solution.levelSkeleton.getCenterFromShear()
            print(("point in draw: ", str(c2)))
            print(("point in draw2: ", str(c1)))
            e1 = Ellip(c1, 0.4)
            e2 = Ellip(c2, 0.4)
            ells = [e1, e2]
            ellipses = [ells, [QtGui.QColor(255, 0, 0), QtGui.QColor(0, 255, 0)]]
            for box in solution.getValidVoilesBoxes(self.constraints['d']):
                polys[0].append(Poly([Pnt(pnt[0], pnt[1]) for pnt in box.exterior.coords]))
                q1 = QtGui.QColor(0, 255, 0)
                q1.setAlpha(20)
                polys[1].append(q1)

            for box in solution.getNonValidVoilesBoxes(self.constraints['d']):
                polys[0].append(Poly([Pnt(pnt[0], pnt[1]) for pnt in box.exterior.coords]))
                q1 = QtGui.QColor(255, 0, 0)
                q1.setAlpha(20)
                polys[1].append(q1)
        else:
            polys = self.getPolygonsFromLevelSkeletons(levelSkeleton)
            if self.storey_mode:
                polys[0].extend([lvlSkel.slabSkeleton.poly.copy() for lvlSkel in levelSkeleton.levelSkeletons])
                for _ in levelSkeleton.levelSkeletons:
                    q1 = QtGui.QColor(random()*255, random()*255, random()*255)
                    q1.setAlpha(20)
                    polys[1].append(q1)
            else:
                polys[0].append(levelSkeleton.slabSkeleton.poly.copy())
                q1 = QtGui.QColor(random() * 255, random() * 255, random() * 255)
                q1.setAlpha(20)
                polys[1].append(q1)
        self.draw(polys, ellipses)

    def listViewSelected(self, index):
        if not self.storey_mode:
            self.selectedRow = row = index.row()
            # print ('selected item index found at %s with data: %s' % (index.row(), index.data().toString()))
            shapes = [wall.shape for wall in self.levels[row].walls]
            # self.drawPolygons(shapes)
            # polys = self.getPolygonsFromLevelSkeletons(self.skeletonLevels[row])
            self.drawSkeleton(self.skeletonLevels[row])
            shapes.append(self.levels[row].slab.shape)
            self.setViewerDisplay("Selected", shapes)
        else:
            self.selectedRow = row = index.row()
            # print ('selected item index found at %s with data: %s' % (index.row(), index.data().toString()))
            shapes = [wall.shape for wall in self.storeySkeletons[row].walls]
            # self.drawPolygons(shapes)
            # polys = self.getPolygonsFromLevelSkeletons(self.skeletonLevels[row])
            self.drawSkeleton(self.storeySkeletons[row])
            shapes += [l.slab.shape for l in self.storeySkeletons[row].levels]
            self.setViewerDisplay("Selected", shapes)


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
    file = "../IFCFiles/villa2.ifc"
    wShapes, sShapes = createShapes(file)
    space_shapes = getSpaceShapesFromIfc(file)
    space_shapes = [s for _, s in space_shapes]
    app = QtWidgets.QApplication(sys.argv)
    form = TryApp(wallShapes=wShapes, slabShapes=sShapes, spaceShapes=space_shapes)
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
