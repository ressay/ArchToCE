from Geometry import ShapeToPoly

class Structure(object):
    shape = None

    def __init__(self,shape):
        super(Structure, self).__init__()
        self.shape = shape

    def getBasePolygon(self):
        return ShapeToPoly.getShapeBasePolygon(self.shape)

    def getPolygons(self):
        return ShapeToPoly.getPolygonesFromShape(self.shape)

    def getLowestPoint(self):
        minZ = None
        polygons = ShapeToPoly.getPolygonesFromShape(self.shape)
        for poly in polygons:
            if poly.isInPlaneXY():
                for pnt in poly.points:
                    if not minZ or pnt.z < minZ.z:
                        minZ = pnt

        return minZ

    def getHighestPoint(self):
        maxZ = None
        polygons = ShapeToPoly.getPolygonesFromShape(self.shape)
        for poly in polygons:
            if poly.isInPlaneXY():
                for pnt in poly.points:
                    if not maxZ or pnt.z > maxZ.z:
                        maxZ = pnt

        return maxZ
