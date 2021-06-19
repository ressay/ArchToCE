# from Structure.Slab import Slab
# from Structures.Wall import Wall
from Debugging.Logger import Logger
from Geometry.ShapeToPoly import getBaseOfShapeZ, getTopOfShapeZ
from .Slab import Slab
from Structures.StructureExceptions.NotSlabShapeException import NotSlabShapeException
from Structures.StructureExceptions.NotWallShapeException import NotWallShapeException
from .Wall import Wall

class Level(object):

    def __init__(self, slab, walls):
        super(Level, self).__init__()
        self.slab = slab
        self.walls = walls
        self.relatedLevels = []
        self.heighestZ = None

    @staticmethod
    def generateLevelsFromShapes(wallShapes,slabShapes):
        levels = []
        walls = []
        slabs = []
        logger = Logger.getInstance()
        for shape in wallShapes:
            try:
                # print "wall:"
                logger.clearTrack("NotWallShapeException")
                wall = Wall(shape)
            except NotWallShapeException:
                # print "not added"
                logger.printTrack("NotWallShapeException")
                continue
            walls.append(wall)
        heigh = -2000
        for shape in slabShapes:
            if getTopOfShapeZ(shape) > heigh:
                heigh = getTopOfShapeZ(shape)
            try:
                logger.clearTrack("NotSlabShapeException")
                slab = Slab(shape)
            except NotSlabShapeException:
                # print("slab not added")
                logger.printTrack("NotSlabShapeException")
                continue
            if slab.getBasePolygon().area() < 2:  # 2 m^2 is limit to consider the slab
                continue
            slabs.append(slab)


        for slab in slabs:
            levels.append(Level(slab, slab.getSupportingWalls(walls)))
        for level in levels:
            level.relatedLevels = levels
            print("In level: ",level.relatedLevels)
            level.heighestZ = heigh
        return levels

    def getLowerLevels(self):
        lowerLevels = [lvl for lvl in self.relatedLevels if lvl.isUnder(self)]
        if len(lowerLevels) != 0:
            maxVal = max([level.getHeight() for level in lowerLevels])
            return [level for level in lowerLevels if level.getHeight() == maxVal]
        return []

    def getRightLowerLevels(self):
        return [lvl for lvl in self.relatedLevels if lvl.isRightUnder(self)]

    def getLowerLevel(self):
        lowerLevels = self.getLowerLevels()
        if lowerLevels and len(lowerLevels) != 0:
            return lowerLevels[0]
        return None

    def getUpperLevel(self):
        upperLevels = [lvl for lvl in self.relatedLevels if lvl.isOver(self)]
        if len(upperLevels) != 0:
            return min(upperLevels, key=lambda p: p.getHeight())
        return None

    def getUpperLevels(self):
        return [lvl for lvl in self.relatedLevels if lvl.isOver(self)]

    def isOver(self,level):
        return self.getHeight() > level.getHeight()

    def isUnder(self,level):
        return self.getHeight() < level.getHeight()

    def isRightUnder(self, level):
        if level.getHeight() <= self.getHeight():
            return False
        return True
        lowerLevels = [lvl for lvl in level.relatedLevels if lvl.getHeight() < level.getHeight()]
        # print('LOWERLEVELS SIZE BEFORE FILTER: ', len(lowerLevels))
        lowerLevels = [lvl for lvl in lowerLevels if lvl.getHeight() > self.getHeight()]
        # print('LOWERLEVELS SIZE AFTER FILTER: ', len(lowerLevels))
        union = None
        for lvl in lowerLevels:
            intersection = self.slab.getBasePolygon().intersection(lvl.slab.getBasePolygon())
            if not intersection:
                continue
            if not union:
                union = intersection.poly
            else:
                union.union(intersection.poly)
        # if not union:
        #     print("TRUE BECAUSE NOT UNION")
        # elif union.area != self.slab.getBasePolygon().area:
        #     print("TRUE BECAUSE AREAS ARE NOT EQUAL",union.area,self.slab.getBasePolygon().poly.area)
        return not union or union.area != self.slab.getBasePolygon().poly.area


    def getHeight(self):
        return float(getBaseOfShapeZ(self.slab.shape))

    def getHeightOverLowerLevel(self):
        if self.getLowerLevel() is None:
            return 2.7
        return self.getHeight() - self.getLowerLevel().getHeight()

    def getBuildingHeight(self):
        return max(level.getHeight() for level in self.relatedLevels)

# slab z: -0.2
# slab z: 3.8
# slab z: 7.8
# slab z: 5.8
# slab z: 11.8
# slab z: 15.8
# slab z: 19.8