from Geometry.Geom2D import Pnt
from Skeleton.BoxSkeleton import NotBoxError
from Skeleton.SlabSkeleton import SlabSkeleton
from Skeleton.WallSkeleton import WallSkeleton
from Skeleton.Skelet import Skelet


class LevelSkeleton(Skelet):

    def __init__(self,walls,slab,level):
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
        for wall in level.walls:
            wallSkeletons += WallSkeleton.createSkeletonsFromWall(wall,
                                                        level.getLowerLevel().slab.getHighestZ(),
                                                                  level.slab.getLowestZ())
        # wallSkeletons = [WallSkeleton.createSkeletonFromWall(wall) for wall in level.walls]
        return LevelSkeleton(wallSkeletons,slabSkeleton,level)

    def getVoileLengthNeeded(self):
        return 1.3*self.height*self.slabSkeleton.poly.area()/100

    def getWallsTotalLength(self):
        length = 0
        for wallSkeleton in self.wallSkeletons:
            length += wallSkeleton.vecLength.magn()
        return length

    def getVoilesTotalLength(self):
        return sum(wallSkeleton.getVoilesLength() for wallSkeleton in self.wallSkeletons)

    def getRatio(self):
        if self.getWallsTotalLength() == 0:
            return 1
        return self.getVoileLengthNeeded()/self.getWallsTotalLength()

    def copy(self):
        walls = [wallSkeleton.copy() for wallSkeleton in self.wallSkeletons]
        levelSkeleton = LevelSkeleton(walls,self.slabSkeleton.copy(),self.level)
        levelSkeleton.evalData = self.evalData
        return levelSkeleton

    def getCenterFromSlab(self):
        return Pnt.createPointFromShapely(self.slabSkeleton.poly.centroid())

    def getSlabArea(self):
        return self.slabSkeleton.poly.area()

    def getCenterFromShear(self):
        sumLiX = 0
        sumLiY = 0
        sumLixi = 0
        sumLiyi = 0
        for wallSkeleton in self.wallSkeletons:
            sLiX, sLiY, sLixi, sLiyi = wallSkeleton.getSums()
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
        cntr = Pnt(y, x)

        return cntr

    def restrictLevelUsableWalls(self,levelSkeleton):
        restrictWalls = levelSkeleton.wallSkeletons
        resultWalls = []
        for wallSkeleton in restrictWalls:
            for wallSkeleton2 in self.wallSkeletons:
                intersection = wallSkeleton.poly.intersection(wallSkeleton2.poly)
                if intersection:
                    resultWalls.append(WallSkeleton(intersection))

        self.wallSkeletons = resultWalls

    def copyLevelsVoiles(self,levelSkeleton):
        aboveWalls = levelSkeleton.wallSkeletons
        for wallSkeleton in aboveWalls:
            if not wallSkeleton.getVoilesLength():
                continue
            for wallSkeleton2 in self.wallSkeletons:
                intersection = wallSkeleton.poly.intersection(wallSkeleton2.poly)
                if intersection and wallSkeleton.poly.area() == intersection.area(): # test if polygons are equal
                    voiles = wallSkeleton.getAllVoiles()
                    for voileSkeleton in voiles:
                        voileSkeleton = voileSkeleton.copy()
                        voileSkeleton.setParentWall(wallSkeleton2,True)
                        wallSkeleton2.attachFixedVoile(voileSkeleton)
                    break
    def getPolys(self):
        return [wallSkeleton.poly for wallSkeleton in self.wallSkeletons]