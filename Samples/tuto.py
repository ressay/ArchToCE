import sys

from DrawUtils import QtGui, Window
from Ifc import IfcUtils

wall_shapes = IfcUtils.getWallShapesFromIfc("px+vl4.ifc")
shapes = []
for wall,shape in wall_shapes:
    shapes.append(shape)

polygons = IfcUtils.getWallsShapesBasePolygons(shapes)
lx = min([pnt.x for pnt in [pt for polygon in polygons for pt in polygon.points]])
ly = min([pnt.y for pnt in [pt for polygon in polygons for pt in polygon.points]])

for polygon in polygons:
    polygon.move(-lx,-ly)
    print ("polygon is: ")
    for pnt in polygon.points:
        print("point is: (%.2f, %.2f) " % (pnt.x, pnt.y))

app = QtGui.QApplication(sys.argv)
w = Window(polygons)
w.show()
IfcUtils.displayShapes(shapes)

sys.exit(app.exec_())

# polygon is:
# point is: (-11.72, -6.70)
# point is: (-11.72, 3.40)
# point is: (-11.52, 3.40)
# point is: (-11.52, -6.70)
# polygon is:
# point is: (-11.52, 3.40)
# point is: (-1.62, 3.40)
# point is: (-1.62, 3.20)
# point is: (-11.52, 3.20)