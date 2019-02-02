from Geometry import ShapeToPoly

class Structure(object):
    shape = None

    def __init__(self,shape):
        super(Structure, self).__init__()
        self.shape = shape


    def getBasePolygon(self):
        return ShapeToPoly.getShapeBasePolygon(self.shape)

    def getBasePolygons(self):
        return ShapeToPoly.getShapeBasePolygons(self.shape)

    def getXYPlanePolygons(self,minZ=None,maxZ=None):
        return ShapeToPoly.getShapeXYPlanePolygons(self.shape,minZ,maxZ)

    def getPolygons(self):
        return ShapeToPoly.getPolygonesFromShape(self.shape)

    def getLowestPoint(self):
        minZ = None
        polygons = ShapeToPoly.getPolygonesFromShape(self.shape)
        for poly in polygons:
            # if poly.isInPlaneXY():
            for pnt in poly.points:
                if not minZ or pnt.z < minZ.z:
                    minZ = pnt

        return minZ

    def getHighestPoint(self):
        maxZ = None
        polygons = ShapeToPoly.getPolygonesFromShape(self.shape)
        for poly in polygons:
            for pnt in poly.points:
                if not maxZ or pnt.z > maxZ.z:
                    maxZ = pnt

        return maxZ

    def getLowestZ(self):
        return self.getLowestPoint().z

    def getHighestZ(self):
        return self.getHighestPoint().z
