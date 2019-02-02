# from Structure.Slab import Slab
# from Structures.Wall import Wall
from Debugging.Logger import Logger
from Geometry.ShapeToPoly import getBaseOfShapeZ
from Slab import Slab
from Structures.StructureExceptions.NotSlabShapeException import NotSlabShapeException
from Structures.StructureExceptions.NotWallShapeException import NotWallShapeException
from Wall import Wall

class Level(object):

    def __init__(self, slab, walls):
        super(Level, self).__init__()
        self.slab = slab
        self.walls = walls
        self.relatedLevels = []
        self.lowerLevel = None
        self.upperLevel = None
        self.lowerLevels = None

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
        for shape in slabShapes:
            try:
                logger.clearTrack("NotSlabShapeException")
                slab = Slab(shape)
            except NotSlabShapeException:
                # print("slab not added")
                logger.printTrack("NotSlabShapeException")
                continue
            slabs.append(slab)



        for slab in slabs:
            levels.append(Level(slab, slab.getSupportingWalls(walls)))
        for level in levels:
            level.relatedLevels = levels
        return levels

    def getLowerLevels(self):
        if self.lowerLevels:
            return self.lowerLevels
        lowerLevels = [lvl for lvl in self.relatedLevels if lvl.isUnder(self)]
        if self.lowerLevels is None and len(lowerLevels) != 0:
            maxVal = max([level.getHeight() for level in lowerLevels])
            self.lowerLevels = [level for level in lowerLevels if level.getHeight() == maxVal]
        return self.lowerLevels

    def getLowerLevel(self):
        if self.lowerLevel:
            return self.lowerLevel
        lowerLevels = self.getLowerLevels()
        if lowerLevels and len(lowerLevels) != 0:
            self.lowerLevel = lowerLevels[0]
        return self.lowerLevel

    def getUpperLevel(self):
        if self.upperLevel:
            return self.upperLevel
        upperLevels = [lvl for lvl in self.relatedLevels if lvl.isOver(self)]
        if self.upperLevel is None and len(upperLevels) != 0:
            self.upperLevel = min(upperLevels, key=lambda p: p.getHeight())
        return self.upperLevel

    def isOver(self,level):
        return self.getHeight() > level.getHeight()

    def isUnder(self,level):
        return self.getHeight() < level.getHeight()

    def getHeight(self):
        return float(getBaseOfShapeZ(self.slab.shape))

    def getHeightOverLowerLevel(self):
        if self.getLowerLevel() is None:
            return -1
        return self.getHeight() - self.getLowerLevel().getHeight()

# slab z: -0.2
# slab z: 3.8
# slab z: 7.8
# slab z: 5.8
# slab z: 11.8
# slab z: 15.8
# slab z: 19.8