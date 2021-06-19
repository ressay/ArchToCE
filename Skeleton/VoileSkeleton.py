#TODO change name
from shapely.geometry import Polygon, Point

from Geometry.Geom2D import Poly, Pnt
from Skeleton.BoxSkeleton import BoxSkeleton
# from Skeleton.WallSkeleton import WallSkeleton


class VoileSkeleton(BoxSkeleton):

    def __init__(self,parent,start,end):
        self.parentWall = parent
        self.start = start
        self.end = end
        poly = self.getPolyFromStartEnd(start,end)
        super(VoileSkeleton, self).__init__(poly)
        self.pointsList = None
        self.isPointValid = None
        self.surrondingBox = None
        self.surrondingBoxes = None


    def setParentWall(self,wallSkeleton,update=False):
        self.parentWall = wallSkeleton
        if update:
            return self.updateStartEnd()
        return True

    def getPolyFromStartEnd(self, start, end):
        parent = self.parentWall
        if parent.iscolumnParent:
            poly = parent.poly
        else:
            length = end - start
            newLengthVec = parent.vecLength.copy().resize(length)
            move = start
            moveVec = parent.vecLength.copy()
            moveVec.resize(move)
            topLeftPnt = parent.topLeftPnt + moveVec
            newWidthVec = parent.vecWidth.copy()
            pnt1 = topLeftPnt + newWidthVec
            pnt2 = pnt1 + newLengthVec
            pnt3 = topLeftPnt + newLengthVec
            poly = Poly([topLeftPnt, pnt1, pnt2, pnt3])
        return poly

    def updateStartEnd(self):
        self.surrondingBox = None
        parent = self.parentWall
        vecL = parent.vecLength
        topLeftPnt = parent.topLeftPnt
        vecs = []
        for pnt in self.poly.points:
            vec = pnt - topLeftPnt
            if vec.isParallel(vecL,0.005):
                vecs.append(vec)
        if len(vecs) != 2:
            print(("ERROR UPDATE START END VOILESKELETON: NUMBER OF"
                  " PARALLEL VECTORS EXPECTED: 2, FOUND: ",len(vecs)))
            return False
        print('INFO UPDATE START END VOILESKELETON: CORRECT NUMBER')
        self.start = min([vecs[0].magn(), vecs[1].magn()])
        self.end = max([vecs[0].magn(), vecs[1].magn()])
        return True

    def getLength(self):
        return self.end - self.start

    def getLengthX(self):
        return abs(self.vecLength.x())

    def getLengthY(self):
        return abs(self.vecLength.y())

    def copy(self):
        voile = VoileSkeleton(self.parentWall, self.start, self.end)
        voile.evalData = self.evalData
        return voile

    def getStartPoint(self):
        return self.topLeftPnt

    def getEndPoint(self):
        return self.topLeftPnt + self.vecLength

    # def startIsValid(self):
    #     self.isStartValid = True
    #
    # def endIsValid(self):
    #     self.isEndValid = True

    def getPointsList(self):
        if not self.pointsList:
            self.pointsList = [self.getStartPoint(),self.getEndPoint()]
            self.isPointValid = [False for p in self.pointsList]
        return self.pointsList

    def setPointValid(self,index):
        self.isPointValid[index] = True

    def getSurrondingBox(self, d_ratio):
        if self.surrondingBox:
            return self.surrondingBox
        # distance = 4*d_ratio
        # wid = Pnt(self.vecLength.y(),-self.vecLength.x())
        # # if distance == 0 or self.vecWidth.magn() == 0:
        # #     print ("distance: ", distance, "vecWidth: ", self.vecWidth.magn())
        # wid = wid.copy().resize(distance)*2 + wid.copy().resize(self.vecWidth.magn())
        # # leng = self.vecLength.copy().resize(distance)*2 + self.vecLength
        # leng = self.vecLength
        # center = self.topLeftPnt + self.vecLength/2 + self.vecWidth/2
        # pnt1 = center - leng/2 - wid/2
        # pnts = [pnt1, pnt1 + leng, pnt1 + leng + wid, pnt1 + wid]
        # polyPnts = [[pnt.x(),pnt.y()] for pnt in pnts]
        # polygon = Polygon(polyPnts)
        # p = center - leng/2
        # p = Point(p.x(),p.y())
        # p2 = center + leng/2
        # p2 = Point(p2.x(),p2.y())
        # print("here D value",distance+self.vecWidth.magn()/2)
        # circle = p.buffer(distance+self.vecWidth.magn()/2)
        # circle2 = p2.buffer(distance+self.vecWidth.magn()/2)
        # result = polygon.union(circle).union(circle2)

        Height=6
        parentwall=self.parentWall
        if parentwall.iscolumnParent:
            if self.vecWidth.y() == 0:
                wid = VoileSkeleton.realValue(abs(self.vecWidth.x()), Height)
                len = VoileSkeleton.realValue(abs(self.vecLength.y()), Height)
                pnt1 = Point(self.poly.centroid().x + 0.5 * wid, self.poly.centroid().y - 0.5 * len)
                pnts = [pnt1, Point(pnt1.x, pnt1.y + len), Point(pnt1.x - wid, pnt1.y + len),
                        Point(pnt1.x - wid, pnt1.y)]
            elif self.vecWidth.y() != 0:
                wid = VoileSkeleton.realValue(abs(self.vecWidth.y()), Height)
                len = VoileSkeleton.realValue(abs(self.vecLength.x()), Height)
                pnt1 = Point(self.poly.centroid().x +0.5* len, self.poly.centroid().y -0.5* wid)
                pnts = [pnt1, Point(pnt1.x, pnt1.y +  wid), Point(pnt1.x - len, pnt1.y + wid),
                            Point(pnt1.x - len, pnt1.y)]
            result = Polygon(pnts)
        else:
            if self.vecWidth.y() == 0:
                wid = abs(self.vecWidth.x())
                len = abs(self.vecLength.y())
                pnt1 = Point(self.poly.centroid().x + 1.2, self.poly.centroid().y - 1.2 - 0.5 * len)
                pnts = [pnt1, Point(pnt1.x, pnt1.y + len + 2.4), Point(pnt1.x - 2.4, pnt1.y + len + 2.4),
                        Point(pnt1.x - 2.4, pnt1.y)]
                result = Polygon(pnts)
            elif self.vecWidth.y() != 0:
                wid = abs(self.vecWidth.y())
                len = abs(self.vecLength.x())
                pnt1 = Point(self.poly.centroid().x - 1.2-0.5*len, self.poly.centroid().y +1.2)
                pnts = [pnt1, Point(pnt1.x+ len+2.4, pnt1.y ), Point(pnt1.x + len+2.4, pnt1.y -2.4),
                        Point(pnt1.x, pnt1.y-2.4)]
                result = Polygon(pnts)

        self.surrondingBox = result
        return result

    @staticmethod
    def realValue(dist, Height):
        check=Height/3
        dist=round(dist,2)
        if 0 < check <= 1: ind = (dist - 0.3) / 0.15
        if 1 < check <= 2: ind = (dist - 0.35) / 0.15
        if 2 < check <= 3: ind = (dist - 0.4) / 0.15
        if 3 < check <= 4: ind = (dist - 0.45) / 0.15
        if 4 < check <= 7: ind = (dist - 0.5) / 0.15
        realvalues=(4.5,6,7.5,9,10.5,12)
        return realvalues[int(ind)]
    def getSurrondingBoxes(self,selected=None):
        if self.surrondingBoxes:
            return self.surrondingBoxes
        if selected is None:
            selected = [1,1,1,1]
        distance = 4
        distance2 = 1
        wid = Pnt(self.vecLength.y(),-self.vecLength.x())
        wid2 = wid.copy().resize(distance2)*2 + wid.copy().resize(self.vecWidth.magn())
        wid1 = wid.copy().resize(distance)*2 + wid.copy().resize(self.vecWidth.magn())
        # leng = self.vecLength.copy().resize(distance)*2 + self.vecLength
        leng = self.vecLength
        center = self.topLeftPnt + self.vecLength/2 + self.vecWidth/2

        if selected[0]:
            wid = wid1
        else:
            wid = wid2
        pnt1 = center - leng / 2 - wid / 2
        pnts = [pnt1, pnt1 + leng, pnt1 + leng + wid/2, pnt1 + wid/2]
        polygon = Polygon([[pnt.x(), pnt.y()] for pnt in pnts])

        if selected[1]:
            wid = wid1
        else:
            wid = wid2
        pnt1 = center - leng / 2 + wid / 2
        pnts = [pnt1, pnt1 + leng, pnt1 + leng - wid/2, pnt1 - wid/2]
        polygon2 = Polygon([[pnt.x(), pnt.y()] for pnt in pnts])

        if selected[2]:
            d = distance
        else:
            d = distance2
        p = center - leng/2
        p = Point(p.x(),p.y())
        circle = p.buffer(d+self.vecWidth.magn()/2)

        if selected[3]:
            d = distance
        else:
            d = distance2
        p2 = center + leng / 2
        p2 = Point(p2.x(), p2.y())
        circle2 = p2.buffer(d+self.vecWidth.magn()/2)

        result = [polygon,polygon2,circle,circle2]
        self.surrondingBoxes = result
        return result
