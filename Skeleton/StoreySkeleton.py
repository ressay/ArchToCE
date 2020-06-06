from shapely.geometry import Polygon
from shapely.ops import cascaded_union

from Geometry.Geom2D import Pnt
from Skeleton.BoxSkeleton import NotBoxError
from Skeleton.SlabSkeleton import SlabSkeleton
from Skeleton.WallSkeleton import WallSkeleton
from Skeleton.Skelet import Skelet
import math


class StoreySkeleton(Skelet):
    def __init__(self, levelSkeletons):
        super(StoreySkeleton, self).__init__()
        self.levels = [levelSkeleton.level for levelSkeleton in levelSkeletons]
        self.levelSkeletons = levelSkeletons
        self.wallSkeletons = [wallSkeleton for levelSkeleton in levelSkeletons
                              for wallSkeleton in levelSkeleton.wallSkeletons]
        self.walls = [wall for level in self.levels
                      for wall in level.walls]
        self.notModifiedWalls = [levelSkeleton.wallSkeletons for levelSkeleton in levelSkeletons]
        self.slabSkeletons = [levelSkeleton.slabSkeleton for levelSkeleton in levelSkeletons]
        self.height = self.levels[0].getHeightOverLowerLevel()

    def getWallsTotalLength(self):
        length = 0
        for wallSkeleton in self.wallSkeletons:
            length += wallSkeleton.vecLength.magn()
        return length

    def getVoilesTotalLength(self):
        return sum(wallSkeleton.getVoilesLength() for wallSkeleton in self.wallSkeletons)

    def getPolys(self):
        return [wallSkeleton.poly for wallSkeleton in self.wallSkeletons]
