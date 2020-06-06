from Geometry.ShapeToPoly import getShapeBasePolygon
from Geometry.ShapeToPoly import getPolygonesFromShape
from Structure import Structure
from Structures.StructureExceptions.NotWallShapeException import NotWallShapeException


class Wall(Structure):

    def __init__(self,shape):
        if not getShapeBasePolygon(shape):
            polygons = getPolygonesFromShape(shape)
            for polygon in polygons:
                print "polygon:"
                for pnt in polygon.points:
                    print("point is: (%.2f, %.2f, %.2f) " % (pnt.x, pnt.y, pnt.z))
            raise NotWallShapeException("wall doesn't have base polygon")
        super(Wall, self).__init__(shape)


    def isSupporting(self,slab):
        tolerance = 0.2
        # miniArea = self.getBasePolygon().area()/5
        lowestW = self.getLowestPoint()
        lowestS = slab.getLowestPoint()

        if lowestS and lowestW and lowestW.z < lowestS.z:
            if self.getHighestPoint().z >= lowestS.z-tolerance:# and self._isUnderSlab(slab):
                polygons = self.getBasePolygons()
                # s = 0
                for poly in polygons:
                    inters = poly.intersection(slab.getBasePolygon())
                    if inters:
                        return True
                return False

        return False

    def _isUnderSlab(self,slab):
        polW = self.getBasePolygon()
        polS = slab.getBasePolygon()
        return polS.intersects(polW)