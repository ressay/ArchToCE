# from Structure.Slab import Slab
# from Structure.Wall import Wall
from Geometry.ShapeToPoly import getBaseOfShapeZ
from Slab import Slab
from Wall import Wall

class Level(object):

    def __init__(self, slab, walls):
        super(Level, self).__init__()
        self.slab = slab
        self.walls = walls
        self.relatedLevels = []
        self.lowerLevel = None
        self.upperLevel = None

    @staticmethod
    def generateLevelsFromShapes(wallShapes,slabShapes):
        levels = []
        walls = []
        slabs = []
        for shape in wallShapes:
            walls.append(Wall(shape))

        for shape in slabShapes:
            slabs.append(Slab(shape))

        for slab in slabs:
            levels.append(Level(slab, slab.getSupportingWalls(walls)))
        for level in levels:
            level.relatedLevels = levels
        return levels

    def getLowerLevel(self):
        if self.lowerLevel:
            return self.lowerLevel
        lowerLevels = [lvl for lvl in self.relatedLevels if lvl.isUnder(self)]
        if self.lowerLevel is None and len(lowerLevels) != 0:
            self.lowerLevel = max(lowerLevels, key=lambda p: p.getHeight())
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

