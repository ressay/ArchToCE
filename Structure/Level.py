# from Structure.Slab import Slab
# from Structure.Wall import Wall
from Slab import Slab
from Wall import Wall

class Level(object):
    walls = []
    slabs = []

    def __init__(self,slabs,walls):
        super(Level, self).__init__()
        self.slabs = slabs
        self.walls = walls

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
            levels.append(Level([slab], slab.getSupportingWalls(walls)))
        return levels



