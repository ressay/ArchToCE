from shapely.geometry import Polygon, Point

from Geometry.Geom2D import Poly, Pnt
from Skeleton.BoxSkeleton import BoxSkeleton

class ColumnSkeleton(BoxSkeleton):
    def __init__(self, poly,parent):
        super(ColumnSkeleton, self).__init__(poly)
        self.parentwall = parent
