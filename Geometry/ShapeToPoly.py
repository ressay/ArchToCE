import OCC.Core.BRep
import OCC.Core.BRepBndLib
import OCC.Core.BRepBndLib
import OCC.Core.Bnd
import OCC.Core.Bnd
import OCC.Core.Geom
import OCC.Core.TopAbs
import OCC.Core.TopExp
import OCC.Core.TopoDS
import OCC.Core.gp


def getPolygonesFromShape(shape):
    from Geometry.Geom3D import Pnt3D,Poly3D

    exp = OCC.Core.TopExp.TopExp_Explorer(shape, OCC.Core.TopAbs.TopAbs_WIRE)  # .TopAbs_FACE)
    polygons = []
    while exp.More():
        wire = OCC.Core.TopoDS.topods.Wire(OCC.Core.TopoDS.topods.Wire(exp.Current()))
        exp.Next()
        points = []
        from OCCUtils import Topology
        explorer = Topology.WireExplorer(wire)
        vertices = explorer.ordered_vertices()
        for vertex in vertices:
            pnt = OCC.Core.BRep.BRep_Tool_Pnt(vertex)
            points.append(Pnt3D(pnt.X(),pnt.Y(),pnt.Z()))
        polygons.append(Poly3D(points))

    return polygons

def getShapeBasePolygon(shape):
    from Geometry.Geom2D import Pnt,Poly
    polygons = getPolygonesFromShape(shape)
    minZ = min([pnt.z for polygon in polygons for pnt in polygon.points])
    # print "min z: " + str(minZ)
    for polygon in polygons:
        points = []
        if polygon.isInPlaneXY(minZ):
            for pnt in polygon.points:
                points.append(Pnt(pnt.x, pnt.y))
            return Poly(points)
    return None

def getShapeBasePolygons(shape):
    from Geometry.Geom2D import Pnt,Poly
    polygons = getPolygonesFromShape(shape)
    minZ = min([pnt.z for polygon in polygons for pnt in polygon.points])
    polys = []()
    # print "min z: " + str(minZ)
    for polygon in polygons:
        points = []
        if polygon.isInPlaneXY(minZ):
            for pnt in polygon.points:
                points.append(Pnt(pnt.x, pnt.y))
            polys.append(Poly(points))
    return polys

def getShapeXYPlanePolygons(shape,minZ=None,maxZ=None):
    from Geometry.Geom2D import Pnt,Poly
    polygons = getPolygonesFromShape(shape)
    polys = []
    # print "min z: " + str(minZ)
    for polygon in polygons:
        points = []
        if polygon.isInPlaneXY():
            if minZ is not None and polygon.points[0].z < minZ:
                continue
            if maxZ is not None and polygon.points[0].z > maxZ:
                continue
            for pnt in polygon.points:
                points.append(Pnt(pnt.x, pnt.y))
            polys.append(Poly(points))
    return polys

def getBaseOfShapeZ(shape):
    polygons = getPolygonesFromShape(shape)
    return min([pnt.z for polygon in polygons for pnt in polygon.points])

def getTopOfShapeZ(shape):
    polygons = getPolygonesFromShape(shape)
    return max([pnt.z for polygon in polygons for pnt in polygon.points])

def getShapesBasePolygons(shapes):
    polys = []
    for shape in shapes:
        polys.append(getShapeBasePolygon(shape))

    return polys
