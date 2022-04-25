from shapely.geometry import Polygon
from shapely.ops import cascaded_union
from Geometry import ShapeToPoly
from Geometry.Geom2D import Pnt, linestring, Poly
from Skeleton.BoxSkeleton import NotBoxError
from Skeleton.SlabSkeleton import SlabSkeleton
from Skeleton.VoileSkeleton import VoileSkeleton
from Skeleton.WallSkeleton import WallSkeleton
from Skeleton.Skelet import Skelet
from Skeleton.VoileSkeleton import VoileSkeleton
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

    @staticmethod
    def CreateColumnShapes(distances, TotalHeight, Columns):
        ColumnPolys = []
        Vlen = 0
        Hlen = 0
        for i in range(len(Columns)):
            cx = Columns[i].x
            cy = Columns[i].y
            Hdim, Vdim = LevelSkeleton.GetColumnDimensions(distances[0][i], distances[1][i], TotalHeight)
            if Hdim > Vdim:
                Hlen += Hdim
            else:
                Vlen += Vdim
            print("Column n°:", i, "maxDim", max(Hdim, Vdim))
            pnt1 = (round(cx - Hdim / 2, 2), round(cy - Vdim / 2, 2))
            pnt2 = (round(cx + Hdim / 2, 2), round(cy - Vdim / 2, 2))
            pnt3 = (round(cx + Hdim / 2, 2), round(cy + Vdim / 2, 2))
            pnt4 = (round(cx - Hdim / 2, 2), round(cy + Vdim / 2, 2))
            ColumnPoly = Polygon([pnt1, pnt2, pnt3, pnt4])
            ColumnPolys.append(ColumnPoly)
        Len = Vlen + Hlen
        return ColumnPolys, Len

    @staticmethod
    def GetColumnDimensions(Hdist, Vdist, Height):
        Hdim = 0
        Vdim = 0
        if 3 <= Hdist <= 4.5: Hdim = 0.3
        if 4.5 < Hdist <= 6: Hdim = 0.45
        if 6 < Hdist <= 7.5: Hdim = 0.6
        if 7.5 < Hdist <= 9: Hdim = 0.75
        if 9 < Hdist <= 10.5: Hdim = 0.9
        if 10.5 < Hdist <= 12: Hdim = 1.05

        if 3 <= Vdist <= 4.5: Vdim = 0.3
        if 4.5 < Vdist <= 6: Vdim = 0.45
        if 6 < Vdist <= 7.5: Vdim = 0.6
        if 7.5 < Vdist <= 9: Vdim = 0.75
        if 9 < Vdist <= 10.5: Vdim = 0.9
        if 10.5 < Vdist <= 12: Vdim = 1.05

        if 3 <= Height <= 6:
            Hdim = Hdim + 0.05
            Vdim = Vdim + 0.05
        if 6 < Height <= 9:
            Hdim = Hdim + 0.1
            Vdim = Vdim + 0.1
        if 9 < Height <= 12:
            Hdim = Hdim + 0.15
            Vdim = Vdim + 0.15
        if 12 <= Height <= 17:
            Hdim = Hdim + 0.2
            Vdim = Vdim + 0.2

        return Hdim, Vdim

    def getVoileLengthNeeded(self, weight=1, ColumnsLength=0):
        # height = self.level.heighestZ
        # coeff = 1.3*weight
        # if height < 30:
        #     coeff = 0.7*weight
        #     print("here coef2",coeff)
        # return coeff * height * self.slabSkeleton.poly.area() / 100

        Height = self.level.getHeightOverLowerLevel()+0.3
        D = 1.5*Height
        neededLength = 0.2*self.slabSkeleton.poly.area()/3-D
        # print("here area",self.slabSkeleton.poly.area())
        # print("NEEEEDED",neededLength)
        # if neededLength < 0.8: neededLength = 0.8
        # (0.125 * self.slabSkeleton.poly.area() / 2.4) - 1
        return 3

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
        # for wallSkeleton in self.wallSkeletons:
        #     if wallSkeleton.iscolumnParent:print("it is a column in here")
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
    def removeUnwantedWalls(LevelSkeletons,SolutionAxes,Columns):
        for levelSkeleton in LevelSkeletons:
            newWallSkeletons1 = []
            newWallSkeletons4 = []
            print("number of level", LevelSkeletons.index(levelSkeleton))
            for wallskeleton in levelSkeleton.wallSkeletons:
                y = round(wallskeleton.poly.centroid().y, 2)
                x = round(wallskeleton.poly.centroid().x, 2)
                print("here wall ",levelSkeleton.wallSkeletons.index(wallskeleton),":",x,y)
                for axis in SolutionAxes.axes[0]:
                    # print("here axis:",axis)
                    if y==axis.coords[0][1] :
                        newWallSkeletons1.append(wallskeleton)
                        # print("added horizontal")
                for axis in SolutionAxes.axes[1]:
                    if x==axis.coords[0][0] :
                        newWallSkeletons1.append(wallskeleton)
                # if not test: levelSkeleton.wallSkeletons.remove(wallskeleton)
            for wallsklt in LevelSkeleton.removeColumnIntersections(newWallSkeletons1,Columns):
                newWallSkeletons4.append(wallsklt)

            for Column in Columns:
                pnts = Column.exterior.coords
                Pnts = []
                for i in range(len(pnts)): Pnts.append(Pnt(pnts[i][0], pnts[i][1]))
                wall = Poly(Pnts)
                wallsklt = WallSkeleton.createSkeletonFromPoly(wall)
                wallsklt.iscolumnParent = True
                newWallSkeletons4.append(wallsklt)

            NewWallSkeletons = []
            for wall in newWallSkeletons4:
                if wall not in NewWallSkeletons: NewWallSkeletons.append(wall)
            levelSkeleton.wallSkeletons = copy.deepcopy(NewWallSkeletons)


        return LevelSkeletons
    @staticmethod
    def removeColumnIntersections(newWallSkeletons1,Columns):
        newWallSkeletons3 = []
        newWallSkeletons33=copy.deepcopy(newWallSkeletons1)
        newWallSkeletons = []
        toRemove = []
        for column in Columns:
            pnts = column.exterior.coords
            Pnts = []
            for i in range(len(pnts)): Pnts.append(Pnt(pnts[i][0], pnts[i][1]))
            ColumnWall = Poly(Pnts)
            for i in range(len(newWallSkeletons33)):
                wallskeleton = newWallSkeletons33[i]
                poly = wallskeleton.poly
                if poly.intersects(ColumnWall):
                    if poly.intersection(ColumnWall).area() == poly.area():toRemove.append(wallskeleton)
                    if poly.intersection(ColumnWall).area()!= poly.area():
                        wallsklts = LevelSkeleton.wallskeletonfromDif(poly,ColumnWall)
                        newWallSkeletons33[i] = wallsklts[0]
                        newWallSkeletons3.append(wallsklts[0])
                        if len(wallsklts) == 2:
                            newWallSkeletons33.append(wallsklts[1])
                            newWallSkeletons3.append(wallsklts[1])
        todelete = []
        for column in Columns:
            pnts = column.exterior.coords
            Pnts = []
            for i in range(len(pnts)): Pnts.append(Pnt(pnts[i][0], pnts[i][1]))
            ColumnWall = Poly(Pnts)
            for i in range(len(newWallSkeletons3)):
                wallskeleton = newWallSkeletons3[i]
                poly = wallskeleton.poly
                if poly.intersects(ColumnWall):
                    intersection=poly.intersection(ColumnWall)
                    if intersection != None:
                        todelete.append(wallskeleton)

        for elmt in toRemove:
            if elmt in newWallSkeletons33: newWallSkeletons33.remove(elmt)
        for elmnt in newWallSkeletons33:
            if elmnt not in newWallSkeletons: newWallSkeletons.append(elmnt)
        for elmt in newWallSkeletons3:
            if elmt not in newWallSkeletons: newWallSkeletons.append(elmt)
        for wall in todelete:
            if wall in newWallSkeletons: newWallSkeletons.remove(wall)
        return newWallSkeletons

    @staticmethod
    def wallskeletonfromDif(poly,ColumnWall):
        newWallSkeletons = []
        polys = poly.difference(ColumnWall)
        if polys.geom_type == 'Polygon':
            pnts = polys.exterior.coords
            Pnts = []
            for i in range(len(pnts)): Pnts.append(Pnt(pnts[i][0], pnts[i][1]))
            polygon = Poly(Pnts)
            if polygon.area() > 0:
                newWallSkeletons.append(LevelSkeleton.Addnewpolys(polygon))
        if polys.geom_type == "MultiPolygon":
            polygons = polys.geoms
            for Polys in polygons:
                pnts = Polys.exterior.coords
                Pnts = []
                for i in range(len(pnts)): Pnts.append(Pnt(pnts[i][0], pnts[i][1]))
                polygon = Poly(Pnts)
                if polygon.area() > 0:
                    newWallSkeletons.append(LevelSkeleton.Addnewpolys(polygon))
        return newWallSkeletons

    @staticmethod
    def Addnewpolys(polygon):
        newwallsklt = WallSkeleton.createSkeletonFromPoly(polygon)
        return newwallsklt

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

    def addColumnsAsVoiles(self, ColumnsVoileSkeletons):
        ColumnVoiles = 0
        for wallSkeleton2 in self.wallSkeletons:
            X = round(wallSkeleton2.poly.centroid().x, 2)
            Y = round(wallSkeleton2.poly.centroid().y, 2)
            A = wallSkeleton2.poly.MaxCoords()
            B = wallSkeleton2.poly.MinCoords()
            voiles = ColumnsVoileSkeletons
            for voileSkeleton in voiles:
                x = round(voileSkeleton.poly.centroid().x,2)
                y = round(voileSkeleton.poly.centroid().y,2)
                if x==X :
                    if y == Y:
                        wallSkeleton2.attachFixedVoile(voileSkeleton)
            ColumnVoiles += len(wallSkeleton2.getAllVoiles())
            voiles = wallSkeleton2.getAllVoiles()


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

    def ScoreOfUnacceptableVoiles(self):
        VoileSkeletons = [[],[],[]]
        # print('1',VoileSkeletons)
        ColumnWalls = []
        N=0
        for wallSkeleton in self.wallSkeletons:
            if wallSkeleton.iscolumnParent:
                ColumnWalls.append(wallSkeleton)
            else:
                for VoileSkeleton in wallSkeleton.getAllVoiles():
                    VoileSkeletons[0].append(VoileSkeleton)
                    VoileSkeletons[1].append(wallSkeleton.getAllVoiles().index(VoileSkeleton))
                    VoileSkeletons[2].append(self.wallSkeletons.index(wallSkeleton))
        # print('1', VoileSkeletons)
        AllElements = ColumnWalls + VoileSkeletons[0]
        problemwallsInds = [[],[],[]]
        if len(VoileSkeletons[0]):
            for VoileS in VoileSkeletons[0]:
                test = False
                CurrentCenter = VoileS.poly.centroid()
                leftDists = []
                rightDists = []
                ind = VoileSkeletons[0].index(VoileS)
                if VoileS.getLengthX() != 0:  # Horizontal=> same Y
                    # print('2', VoileS)
                    for element in AllElements:
                        eleCenter = element.poly.centroid()
                        eleWidth = element.poly.MaxCoords().x()-element.poly.MinCoords().x()
                        Vwidth = VoileS.poly.MaxCoords().x()-VoileS.poly.MinCoords().x()
                        if type(VoileS) != type(element):
                            test = True
                        elif VoileS != element : test = True
                        if test :
                            if round(CurrentCenter.y, 2) == round(eleCenter.y, 2):

                                dist = round(CurrentCenter.x, 2)-round(eleCenter.x, 2)-(eleWidth+Vwidth)/2
                                if dist > 0: leftDists.append(abs(dist))
                                else : rightDists.append(abs(dist))

                    if len(leftDists):
                        # print('22', VoileS)
                        if 0.1<min(leftDists)<2 :
                            N+=1
                            if ind not in problemwallsInds[0]:
                                problemwallsInds[0].append(ind)
                                problemwallsInds[1].append(VoileSkeletons[1][ind])
                                problemwallsInds[2].append(VoileSkeletons[2][ind])
                    if len(rightDists):
                        # print('222', VoileS)
                        if 0.1<min(rightDists)<2 :
                            N+=1
                            if ind not in problemwallsInds[0]:
                                problemwallsInds[0].append(ind)
                                problemwallsInds[1].append(VoileSkeletons[1][ind])
                                problemwallsInds[2].append(VoileSkeletons[2][ind])
                if VoileS.getLengthY() != 0:  # Vertical=> same X
                    DownDists = []
                    UpDists = []
                    # print('3', VoileS)
                    for element in AllElements:
                        eleCenter = element.poly.centroid()
                        eleHeight = element.poly.MaxCoords().y()-element.poly.MinCoords().y()
                        Vheight = VoileS.poly.MaxCoords().y()-VoileS.poly.MinCoords().y()
                        if type(VoileS) != type(element):
                            test = True
                        elif VoileS != element:
                            test = True
                        if test:
                            if round(CurrentCenter.x, 2) == round(eleCenter.x, 2):

                                dist = round(CurrentCenter.y, 2)-round(eleCenter.y, 2)-(eleHeight+Vheight)/2
                                if dist > 0: DownDists.append(abs(dist))
                                else : UpDists.append(abs(dist))
                    ind = VoileSkeletons[0].index(VoileS)
                    if len(DownDists):
                        # print('2', VoileS)
                        if 0.1<min(DownDists)<2 :
                            N+=1
                            if ind not in problemwallsInds[0]:
                                problemwallsInds[0].append(ind)
                                problemwallsInds[1].append(VoileSkeletons[1][ind])
                                problemwallsInds[2].append(VoileSkeletons[2][ind])
                    if len(UpDists):
                        if 0.1<min(UpDists)<2 :
                            N+=1
                            if ind not in problemwallsInds[0]:
                                problemwallsInds[0].append(ind)
                                problemwallsInds[1].append(VoileSkeletons[1][ind])
                                problemwallsInds[2].append(VoileSkeletons[2][ind])

            # for sVoile in VoileSkeletons:
            #     if not VoileS.TouchesColumn(ColumnWalls=ColumnWalls): N +=1
            return 1 - N/(2*len(VoileSkeletons)), problemwallsInds
        else: return 0, [[], [], []]
