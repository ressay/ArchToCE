from shapely.geometry import Polygon
from shapely.ops import cascaded_union

from Geometry.Geom2D import Pnt, linestring
from Skeleton.BoxSkeleton import NotBoxError
from Skeleton.SlabSkeleton import SlabSkeleton
from Skeleton.WallSkeleton import WallSkeleton
from Skeleton.Skelet import Skelet
import math
import copy
# Add intersection of two walls same level  (axes or polygons)

class LevelSkeleton(Skelet):
    def __init__(self, walls, slab, level):
        super(LevelSkeleton, self).__init__()
        self.wallSkeletons = walls
        self.notModifiedWalls = walls
        self.slabSkeleton = slab
        self.level = level
        self.height = level.getHeightOverLowerLevel()

    @staticmethod
    def createSkeletonFromLevel(level):
        slabSkeleton = SlabSkeleton.createSkeletonFromSlab(level.slab)
        wallSkeletons = []
        lowerlevel = level.getLowerLevel()
        lowZ = None if lowerlevel is None else lowerlevel.slab.getHighestZ()
        print("for ", level, "lowz is: ", lowZ)
        if lowZ is None:
            lowZ = 0
        for wall in level.walls:
            wallSkeletons += WallSkeleton.createSkeletonsFromWall(wall,
                                                                  lowZ,
                                                                  level.slab.getLowestZ())
        # wallSkeletons = [WallSkeleton.createSkeletonFromWall(wall) for wall in level.walls]
        return LevelSkeleton(wallSkeletons, slabSkeleton, level)

    @staticmethod
    def createNewSkeletonfromLevel(level,SolutionAxes):
        slabSkeleton = SlabSkeleton.createSkeletonFromSlab(level.slab)
        wallSkeletons = []
        lowerlevel = level.getLowerLevel()
        lowZ = None if lowerlevel is None else lowerlevel.slab.getHighestZ()
        print("for ", level, "lowz is: ", lowZ)
        test=False
        if lowZ is None:
            lowZ = 0
        for axis in SolutionAxes.axes[0]:
            print("here axis",axis.coords[0][1])
        for wall in level.walls:
            wallSkeletons += WallSkeleton.createSkeletonsFromWall(wall,
                                                                  lowZ,
                                                                  level.slab.getLowestZ())
        # for wall in level.walls:
        #     wallSkeleton = WallSkeleton.createSkeletonFromWall(wall)
        #     x = round(wallSkeleton.poly.centroid().x,2)
        #     y = round(wallSkeleton.poly.centroid().y,2)

            # for axis in SolutionAxes.axes[0]:
            #     if y==axis.coords[0][1]:
            #         wallSkeletons += WallSkeleton.createSkeletonsFromWall(wall,
            #                                                               lowZ,
            #                                                               level.slab.getLowestZ())
            #         test = True
            # for axis in SolutionAxes.axes[1]:
            #     if x==axis.coords[0][0]:
            #         # print("I am here Vertical",mid,"\n",axis)
            #         wallSkeletons += WallSkeleton.createSkeletonsFromWall(wall,
            #                                                               lowZ,
            #                                                               level.slab.getLowestZ())
            #         test = True
            # if test == False: level.walls.remove(wall)
        return LevelSkeleton(wallSkeletons, slabSkeleton, level)

    def getVoileLengthNeeded(self, weight=1):
        height = self.level.heighestZ
        coeff = 1.3*weight
        if height < 30:
            coeff = 0.7*weight
        return coeff * height * self.slabSkeleton.poly.area() / 100

    def getWallsTotalLength(self):
        length = 0
        for wallSkeleton in self.wallSkeletons:
            length += wallSkeleton.vecLength.magn()
        return length

    def getVoilesTotalLength(self):
        return sum(wallSkeleton.getVoilesLength() for wallSkeleton in self.wallSkeletons)

    def getRatio(self, ratio=1):
        if self.getWallsTotalLength() == 0:
            return 1
        return self.getVoileLengthNeeded(ratio) / self.getWallsTotalLength()

    def copy(self):
        walls = [wallSkeleton.copy() for wallSkeleton in self.wallSkeletons]
        levelSkeleton = LevelSkeleton(walls, self.slabSkeleton.copy(), self.level)
        levelSkeleton.evalData = self.evalData
        return levelSkeleton

    def getCenterFromSlab(self):
        return Pnt.createPointFromShapely(self.slabSkeleton.poly.centroid())

    def getSlabArea(self):
        return self.slabSkeleton.poly.area()

    def getTorsionalRadius(self, origin):
        ssumX2Ly3 = 0
        ssumY2Lx3 = 0
        ssumLx3 = 0
        ssumLy3 = 0

        for wallSkeleton in self.wallSkeletons:
            sumLx3, sumLy3, sumX2Ly3, sumY2Lx3 = wallSkeleton.getSums2(origin)
            ssumX2Ly3 += sumX2Ly3
            ssumY2Lx3 += sumY2Lx3
            ssumLx3 += sumLx3
            ssumLy3 += sumLy3

        Rx, Ry = 0, 0
        if ssumLx3 != 0:
            Ry = math.sqrt((ssumX2Ly3 + ssumY2Lx3)/ssumLx3)
        if ssumLy3 != 0:
            Rx = math.sqrt((ssumY2Lx3 + ssumX2Ly3)/ssumLy3)
        return math.sqrt(Rx), math.sqrt(Ry)

    def getCenterFromShear(self):
        sumLiX = 0
        sumLiY = 0
        sumLixi = 0
        sumLiyi = 0

        nShears = 0
        for wallSkeleton in self.wallSkeletons:
            sLiX, sLiY, sLixi, sLiyi = wallSkeleton.getSums()
            nShears += len(wallSkeleton.getAllVoiles())
            sumLiX += sLiX
            sumLiY += sLiY
            sumLixi += sLixi
            sumLiyi += sLiyi

        x = 0
        y = 0
        if sumLiY != 0:
            x = sumLixi / sumLiY
        else:
            print("sumLiY is 0")
            if sumLiyi != 0:
                print("hummm error")
        if sumLiX != 0:
            y = sumLiyi / sumLiX
        else:
            print("sumLiX is 0")
            if sumLixi != 0:
                print("hummm error")
        cntr = Pnt(x, y)

        return cntr

    @staticmethod
    def removeUnwantedWalls(LevelSkeletons,SolutionAxes):
        for levelSkeleton in LevelSkeletons:
            newWallSkeletons = []
            # print("number of walls", len(levelSkeleton.wallSkeletons))
            for wallskeleton in levelSkeleton.wallSkeletons:
                test = False
                y = round(wallskeleton.poly.centroid().y, 2)
                x = round(wallskeleton.poly.centroid().x, 2)
                # print("here wallz ",levelSkeleton.wallSkeletons.index(wallskeleton),":",wallskeleton)
                for axis in SolutionAxes.axes[0]:
                    # print("here axis:",axis)
                    if y==axis.coords[0][1]:
                        test = True
                        newWallSkeletons.append(wallskeleton)
                        # print("added horizontal")
                for axis in SolutionAxes.axes[1]:
                    if x==axis.coords[0][0]:
                        test = True
                        newWallSkeletons.append(wallskeleton)
                # if not test: levelSkeleton.wallSkeletons.remove(wallskeleton)
            levelSkeleton.wallSkeletons = copy.deepcopy(newWallSkeletons)
            # print("new number of walls", len(levelSkeleton.wallSkeletons))
        return LevelSkeletons

    def restrictLevelUsableWalls(self, levelSkeletons):
        restrictWalls = []
        for levelSkeleton in levelSkeletons:
            toAdd = []
            upperLvlsPolys = [lvl.level.slab.getBasePolygon().poly for lvl in levelSkeletons if
                              lvl.level.getHeight() > levelSkeleton.level.getHeight()]
            upperPoly = cascaded_union(upperLvlsPolys)
            for wallSkeleton in levelSkeleton.wallSkeletons:
                intersection = wallSkeleton.poly.poly.intersection(upperPoly)
                if type(intersection) is not Polygon or intersection.area != wallSkeleton.poly.area():
                    toAdd.append(wallSkeleton)
            restrictWalls += toAdd
        resultWalls = []
        for wallSkeleton in restrictWalls:
            for wallSkeleton2 in self.wallSkeletons:
                intersection = wallSkeleton.poly.intersection(wallSkeleton2.poly)
                if intersection:
                    resultWalls.append(WallSkeleton(intersection))

        self.wallSkeletons = resultWalls

    def copyLevelsVoiles(self, levelSkeletons):
        aboveWalls = []
        for levelSkeleton in levelSkeletons:
            aboveWalls += levelSkeleton.wallSkeletons
        for wallSkeleton in aboveWalls:
            if not wallSkeleton.getVoilesLength():
                continue
            for wallSkeleton2 in self.wallSkeletons:
                intersection = wallSkeleton.poly.intersection(wallSkeleton2.poly)
                if intersection and wallSkeleton.poly.area() == intersection.area():  # test if polygons are equal
                    voiles = wallSkeleton.getAllVoiles()
                    for voileSkeleton in voiles:
                        voileSkeleton = voileSkeleton.copy()
                        voileSkeleton.setParentWall(wallSkeleton2, True)
                        wallSkeleton2.attachFixedVoile(voileSkeleton)
                    break

    def getPolys(self):
        return [wallSkeleton.poly for wallSkeleton in self.wallSkeletons]
