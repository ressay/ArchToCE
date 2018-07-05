from Geometry.Geom2D import Pnt
from Skeleton.PolySkeleton import PolySkeleton

class NotBoxError(Exception):
    pass
class BoxSkeleton(PolySkeleton):

    def __init__(self, poly,pnts = None):
        super(BoxSkeleton, self).__init__(poly)
        if pnts:
            self.topLeftPnt, self.vecLength, self.vecWidth = pnts
            return

        self.topLeftPnt = Pnt
        self.vecLength = Pnt
        self.vecWidth = Pnt
        if len(poly.points) != 4:
            raise NotBoxError("not four points")
        # else:
        #     pnts = poly.points
        #     for p in pnts:
        #         print p
        #     vec1 = pnts[0] - pnts[1]
        #     vec2 = pnts[3] - pnts[2]
        #     threshold = vec1.magn()*0.1
        #     print ("vec1: "+str(vec1)+" vec2: "+str(vec2))
        #     if not (abs(vec1.x() - vec2.x()) <= threshold and abs(vec1.y()-vec2.y()) <= threshold):
        #         raise NotBoxError("not parallel")
        self._getTopLeftPoint()

            
    def _getTopLeftPoint(self):
        pnts = self.poly.points
        minXpnt = min(pnts,key=lambda p: p.x())
        self.topLeftPnt = minXpnt
        index = 0
        for pnt in pnts:
            if minXpnt == pnt:
                break
            index += 1
        i1 = (index+1) % 4
        i2 = (index-1) % 4
        
        vec1 = pnts[i1] - minXpnt
        vec2 = pnts[i2] - minXpnt
        if vec1.magn() > vec2.magn():
            self.vecWidth = vec2
            self.vecLength = vec1
        else:
            self.vecWidth = vec1
            self.vecLength = vec2



    def getWidth(self):
        return self.vecWidth.magn()

    def getHeight(self):
        return self.vecLength.magn()

