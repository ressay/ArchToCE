
import ifcopenshell
ifc_file = ifcopenshell.open('D:\blida.ifc')
products = ifc_file.by_type('IfcProduct')
print(products)
for product in products :
 print(product.is_a())

#select a type from the ifc file
wall = ifc_file.by_type('IfcWall')
print(wall)

#lenght of walls from IFc
def print_element_quantities(element_quantity):
 for quantity in element_quantity.Quantities:
  print(quantity.Name)
  if quantity.is_a('IfcQuantityLength'):
   print(quantity.lengthValue)

#coordinates
if wall.ObjectPlacement.PlacementRelTo:
 # Inherit the coordinates of its parents
 pass
local_coordinates = wall.ObjectPlacement.RelativePlacement.Location[0]

#Geometry data
geometry = wall.Representation.Representations[0].Items[0] # An IfcExtrudedAreaSolid in this example
print(geometry.Position.Location[0]) # The centroid of the wall, so if the wall axis goes from (0, 0, 0) to (4, 0, 0) it will be (2, 0, 0)
print(geometry.ExtrudeDirection) # A vector pointing up (0, 0, 1)
print(geometry.Depth) # The height of the wall, say 3000
print(geometry.SweptArea) # A closed and filled area curve that can be extruded into a manifold, solid object
print(geometry.SweptArea.OuterCurve.Points) # the list of points that are in the polyline
