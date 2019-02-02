from Debugging.Logger import Logger


class Pnt3D(object):
    accuracy = 0.000001
    def __init__(self,x,y,z):
        super(Pnt3D, self).__init__()
        self.x = x
        self.y = y
        self.z = z


class Poly3D(object):
    points = []

    def __init__(self,pts):
        super(Poly3D, self).__init__()
        self.points = pts


    def isInPlaneXY(self,z=None):
        logger = Logger.getInstance()
        if z is None:
            z = self.points[0].z

        logger.log("NotSlabShapeException","z is: " + str(z) + "\n")
        for point in self.points:
            logger.log("NotSlabShapeException", "pnt: " + str(point.z) + " vs " + str(z) + "\n")
            if abs(point.z - z) > Pnt3D.accuracy:
                logger.log("NotSlabShapeException", "result: " + str(point.z - z) + "\n")
                logger.log("NotSlabShapeException","out\n")
                return False
        return True

    def isInPlaneXZ(self,y=None):
        if y is None:
            y = self.points[0].y
        for point in self.points:
            if point.y != y:
                return False
        return True

    def isInPlaneYZ(self,x=None):
        if x is None:
            x = self.points[0].x
        for point in self.points:
            if point.x != x:
                return False
        return True
