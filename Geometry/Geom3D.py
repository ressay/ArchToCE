
class Pnt3D(object):
    x = 0
    y = 0
    z = 0
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


    def isInPlaneXY(self):
        z = self.points[0].z
        for point in self.points:
            if point.z != z:
                return False
        return True

    def isInPlaneXZ(self):
        y = self.points[0].y
        for point in self.points:
            if point.y != y:
                return False
        return True

    def isInPlaneYZ(self):
        x = self.points[0].x
        for point in self.points:
            if point.x != x:
                return False
        return True
