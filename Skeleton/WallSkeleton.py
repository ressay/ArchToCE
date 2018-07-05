import random

from Skeleton.BoxSkeleton import BoxSkeleton
from Skeleton.VoileSkeleton import VoileSkeleton


class WallSkeleton(BoxSkeleton):
    discreteFactor = 0.1 # each 0.1 m
    miniVoileLength = 0.6
    # attachedVoiles = []
    def __init__(self, poly,pnts = None):
        super(WallSkeleton, self).__init__(poly,pnts)
        self.attachedVoiles = []

    @staticmethod
    def createSkeletonFromWall(wall):
        return WallSkeleton(wall.getBasePolygon())

    def createRandomVoileFromRatio(self,ratio):
        if ratio >= 1:
            return VoileSkeleton(self,0,self.vecLength.magn())
        length = self.vecLength.magn()*ratio
        leftLength = self.vecLength.magn() - length
        move = random.uniform(0,leftLength)
        return VoileSkeleton(self,move,move+length)

    def createRandomVoilesFromLengthNeeded(self, totalLength, needed):
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

    def attachVoiles(self,voileSkeletons):
        for voileSkeleton in voileSkeletons:
            self.attachedVoiles.append(voileSkeleton)
            voileSkeleton.setParentWall(self)

    def attachVoile(self,voileSkeleton):
        self.attachedVoiles.append(voileSkeleton)
        voileSkeleton.setParentWall(self)

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


    def copy(self):
        wallSkeleton = WallSkeleton(self.poly.copy(),(self.topLeftPnt, self.vecLength, self.vecWidth))
        wallSkeleton.evalData = self.evalData
        wallSkeleton.attachVoiles([voileSkeleton.copy() for voileSkeleton in self.attachedVoiles])
        return wallSkeleton

    def copyWithoutVoiles(self):
        wallSkeleton = WallSkeleton(self.poly.copy(),(self.topLeftPnt, self.vecLength, self.vecWidth))
        wallSkeleton.evalData = self.evalData
        return wallSkeleton
