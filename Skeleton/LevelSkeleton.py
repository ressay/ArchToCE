from Skeleton.SlabSkeleton import SlabSkeleton
from Skeleton.WallSkeleton import WallSkeleton
from Skeleton.Skelet import Skelet


class LevelSkeleton(Skelet):

    def __init__(self,walls,slab,level):
        super(LevelSkeleton, self).__init__()
        self.wallSkeletons = walls
        self.slabSkeleton = slab
        self.level = level
        self.height = level.getHeightOverLowerLevel()

    @staticmethod
    def createSkeletonFromLevel(level):
        slabSkeleton = SlabSkeleton.createSkeletonFromSlab(level.slab)
        wallSkeletons = [WallSkeleton.createSkeletonFromWall(wall) for wall in level.walls]
        return LevelSkeleton(wallSkeletons,slabSkeleton,level)

    def getVoileLengthNeeded(self):
        return 1.3*self.height*self.slabSkeleton.poly.area()/100

    def getWallsTotalLength(self):
        length = 0
        for wallSkeleton in self.wallSkeletons:
            length += wallSkeleton.vecLength.magn()
        return length

    def getRatio(self):
        if self.getWallsTotalLength() == 0:
            return 1
        return self.getVoileLengthNeeded()/self.getWallsTotalLength()

    def copy(self):
        walls = [wallSkeleton.copy() for wallSkeleton in self.wallSkeletons]
        levelSkeleton = LevelSkeleton(walls,self.slabSkeleton.copy(),self.level)
        levelSkeleton.evalData = self.evalData
        return levelSkeleton