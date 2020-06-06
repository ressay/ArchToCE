import random

import math

import numpy

from Geometry import ShapeToPoly
from Geometry.Geom2D import Pnt
from Skeleton.BoxSkeleton import BoxSkeleton, NotBoxError
from Skeleton.VoileSkeleton import VoileSkeleton
from UI import Plotter


class WallSkeleton(BoxSkeleton):
    discreteFactor = 0.1 # each 0.1 m
    miniVoileLength = 0.8
    maxVoileLength = 4
    optimumVoileLength = 2.5
    startFromZeroProba = 0.7
    # attachedVoiles = []
    def __init__(self, poly,pnts=None):
        super(WallSkeleton, self).__init__(poly,pnts)
        self.attachedVoiles = []
        self.fixedVoiles = []
        self.sums = None
        self.sums2 = None

    @staticmethod
    def createSkeletonFromWall(wall):
        return WallSkeleton(wall.getBasePolygon())

    @staticmethod
    def createSkeletonsFromWall(wall, minZ=None,maxZ=None):
        e = 0.2
        pols = ShapeToPoly.getPolygonesFromShape(wall.shape)
        if maxZ is not None:
            maxZ = min([maxZ,max([pnt.z for poly in pols for pnt in poly.points])])-e
        if minZ is not None: minZ = minZ + e
        allPolygons = wall.getXYPlanePolygons(minZ,maxZ)

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
                print("not box error damn")
                continue
            wallSkeletons.append(wallSkeleton)

        return wallSkeletons

    def createRandomVoileFromRatio(self,ratio):
        if ratio >= 1:
            return VoileSkeleton(self,0,self.vecLength.magn())
        length = self.vecLength.magn()*ratio
        leftLength = self.vecLength.magn() - length
        move = random.uniform(0,leftLength)
        return VoileSkeleton(self,move,move+length)

    def createRandomVoilesFromLengthNeeded(self, totalLength, needed):
        return self.createRandomVoilesFromLengthNeeded2(totalLength,needed)

    def createRandomVoilesFromLengthNeeded1(self, totalLength, needed):
        lengthDiscreted = self.vecLength.magn()/WallSkeleton.discreteFactor
        minVoileLen = WallSkeleton.miniVoileLength/WallSkeleton.discreteFactor
        voiles = []
        start = 0
        i = 0
        proba = needed / totalLength
        lengthCreated = 0
        while i < int(lengthDiscreted-minVoileLen):
            # for i in range(int(lengthDiscreted-minVoileLen)):

            rand = random.uniform(0,1)
            if rand <= proba:
                needed -= minVoileLen
                totalLength -= minVoileLen
                i += minVoileLen
                end = start + WallSkeleton.miniVoileLength
                while random.uniform(0,1) <= proba and i < int(lengthDiscreted):
                    needed -= 1
                    totalLength -= 1
                    end += WallSkeleton.discreteFactor
                    i += 1

                voiles.append(VoileSkeleton(self,start,end))
                lengthCreated += (end - start)
                start = end

            start += WallSkeleton.discreteFactor
            totalLength -= 1
            i += 1

        return lengthCreated,voiles

    def createRandomVoilesFromLengthNeeded2(self, totalLength, needed):
        lengthDiscreted = self.vecLength.magn()/WallSkeleton.discreteFactor
        if totalLength <= 0 or needed <= 0 or lengthDiscreted < 1:
            return 0,[]
        proba = min([needed / totalLength, 1])
        # if lengthDiscreted < 1:
        #     if random.uniform(0,1) < proba:
        #         return self.vecLength.magn(),[VoileSkeleton(self,0,self.vecLength.magn())]
        #     return 0,[]
        minVoileLen = WallSkeleton.miniVoileLength/WallSkeleton.discreteFactor
        voiles = []

        lengthCreated = 0
        n = numpy.random.binomial(lengthDiscreted,proba)
        length = n*WallSkeleton.discreteFactor
        listToAdd = []
        while length >= WallSkeleton.miniVoileLength:
            mean = WallSkeleton.optimumVoileLength
            dev = max([WallSkeleton.maxVoileLength - mean,mean-WallSkeleton.miniVoileLength])
            toAdd = numpy.random.normal(mean,dev)
            toAdd = min([max([toAdd,WallSkeleton.miniVoileLength]),WallSkeleton.maxVoileLength])
            listToAdd.append(toAdd)
            lengthCreated += toAdd
            length -= toAdd
        # first voile start from 0
        s,e = 0,self.vecLength.magn()
        left = max([0,self.vecLength.magn() - lengthCreated])
        lengthCreated = 0
        if random.uniform(0,1) < WallSkeleton.startFromZeroProba:
            if len(listToAdd) > 0:
                end = min([listToAdd[0],self.vecLength.magn()])
                voile = VoileSkeleton(self,0,end)
                del listToAdd[0]
                voiles.append(voile)
                s = end
                lengthCreated += voile.getLength()
        if random.uniform(0,1) < WallSkeleton.startFromZeroProba:
            if len(listToAdd) > 0:
                start = max([0,self.vecLength.magn()-listToAdd[0]])
                voile = VoileSkeleton(self,start,self.vecLength.magn())
                del listToAdd[0]
                voiles.append(voile)
                e = start
                lengthCreated += voile.getLength()

        while s < e and len(listToAdd) > 0:
            leave = random.uniform(0,left)
            left = max([0,left-leave])
            start = s+leave
            end = min([start+listToAdd[0],e])
            if end - start > self.vecLength.magn():
                print ("ERROR FROM WALL SKELETON RANDOM",end-start,self.vecLength.magn(),left,start,end,s,leave)
            voile = VoileSkeleton(self,start,end)
            voiles.append(voile)
            s = end
            lengthCreated += voile.getLength()
            del listToAdd[0]

        return lengthCreated,voiles

    def attachVoiles(self,voileSkeletons):
        for voileSkeleton in voileSkeletons:
            self.attachVoile(voileSkeleton)

    def attachVoile(self,voileSkeleton):
        # self.attachedVoiles.append(voileSkeleton)
        # voileSkeleton.setParentWall(self)
        self.reInitFitness()
        voileSkeleton.setParentWall(self)
        from Optimization.Genetic.GeneticOperations import mergeVoile
        start = voileSkeleton.start
        end = voileSkeleton.end
        if end-start > self.vecLength.magn():
            print('PROBLEM VOILE LENGTH',end-start,self.vecLength.magn())
        mergeVoile(self.attachedVoiles,voileSkeleton)

    def attachFixedVoile(self,voileSkeleton):
        # self.attachedVoiles.append(voileSkeleton)
        # voileSkeleton.setParentWall(self)
        self.reInitFitness()
        voileSkeleton.setParentWall(self)
        from Optimization.Genetic.GeneticOperations import mergeVoile
        mergeVoile(self.fixedVoiles,voileSkeleton)

    # gets voile starting from most left point to distance
    def getVoilesBetween(self, mini=0,maxi=1):
        mini = mini*self.vecLength.magn()
        maxi = maxi*self.vecLength.magn()
        newVoiles = []
        for voile in self.attachedVoiles:
            if mini <= voile.start < maxi:
                newVoiles.append(VoileSkeleton(self,voile.start,min(maxi,voile.end)))
            elif voile.start <= mini < voile.end:
                newVoiles.append(VoileSkeleton(self, mini, min(maxi, voile.end)))
        return newVoiles

    def getAllVoiles(self):
        return self.attachedVoiles+self.fixedVoiles

    def removeVoile(self,index):
        self.reInitFitness()
        del self.attachedVoiles[index]

    def getVoile(self,index):
        return self.attachedVoiles[index]


    def copy(self):
        wallSkeleton = WallSkeleton(self.poly.copy(),(self.topLeftPnt, self.vecLength, self.vecWidth))
        wallSkeleton.evalData = self.evalData
        wallSkeleton.attachVoiles([voileSkeleton.copy() for voileSkeleton in self.attachedVoiles])
        wallSkeleton.fixedVoiles = self.fixedVoiles
        return wallSkeleton

    def copyWithoutVoiles(self):
        wallSkeleton = WallSkeleton(self.poly.copy(),(self.topLeftPnt, self.vecLength, self.vecWidth))
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
        for voileSkeleton in self.getAllVoiles():
            centerV = voileSkeleton.poly.centroid()
            centerV = Pnt(centerV.x - origin.x(), centerV.y - origin.y())
            Lx3 = math.pow(abs(voileSkeleton.vecLength.x()), 3)
            Ly3 = math.pow(abs(voileSkeleton.vecLength.y()), 3)
            sumLx3 += Lx3
            sumLy3 += Ly3
            sumX2Ly3 += Ly3 * math.pow(centerV.x(),2)
            sumY2Lx3 += Lx3 * math.pow(centerV.y(),2)
        self.sums2 = sumLx3,sumLy3,sumX2Ly3,sumY2Lx3
        return self.sums2

    def getSums(self):
        if self.sums is not None:
            return self.sums
        sumLi1 = 0
        sumLi2 = 0
        sumLixi = 0
        sumLiyi = 0
        for voileSkeleton in self.getAllVoiles():
            centerV = voileSkeleton.poly.centroid()
            centerV = Pnt(centerV.x, centerV.y)
            x3 = math.pow(abs(voileSkeleton.vecLength.x()), 3)
            y3 = math.pow(abs(voileSkeleton.vecLength.y()), 3)
            sumLi1 += x3
            sumLi2 += y3
            sumLixi += y3 * centerV.x()
            sumLiyi += x3 * centerV.y()
        self.sums = sumLi1,sumLi2,sumLixi,sumLiyi
        return self.sums

    def getVoilesLength(self):
        return sum(voileSkeleton.getLength() for voileSkeleton in self.getAllVoiles())



