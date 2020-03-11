import ifcopenshell
ifc_file = ifcopenshell.open(r'C:\Users\lenovo\Desktop\PFE\blida.ifc')
products = ifc_file.by_type('IfcWall')
print(products)
for product in products :
    print(product.is_a())
wall = ifc_file.by_type('IfcWall')[0]
for definition in wall.IsDefinedBy:
    related_data = definition.RelatingPropertyDefinition
    if related_data.is_a('IfcPropertySet'):
        pass
    elif related_data.is_a('IfcElementQuantity'):
        print_element_quantities(related_data)

def print_element_quantities(element_quantity):
 for quantity in element_quantity.Quantities:
  print(quantity.Name)
  if quantity.is_a('IfcQuantityLength'):
   print(quantity.lengthValue)


 print_element_quantities(product.IfcQuantityLength)
