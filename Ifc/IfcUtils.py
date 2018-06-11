
import ifcopenshell as ifc
from ifcopenshell import geom

settings = geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)

def getWallShapesFromIfc(fileName):

    f = ifc.open(fileName)
    # Get a list of all walls in the file
    walls = f.by_type("IfcWall")
    # Create a list of wall representation shapes
    wall_shapes = []

    for wall in walls:
        # print("doing stuff")
        shape = geom.create_shape(settings, wall).geometry
        if shape:
            # print("doing stuff22")
            wall_shapes.append((wall, shape))

    return wall_shapes

def getSlabShapesFromIfc(fileName):
    f = ifc.open(fileName)
    # Get a list of all walls in the file
    slabs = f.by_type("IfcSlab")
    # Create a list of wall representation shapes
    slab_shapes = []

    for slab in slabs:
        shape = geom.create_shape(settings, slab).geometry
        slab_shapes.append((slab, shape))

    return slab_shapes



def displayShapes(shapes):
    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display("qt-pyqt4")
    for shape in shapes:
        display.DisplayShape(shape)
    start_display()

