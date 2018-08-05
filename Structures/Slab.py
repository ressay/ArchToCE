from Geometry.ShapeToPoly import getShapeBasePolygon, getBaseOfShapeZ
from Structure import Structure
from Structures.StructureExceptions.NotSlabShapeException import NotSlabShapeException


class Slab(Structure):

    def __init__(self,shape):
        print("slab z: " + str(getBaseOfShapeZ(shape)))
        if not getShapeBasePolygon(shape):
            raise NotSlabShapeException("slab doesn't have base polygon")
        super(Slab, self).__init__(shape)


    def getSupportingWalls(self,walls):
        supportingWalls = []
        for wall in walls:
            if wall.isSupporting(self):
                supportingWalls.append(wall)

        return supportingWalls