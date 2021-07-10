import random
import math
import pandas as pd
import numpy
from shapely.geometry import linestring, Point, Polygon
from Geometry import ShapeToPoly
from Geometry.Geom2D import Pnt, Poly
from Skeleton.BoxSkeleton import BoxSkeleton, NotBoxError
from Skeleton.VoileSkeleton import VoileSkeleton
from UI import Plotter


class WallSkeleton(BoxSkeleton):
    discreteFactor = 0.1  # each 0.1 m
    miniVoileLength = 0.8
    maxVoileLength = 4
    optimumVoileLength = 2.5
    startFromZeroProba = 0.7

    # attachedVoiles = []
    def __init__(self, poly, pnts=None):
        super(WallSkeleton, self).__init__(poly, pnts)
        self.attachedVoiles = []
        self.fixedVoiles = []
        self.sums = None
        self.sums2 = None
        self.iscolumnParent = False

    @staticmethod
    def createSkeletonFromWall(wall):
        return WallSkeleton(wall.getBasePolygon())

    @staticmethod
    def createSkeletonFromPoly(ply):
        return WallSkeleton(ply)

    @staticmethod
    def getPolygonMid(wallskeleton):
        wallskeletons = []
        wallskeletons.append(wallskeleton)
        H,V,a,b,c,d = WallSkeleton.getMids(wallskeletons)
        if len(H)==0: return V[0]
        else:return H[0]

    @staticmethod
    def createSkeletonsFromWall(wall, minZ=None, maxZ=None):
        e = 0.2
        pols = ShapeToPoly.getPolygonesFromShape(wall.shape)
        if maxZ is not None:
            maxZ = min([maxZ, max([pnt.z for poly in pols for pnt in poly.points])]) - e
        if minZ is not None: minZ = minZ + e
        allPolygons = wall.getXYPlanePolygons(minZ, maxZ)

        # print('maxZ: ',maxZ,' maxZ2: ',maxZ2)
        polygons = wall.getBasePolygons()
        result = []
        i = 1
        # from matplotlib import pyplot as plt
        for poly2 in allPolygons:
            for poly in polygons:
                if not poly.intersects(poly2):
                    result.append(poly)
                    continue
                inters = poly.intersection(poly2)
                if inters:
                    result += poly.subtractPoly(inters)
                else:
                    result.append(poly)
            polygons = result
            # Plotter.plotPolys(polygons,i)
            # plt.show()
            i += 1
            result = []

        wallSkeletons = []


        for polygon in polygons:
            try:
                wallSkeleton = WallSkeleton(polygon)
            except NotBoxError:
                print("not box error")
                continue
            wallSkeletons.append(wallSkeleton)

        return wallSkeletons
    @staticmethod
    def getMids(wallSkeletons):
        HorizontalWallSkeletons = []
        VerticalWallSkeletons = []
        HorizontalMid = []
        VerticalMid = []
        HaxesCoords = []
        VaxesCoords = []
        for wallSkeleton in wallSkeletons:
            if abs(wallSkeleton.vecLength.x()) < abs(wallSkeleton.vecLength.y()):
                VerticalWallSkeletons.append(wallSkeleton)
            else:
                HorizontalWallSkeletons.append(wallSkeleton)

        for wallSkeleton in VerticalWallSkeletons:
            Mid,Coord = wallSkeleton.poly.VerticalalMids(wallSkeleton.getWidth(),wallSkeleton.getHeight())
            if Mid.length>0.21:
                if Coord not in VaxesCoords: VaxesCoords.append(Coord)
            VerticalMid.append(Mid)

        for wallSkeleton in HorizontalWallSkeletons:
            Mid,Coord = wallSkeleton.poly.HorizontalMids(wallSkeleton.getWidth(),wallSkeleton.getHeight())
            if Mid.length>0.21:
                if Coord not in HaxesCoords: HaxesCoords.append(Coord)
            HorizontalMid.append(Mid)
        # HwallSkeletonandMids = [HorizontalWallSkeletons,HorizontalMid]
        # VwallSkeletonandMids = [VerticalWallSkeletons,VerticalMid]
        return HorizontalMid, VerticalMid,HaxesCoords,VaxesCoords

    @staticmethod
    def createAxes(wallSkeletons,slabSkeleton):
        Haxes=[]
        Vaxes = []
        intersections=[]
        CurPotentialColumns=[]
        HorizontalMid, VerticalMid, HaxesCoords, VaxesCoords = WallSkeleton.getMids(wallSkeletons)
        for coord in VaxesCoords:
            first = (coord, 0)
            second = (coord, round(slabSkeleton.poly.MaxCoords().y(),2))
            Axis = linestring.LineString([first, second])
            Vaxes.append(Axis)

        for coord in HaxesCoords:
            first = (0, coord)
            second = (round(slabSkeleton.poly.MaxCoords().x(),2), coord)
            Axis = linestring.LineString([first, second])
            Haxes.append(Axis)

        for Vaxis in Vaxes:
            for Haxis in Haxes:
                intersection= Vaxis.intersection(Haxis)
                if intersection not in intersections: intersections.append(intersection)

        Mids = VerticalMid+HorizontalMid
        i=0

        for pnt in intersections:
            print("Point",pnt.x,pnt.y)
            for mid in Mids:
                if pnt.within(mid):
                    i=i+1
                    point = Point(round(pnt.x,2),round(pnt.y,2))
                    if point not in CurPotentialColumns: CurPotentialColumns.append(point)

        return Vaxes,Haxes, CurPotentialColumns

    @staticmethod
    def Columns(skeletonLevels,level):

        levelSkeleton = skeletonLevels[level]
        vaxes, haxes, bcolumns = WallSkeleton.createAxes(levelSkeleton.wallSkeletons,
                                                        levelSkeleton.slabSkeleton)
        columns = []
        scolumns = []
        mcolumns=[]
        if level!=0:
            fisrtLevelSkeleton = skeletonLevels[0]
            fColumns = WallSkeleton.createAxes(fisrtLevelSkeleton.wallSkeletons,
                                                                fisrtLevelSkeleton.slabSkeleton)[2]
            for i in range(1,level+1):
                levelSkeleton = skeletonLevels[i]
                for column in fColumns:
                    for wall in levelSkeleton.wallSkeletons:
                        if wall.poly.containsPoint(column): scolumns.append(column)
            for column in scolumns:
                if column not in mcolumns: mcolumns.append(column)
            for column in mcolumns:
                if scolumns.count(column)>=level:
                    columns.append(column)


        else: columns= bcolumns
        axes = haxes + vaxes

        ColumnDistances = WallSkeleton.ColumnDistances(columns)
        return columns, haxes, vaxes

    @staticmethod
    def ColumnDistances(PColumns):
        pColumns=[]
        Distances=[[],[]]
        upyDist=0
        xDist=0
        for Column in PColumns:
            pColumns.append(Column)
            if Column.y>upyDist: upyDist=Column.y
            if Column.x>xDist: xDist=Column.x
        for i in range(len(pColumns)):
            UpyDist =upyDist
            DownyDist = upyDist
            LeftDist = xDist
            RightDist = xDist
            ytest1= True
            ytest2 = True
            xtest1 = True
            xtest2 = True
            for j in range(len(pColumns)):
                if j!=i:
                    if pColumns[i].x == pColumns[j].x:
                        if pColumns[i].y-pColumns[j].y>0 and pColumns[i].y-pColumns[j].y< UpyDist:
                            UpyDist = pColumns[i].y-pColumns[j].y
                            ytest1=False
                        if pColumns[i].y-pColumns[j].y<0 and abs(pColumns[i].y-pColumns[j].y)< DownyDist:
                            DownyDist=abs(pColumns[i].y-pColumns[j].y)
                            ytest2=False

                if pColumns[i].y == pColumns[j].y:
                    if pColumns[i].x - pColumns[j].x > 0 and pColumns[i].x - pColumns[j].x < LeftDist:
                        LeftDist = pColumns[i].x - pColumns[j].x
                        xtest1 = False
                    if pColumns[i].x - pColumns[j].x < 0 and abs(pColumns[i].x - pColumns[j].x) < RightDist:
                        RightDist = abs(pColumns[i].x - pColumns[j].x)
                        xtest2 = False

            if not ytest1 and not ytest2 : finalYdist = max(UpyDist, DownyDist)
            elif ytest1 : finalYdist = DownyDist
            elif ytest2 : finalYdist = UpyDist

            if not xtest1 and not xtest2 : finalXdist = max(LeftDist, RightDist)
            elif xtest1 : finalXdist = RightDist
            elif xtest2 : finalXdist = LeftDist
            Distances[0].append(finalXdist)
            Distances[1].append(finalYdist)

            # print("Distance of the point",i,"(",pColumns[i].x,pColumns[i].y,")",finalXdist,finalYdist)

        return Distances

    def createRandomVoileFromRatio(self, ratio):
        if ratio >= 1:
            return VoileSkeleton(self, 0, self.vecLength.magn())
        length = self.vecLength.magn() * ratio
        leftLength = self.vecLength.magn() - length
        move = random.uniform(0, leftLength)
        return VoileSkeleton(self, move, move + length)

    def createRandomVoilesFromLengthNeeded(self, totalLength, needed):
        return self.createRandomVoilesFromLengthNeeded2(totalLength, needed)

    def createRandomVoilesFromLengthNeeded1(self, totalLength, needed):
        lengthDiscreted = self.vecLength.magn() / WallSkeleton.discreteFactor
        minVoileLen = WallSkeleton.miniVoileLength / WallSkeleton.discreteFactor
        voiles = []
        start = 0
        i = 0
        proba = needed / totalLength
        lengthCreated = 0
        while i < int(lengthDiscreted - minVoileLen):
            # for i in range(int(lengthDiscreted-minVoileLen)):

            rand = random.uniform(0, 1)
            if rand <= proba:
                needed -= minVoileLen
                totalLength -= minVoileLen
                i += minVoileLen
                end = start + WallSkeleton.miniVoileLength
                while random.uniform(0, 1) <= proba and i < int(lengthDiscreted):
                    needed -= 1
                    totalLength -= 1
                    end += WallSkeleton.discreteFactor
                    i += 1

                voiles.append(VoileSkeleton(self, start, end))
                lengthCreated += (end - start)
                start = end

            start += WallSkeleton.discreteFactor
            totalLength -= 1
            i += 1

        return lengthCreated, voiles

    def createRandomVoilesFromLengthNeeded2(self, totalLength, needed):
        lengthDiscreted = self.vecLength.magn() / WallSkeleton.discreteFactor
        if totalLength <= 0 or needed <= 0 or lengthDiscreted < 1:
            return 0, []
        proba = min([needed / totalLength, 1])
        # if lengthDiscreted < 1:
        #     if random.uniform(0,1) < proba:
        #         return self.vecLength.magn(),[VoileSkeleton(self,0,self.vecLength.magn())]
        #     return 0,[]
        minVoileLen = WallSkeleton.miniVoileLength / WallSkeleton.discreteFactor
        voiles = []

        lengthCreated = 0
        n = numpy.random.binomial(lengthDiscreted, proba)
        length = n * WallSkeleton.discreteFactor
        listToAdd = []
        while length >= WallSkeleton.miniVoileLength:
            mean = WallSkeleton.optimumVoileLength
            dev = max([WallSkeleton.maxVoileLength - mean, mean - WallSkeleton.miniVoileLength])
            toAdd = numpy.random.normal(mean, dev)
            toAdd = min([max([toAdd, WallSkeleton.miniVoileLength]), WallSkeleton.maxVoileLength])
            listToAdd.append(toAdd)
            lengthCreated += toAdd
            length -= toAdd
        # first voile start from 0
        s, e = 0, self.vecLength.magn()
        left = max([0, self.vecLength.magn() - lengthCreated])
        lengthCreated = 0
        if random.uniform(0, 1) < WallSkeleton.startFromZeroProba:
            if len(listToAdd) > 0:
                end = min([listToAdd[0], self.vecLength.magn()])
                voile = VoileSkeleton(self, 0, end)
                del listToAdd[0]
                voiles.append(voile)
                s = end
                lengthCreated += voile.getLength()
        if random.uniform(0, 1) < WallSkeleton.startFromZeroProba:
            if len(listToAdd) > 0:
                start = max([0, self.vecLength.magn() - listToAdd[0]])
                voile = VoileSkeleton(self, start, self.vecLength.magn())
                del listToAdd[0]
                voiles.append(voile)
                e = start
                lengthCreated += voile.getLength()

        while s < e and len(listToAdd) > 0:
            leave = random.uniform(0, left)
            left = max([0, left - leave])
            start = s + leave
            end = min([start + listToAdd[0], e])
            if end - start > self.vecLength.magn():
                print(
                    ("ERROR FROM WALL SKELETON RANDOM", end - start, self.vecLength.magn(), left, start, end, s, leave))
            voile = VoileSkeleton(self, start, end)
            voiles.append(voile)
            s = end
            lengthCreated += voile.getLength()
            del listToAdd[0]

        return lengthCreated, voiles

    def attachVoiles(self, voileSkeletons):
        for voileSkeleton in voileSkeletons:
            self.attachVoile(voileSkeleton)

    def attachVoile(self, voileSkeleton):
        # self.attachedVoiles.append(voileSkeleton)
        # voileSkeleton.setParentWall(self)
        self.reInitFitness()
        voileSkeleton.setParentWall(self)
        from Optimization.Genetic.GeneticOperations import mergeVoile
        start = voileSkeleton.start
        end = voileSkeleton.end
        if end - start > self.vecLength.magn():
            print(('PROBLEM VOILE LENGTH', end - start, self.vecLength.magn()))
        mergeVoile(self.attachedVoiles, voileSkeleton)

    def attachFixedVoile(self, voileSkeleton):
        # self.attachedVoiles.append(voileSkeleton)
        # voileSkeleton.setParentWall(self)
        self.reInitFitness()
        voileSkeleton.setParentWall(self)
        from Optimization.Genetic.GeneticOperations import mergeVoile
        mergeVoile(self.fixedVoiles, voileSkeleton)

    # gets voile starting from most left point to distance
    def getVoilesBetween(self, mini=0, maxi=1):
        mini = mini * self.vecLength.magn()
        maxi = maxi * self.vecLength.magn()
        newVoiles = []
        for voile in self.attachedVoiles:
            if mini <= voile.start < maxi:
                newVoiles.append(VoileSkeleton(self, voile.start, min(maxi, voile.end)))
            elif voile.start <= mini < voile.end:
                newVoiles.append(VoileSkeleton(self, mini, min(maxi, voile.end)))
        return newVoiles

    def getAllVoiles(self):
        return self.attachedVoiles + self.fixedVoiles

    def removeVoile(self, index):
        self.reInitFitness()
        del self.attachedVoiles[index]

    def getVoile(self, index):
        return self.attachedVoiles[index]

    def copy(self):
        wallSkeleton = WallSkeleton(self.poly.copy(), (self.topLeftPnt, self.vecLength, self.vecWidth))
        wallSkeleton.evalData = self.evalData
        wallSkeleton.attachVoiles([voileSkeleton.copy() for voileSkeleton in self.attachedVoiles])
        wallSkeleton.fixedVoiles = self.fixedVoiles
        return wallSkeleton

    def copyWithoutVoiles(self):
        wallSkeleton = WallSkeleton(self.poly.copy(), (self.topLeftPnt, self.vecLength, self.vecWidth))
        wallSkeleton.evalData = self.evalData
        wallSkeleton.fixedVoiles = self.fixedVoiles
        return wallSkeleton

    def reInitFitness(self):
        super(WallSkeleton, self).reInitFitness()
        self.sums = None

    def getSums2(self, origin):
        if self.sums2 is not None:
            return self.sums2
        sumLx3 = 0
        sumLy3 = 0
        sumX2Ly3 = 0
        sumY2Lx3 = 0
        if self.iscolumnParent:
            centerV = self.poly.centroid()
            centerV = Pnt(centerV.x, centerV.y)
            x = math.pow(self.poly.MaxCoords().x() - self.poly.MinCoords().x(), 3)
            y = math.pow(self.poly.MaxCoords().y() - self.poly.MinCoords().y(), 3)
            sumLx3 = 0
            sumLy3 = 0
            sumX2Ly3 = 0
            sumY2Lx3 = 0
        else:
            for voileSkeleton in self.getAllVoiles():
                centerV = voileSkeleton.poly.centroid()
                centerV = Pnt(centerV.x - origin.x(), centerV.y - origin.y())
                Lx3 = math.pow(abs(voileSkeleton.vecLength.x()), 3)
                Ly3 = math.pow(abs(voileSkeleton.vecLength.y()), 3)
                sumLx3 += Lx3
                sumLy3 += Ly3
                sumX2Ly3 += Ly3 * math.pow(centerV.x(), 2)
                sumY2Lx3 += Lx3 * math.pow(centerV.y(), 2)
        self.sums2 = sumLx3, sumLy3, sumX2Ly3, sumY2Lx3
        return self.sums2

    def getSums(self):
        # if self.sums is not None:
        #     return self.sums
        sumLi1 = 0
        sumLi2 = 0
        sumLixi = 0
        sumLiyi = 0
        if self.iscolumnParent:
            # centerV = self.poly.centroid()
            # centerV = Pnt(centerV.x, centerV.y)
            # x = math.pow(self .poly.MaxCoords().x() - self.poly.MinCoords().x(), 1)
            # y = math.pow(self.poly.MaxCoords().y() - self.poly.MinCoords().y(), 1)
            # sumLi1 = x
            # sumLi2 = y
            # sumLixi += y * centerV.x()
            # sumLiyi += x * centerV.y()
            a=0
        else:
            for voileSkeleton in self.getAllVoiles():
                centerV = voileSkeleton.poly.centroid()
                centerV = Pnt(centerV.x, centerV.y)
                x3 = math.pow(abs(voileSkeleton.vecLength.x()), 3)
                y3 = math.pow(abs(voileSkeleton.vecLength.y()), 3)
                sumLi1 += x3
                sumLi2 += y3
                sumLixi += y3 * centerV.x()
                sumLiyi += x3 * centerV.y()
        self.sums = sumLi1, sumLi2, sumLixi, sumLiyi
        return self.sums

    def getVoilesLength(self):
        return sum(voileSkeleton.getLength() for voileSkeleton in self.getAllVoiles())

    @staticmethod
    def ColumnToVoile(ColumnPolys, wallSkeletons):
        voiles = []
        for Column in ColumnPolys:
            pnts = Column.exterior.coords
            x= round(Column.centroid.x,2)
            y= round(Column.centroid.y,2)
            end1 = round(pnts[1][0]-pnts[0][0],2)
            end2 = round(pnts[3][1]-pnts[0][1],2)
            if end1>end2: end=end1
            else:end=end2
            for wall in wallSkeletons:
                X = round(wall.poly.centroid().x, 2)
                Y = round(wall.poly.centroid().y, 2)
                dim1 = abs(wall.poly.MinCoords().x() - wall.poly.MaxCoords().x())
                dim2 = abs(wall.poly.MinCoords().y() - wall.poly.MaxCoords().y())
                if X==x and Y==y:
                    if dim1>0.2 and dim2>0.2:
                        voile = VoileSkeleton(wall, 0, end)
                        voiles.append(voile)

        return voiles
