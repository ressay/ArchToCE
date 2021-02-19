from OCC.Core import TopoDS, Graphic3d, AIS, Bnd, BRepBndLib
from OCC.Core.TopoDS import TopoDS_Wire
import ifcopenshell.geom

from OCCUtils import Topology
import OCC
material = Graphic3d.Graphic3d_MaterialAspect(Graphic3d.Graphic3d_NOM_PLASTER)

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)



file = ifcopenshell.open("Mur.ifc")
walls = file.by_type("IfcWall")
bbox = OCC.Core.Bnd.Bnd_Box()
for wall in walls:
    product = ifcopenshell.geom.create_shape(settings, wall)
    shape = TopoDS.TopoDS_Iterator(product.geometry).Value()
    occ_display = ifcopenshell.geom.utils.initialize_display()
    ifcopenshell.geom.utils.display_shape(shape)
    shape_gpXYZ = shape.Location().Transformation().TranslationPart()
    print((shape_gpXYZ.X(), shape_gpXYZ.Y(), shape_gpXYZ.Z()))
    break
    # wire = TopoDS.topods_Wire(product)
    # explorer = Topology.WireExplorer(wire)
    # vertices = explorer.ordered_vertices()
    # for vertex in vertices:
    #     print vertex
input()