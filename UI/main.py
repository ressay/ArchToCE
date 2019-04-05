import sys
from OCC.Display.backend import load_backend
from PyQt4 import QtGui


import Show2DWindow
# from Optimization.Genetic import GeneticOperations2
from Geometry.Geom2D import Pnt, Ellip, Poly
from Optimization.Genetic import GeneticOperations2
from Optimization.Genetic.GeneticAlgorithm import search
from Optimization.Genetic.GeneticOperations import merge
from Optimization.Solution import Solution
from Skeleton.LevelSkeleton import LevelSkeleton
from Structures.Level import Level
from Ifc import IfcUtils
from UI import Plotter
from UI.Plotter import plotPolys

load_backend("qt-pyqt4")   #here you need to tell OCC.Display to load qt4 backend

class TryApp(QtGui.QMainWindow, Show2DWindow.Ui_MainWindow):
    model = QtGui.QStandardItemModel()
    levels = []
    skeletonLevels = []
    viewerTabs = {}
    def __init__(self, parent=None, wallShapes=None, slabShapes=None):
        super(TryApp, self).__init__(parent)
        self.setupUi(self)
        self.levels = Level.generateLevelsFromShapes(wallShapes,slabShapes)
        print("INFO INIT: DONE GENERATING LEVELS FROM SHAPES")
        self.levels.sort(key=lambda lvl: lvl.getHeight())

        self.skeletonLevels = [LevelSkeleton.createSkeletonFromLevel(level) for level in self.levels]
        self.levelsHash = dict(zip(self.levels, self.skeletonLevels))
        self.skeletonLevelsHash = dict(zip(self.skeletonLevels,self.levels))
        print("INFO INIT: DONE GENERATING LEVELSKELETONS FROM LEVELS")
        baseSlabHeight = 0
        for level in self.levels:
            print("length",len(self.levelsHash[level].getPolys()),level.getHeight())
            if not len(self.levelsHash[level].getPolys()):# or level.getHeight() <= 0:
                baseSlabHeight = level.getHeight()
            else:
                break
        print("SLAB BASE HEIGHT",baseSlabHeight)
        for i,levelSkeleton in enumerate(self.skeletonLevels):
            # if not len(levelSkeleton.getPolys()):
            #     continue
            # if not prevLevel:
            #     prevLevel = levelSkeleton
            #     # plotPolys(levelSkeleton.getPolys(),i,'first')
            #     continue
            # plotPolys(levelSkeleton.getPolys(),i+len(self.skeletonLevels),'original')

            prevLevels = self.skeletonLevelsHash[levelSkeleton].getRightLowerLevels()
            print("**LENGTH BEFORE FILTER:", len(prevLevels))
            if not prevLevels:
                continue

            prevLevels = [self.levelsHash[level] for level in prevLevels if level.getHeight() > baseSlabHeight]
            print("**NUMBER OF LEVELS: ",len(prevLevels))
            if not len(prevLevels):
                continue
            levelSkeleton.restrictLevelUsableWalls(prevLevels)
            # plotPolys(levelSkeleton.getPolys(),i)
        # plt.show()
        self.levels = [level for level in self.levels if len(self.levelsHash[level].getPolys())]
        self.skeletonLevels = [levelSkeleton for levelSkeleton in self.skeletonLevels if len(levelSkeleton.getPolys())]
        self.solutions = {}
        # for skeletonLevel in self.skeletonLevels:
        #     # print("needed ratio: " + str(skeletonLevel.getRatio()))
        #     for wallSkeleton in skeletonLevel.wallSkeletons:
        #         wallSkeleton.attachVoile(wallSkeleton.createRandomVoileFromRatio(0.5))

        self.solutions1 = [Solution.createRandomSolutionFromSkeleton2(skeletonLevel)
                           for skeletonLevel in self.skeletonLevels]
        self.solutions2 = [Solution.createRandomSolutionFromSkeleton2(skeletonLevel)
                           for skeletonLevel in self.skeletonLevels]
        # self.merged = [merge(s1, s2) for s1, s2 in zip(self.solutions1, self.solutions2)]
        # self.crossed = [cross(s1, s2) for s1, s2 in zip(self.solutions1, self.solutions2)]
        self.selectedRow = 1
        # for skeletonLevel in self.skeletonLevels:
        #     print("number of walls: " + str(len(skeletonLevel.wallSkeletons)))
        # levelSkeleton = self.skeletonLevels[1]
        # for wallSkeleton in levelSkeleton.wallSkeletons:
        #     print("length is "+str(len(wallSkeleton.attachedVoiles)))
        self.initListView()
        # self.loadFile.clicked.connect(self.browseFileCallBack)
        # self.openWin.clicked.connect(self.openWinCallBack)
        self.listView.setModel(self.model)
        self.listView.clicked.connect(self.listViewSelected)
        self.sol1.clicked.connect(self.sol1CB)
        self.sol2.clicked.connect(self.sol2CB)
        self.merge.clicked.connect(self.mergeCB)
        self.cross.clicked.connect(self.crossCB)
        self.showLower.clicked.connect(self.showLowerFun)


        self.scrollTab = QtGui.QScrollArea()

        self.tabWidget.addTab(self.scrollTab, "upperView")

        self.addViewerTab("Walls")
        self.addViewerTab("Slabs")
        self.addViewerTab("All")
        self.addViewerTab("Selected")

        self.tabWidget.removeTab(0)
        self.tabWidget.removeTab(0)

        self.setViewerDisplay("Walls",wallShapes)
        self.setViewerDisplay("Slabs",slabShapes)
        all = wallShapes+slabShapes
        self.setViewerDisplay("All",all)
        self.pend = True

    def sol1CB(self):
        print "s1: " + str(self.solutions1[self.selectedRow].getFitness())
        polys = self.getPolygonsFromLevelSkeletons(self.solutions1[self.selectedRow].levelSkeleton)
        self.draw(polys)

    def sol2CB(self):
        print "s2: " + str(self.solutions2[self.selectedRow].getFitness())
        polys = self.getPolygonsFromLevelSkeletons(self.solutions2[self.selectedRow].levelSkeleton)
        self.draw(polys)

    def showLowerFun(self):
        if self.selectedRow is not None:
            from matplotlib import pyplot as plt
            levelSkeleton = self.skeletonLevels[self.selectedRow]
            if levelSkeleton in self.solutions:
                levelSkeleton = self.solutions[levelSkeleton].levelSkeleton
            polys,colors = self.getPolygonsFromLevelSkeletons(levelSkeleton)
            colors = [[c.red()/255.,c.green()/255.,c.blue()/255.,0.8] for c in colors]
            c = colors[-1]
            print('COLOR IN SHOW LOWER IS: ',c[0],c[1],c[2])
            Plotter.plotPolys(polys,self.selectedRow,"plan",colors)
            polys = [poly.poly for poly in polys]
            alphas = [1 for poly in polys]
            boxes = [voileSkeleton.getSurrondingBox()
                     for wallSkeleton in levelSkeleton.wallSkeletons
                     for voileSkeleton in wallSkeleton.getAllVoiles()]
            colors += [[0.5,1,0.5] for box in boxes]
            polys += boxes
            alphas += [0.2 for poly in boxes]
            Plotter.plotShapely(polys,colors,alphas,20)
            plt.show()
            # self.draw(polys)

    def mergeCB(self):
        prev = None
        for levelSkeleton in self.skeletonLevels[::-1]:
            level = self.skeletonLevelsHash[levelSkeleton]
            prevs = [self.solutions[self.levelsHash[p]].levelSkeleton for p in level.getUpperLevels()
                     if self.levelsHash[p] in self.solutions]
            print("PREVS LENGTH IS",len(prevs))
            if len(prevs):
                levelSkeleton.copyLevelsVoiles(prevs)
            i = self.skeletonLevels.index(levelSkeleton)
            solution = search(levelSkeleton,filename="level"+str(i))
            self.solutions[levelSkeleton] = solution
            self.drawSkeleton(levelSkeleton)

    def crossCB(self):

        s1 = self.solutions1[self.selectedRow]
        s2 = self.solutions2[self.selectedRow]
        s,b = GeneticOperations2.cross(s1,s2)
        # print "s fitness: " + str(s.getFitness())
        polys = self.getPolygonsFromLevelSkeletons(s.levelSkeleton)
        self.draw(polys)

    def addViewerTab(self,name):
        from OCC.Display import qtDisplay
        self.viewerTabs[name] = qtDisplay.qtViewer3d(self)
        self.tabWidget.addTab(self.viewerTabs[name],name)
        self.viewerTabs[name].InitDriver()

    def setViewerDisplay(self,name,shapes):
        display = self.viewerTabs[name]._display
        display.EraseAll()
        self.initDisplayer(display,shapes)


    def initDisplayer(self,display,shapes):
        for shape in shapes:
            display.DisplayShape(shape)

    def initListView(self):
        i = 0
        for level in self.skeletonLevels:
            item = QtGui.QStandardItem("level " + str(i))
            i += 1
            self.model.appendRow(item)

    def getPolygonsFromLevels(self,levels):
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

        colors += [QtGui.QColor(255,0,0)
                   for wallSkeleton in levelSkeleton.wallSkeletons
                   for voileSkeleton in wallSkeleton.getAllVoiles()]
        if not len(polygons):
            return
        polys = (polygons,colors)
        center = Pnt.createPointFromShapely(levelSkeleton.slabSkeleton.poly.centroid())
        return polys
        # ellipses = ([Ellip(center, 0.5)], [QtGui.QColor(0, 255, 0)])
        # self.draw(polys,ellipses)


    def draw(self,polys=None,ellipses=None):
        from UI.DrawUtils import Window
        self.scrollTab.setWidget(Window(polys,ellipses=ellipses, rect=self.scrollTab.geometry()))

    def drawPolygons(self,shapes):
        from Geometry import ShapeToPoly
        polygons = ShapeToPoly.getShapesBasePolygons(shapes)
        if not len(polygons):
            return

        from UI.DrawUtils import Window
        self.scrollTab.setWidget(Window(polygons,rect=self.scrollTab.geometry()))

    def drawSkeleton(self,levelSkeleton):

        ellipses = []
        if levelSkeleton in self.solutions:
            solution = self.solutions[levelSkeleton]
            polys = self.getPolygonsFromLevelSkeletons(solution.levelSkeleton)
            c1 = solution.levelSkeleton.getCenterFromSlab()
            c2 = solution.levelSkeleton.getCenterFromShear()
            e1 = Ellip(c1, 0.4)
            e2 = Ellip(c2, 0.4)
            ells = [e1, e2]
            for box in solution.getValidVoilesBoxes():
                polys[0].append(Poly([Pnt(pnt[0], pnt[1]) for pnt in box.exterior.coords]))
                q1 = QtGui.QColor(0, 255, 0)
                q1.setAlpha(20)
                polys[1].append(q1)

            for box in solution.getNonValidVoilesBoxes():
                polys[0].append(Poly([Pnt(pnt[0], pnt[1]) for pnt in box.exterior.coords]))
                q1 = QtGui.QColor(255, 0, 0)
                q1.setAlpha(20)
                polys[1].append(q1)
        else:
            polys = self.getPolygonsFromLevelSkeletons(levelSkeleton)
        self.draw(polys, ellipses)


    def listViewSelected(self, index):
        self.selectedRow = row = index.row()
        # print ('selected item index found at %s with data: %s' % (index.row(), index.data().toString()))
        shapes = [wall.shape for wall in self.levels[row].walls]
        # self.drawPolygons(shapes)
        # polys = self.getPolygonsFromLevelSkeletons(self.skeletonLevels[row])
        self.drawSkeleton(self.skeletonLevels[row])
        shapes.append(self.levels[row].slab.shape)
        self.setViewerDisplay("Selected",shapes)







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

    return wShapes,sShapes

def main():
    file = "../IFCFiles/Immeuble39.ifc"
    wShapes,sShapes = createShapes(file)
    app = QtGui.QApplication(sys.argv)
    form = TryApp(wallShapes=wShapes,slabShapes=sShapes)
    form.show()
    app.exec_()

if __name__ == '__main__':

    main()
