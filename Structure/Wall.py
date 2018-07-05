from Structure import Structure

class Wall(Structure):

    def __init__(self,shape):
        super(Wall, self).__init__(shape)


    def isSupporting(self,slab):
        tolerance = 0.2
        lowestW = self.getLowestPoint()
        lowestS = slab.getLowestPoint()
        if lowestW.z < lowestS.z:
            if self.getHighestPoint().z >= lowestS.z-tolerance and self._isUnderSlab(slab):
                return True

        return False

    def _isUnderSlab(self,slab):
        polW = self.getBasePolygon()
        polS = slab.getBasePolygon()
        return polS.intersects(polW)