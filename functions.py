import ifcopenshell

def get_globalid(i):

    return i.GlobalId

def get_ifcproduct(i):

    return i.is_a()

def get_ifcproduct_name(i):

    name_list=[]

    #If Revit Export, remove BATid after colon
    if i.Name:
        if len(i.Name.split(':', 2 )) == 3:
            name_list.append(i.Name.split(':',2)[0] + ':' + i.Name.split(':',2)[1])
        else:
            name_list.append(i.Name)

    for i in name_list:
        return i

def get_type_name(i):

    if i.IsDefinedBy:
        for j in i.IsDefinedBy:
            if j.is_a('IfcRelDefinesByType'):
                if j.RelatingType.Name:
                    return j.RelatingType.Name

def get_building_storey(i):

    ifcproducts_without_building_storey = [     'IfcSite',
                                                'IfcBuilding',
                                                'IfcBuildingStorey',
                                                'IfcOpeningElement',
                                                'IfcSpace'
                                                ]

    if i.is_a() not in ifcproducts_without_building_storey:
        if i.ContainedInStructure:
            for contained_in_spatial_structure in  i.ContainedInStructure:
                if contained_in_spatial_structure.RelatingStructure.is_a('IfcBuildingStorey'):
                    return contained_in_spatial_structure.RelatingStructure.Name



def get_classification(i):

    if i.HasAssociations:
        for has_associations in i.HasAssociations:
            if has_associations.is_a('IfcRelAssociatesClassification'):
                return has_associations.RelatingClassification.ItemReference



def get_materials(i):

    #For future use to retrieve materials per object

    material_list = []
    if i.HasAssociations:
        for j in i.HasAssociations:
            if j.is_a('IfcRelAssociatesMaterial'):

                if j.RelatingMaterial.is_a('IfcMaterial'):
                    material_list.append(j.RelatingMaterial.Name)

                if j.RelatingMaterial.is_a('IfcMaterialList'):
                    for materials in j.RelatingMaterial.Materials:
                        material_list.append(materials.Name)


                if j.RelatingMaterial.is_a('IfcMaterialLayerSetUsage'):
                    for materials in j.RelatingMaterial.ForLayerSet.MaterialLayers:
                        material_list.append(materials.Material.Name)

                else:
                    pass

    return material_list

def get_thickness(i):

    for properties in i.IsDefinedBy:
        if properties.is_a('IfcRelDefinesByProperties'):
            if properties.RelatingPropertyDefinition.is_a('IfcPropertySet'):
                    if properties.RelatingPropertyDefinition.Name == "Dimensions":
                        for dimensions in properties.RelatingPropertyDefinition.HasProperties:
                            if dimensions.Name == "Thickness":
                                return dimensions.NominalValue[0]
                                continue


            if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                for quantities in properties.RelatingPropertyDefinition.Quantities:
                    if quantities.Name == 'Width':
                        return round(quantities.LengthValue, 0)
                        continue

            if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                for quantities in properties.RelatingPropertyDefinition.Quantities:
                    if quantities.Name == 'Thickness':
                        return round(quantities.LengthValue, 0)
                        continue

            if properties.RelatingPropertyDefinition.Name == "Construction":
                for properties in properties.RelatingPropertyDefinition.HasProperties:
                    if properties.Name == 'Thickness':
                        return round(properties.NominalValue[0], 0)



def get_height(i):

    for properties in i.IsDefinedBy:
        if properties.is_a('IfcRelDefinesByProperties'):

            if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):

                for quantities in properties.RelatingPropertyDefinition.Quantities:
                    if quantities.Name == 'Height':
                        return round(quantities.LengthValue, 0)
                        continue

                    #For Columns
                    if quantities.Name == 'Length':
                        return round(quantities.LengthValue, 0)
                        continue


            if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                for quantities in properties.RelatingPropertyDefinition.Quantities:
                    if quantities.Name == 'Height (Z Size)':
                        return round(quantities.LengthValue, 0)



def get_length(i):

    for properties in i.IsDefinedBy:
        if properties.is_a('IfcRelDefinesByProperties'):
            if properties.RelatingPropertyDefinition.is_a('IfcPropertySet'):
                    if properties.RelatingPropertyDefinition.Name == "Dimensions":
                        for dimensions in properties.RelatingPropertyDefinition.HasProperties:
                            if dimensions.Name == "Length":
                                return dimensions.NominalValue[0]
                                continue

            if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                for quantities in properties.RelatingPropertyDefinition.Quantities:
                    if quantities.Name == 'Length':
                        return round(quantities.LengthValue, 0)
                        continue

def get_width(i):

    for properties in i.IsDefinedBy:
        if properties.is_a('IfcRelDefinesByProperties'):
            if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                for quantities in properties.RelatingPropertyDefinition.Quantities:
                    if quantities.Name == 'Width':
                        return round(quantities.LengthValue, 0)

def get_area(i):

    for properties in i.IsDefinedBy:
        if properties.is_a('IfcRelDefinesByProperties'):
            if properties.RelatingPropertyDefinition:

                if properties.RelatingPropertyDefinition.is_a('IfcPropertySet'):
                    if properties.RelatingPropertyDefinition.Name == "Dimensions":
                        for dimensions in properties.RelatingPropertyDefinition.HasProperties:
                            if dimensions.Name == "Area":
                                return dimensions.NominalValue[0]
                                continue


            if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                for quantities in properties.RelatingPropertyDefinition.Quantities:

                    if quantities.Name == 'GrossSideArea':
                        return round(quantities.AreaValue, 3) #/1000000000
                        continue

                    if quantities.Name == 'GrossArea':
                        return quantities.AreaValue
                        continue

                    if quantities.Name == 'Area':
                        return quantities.AreaValue
                        continue

                    if quantities.Name == 'NetSideArea':
                        return quantities.AreaValue
                        continue

                    if quantities.Name == 'NetArea':
                        return quantities.AreaValue


def get_volume(i):

    for properties in i.IsDefinedBy:
        if properties.is_a('IfcRelDefinesByProperties'):

            if properties.RelatingPropertyDefinition.is_a('IfcPropertySet'):
                    if properties.RelatingPropertyDefinition.Name == "Dimensions":
                        for dimensions in properties.RelatingPropertyDefinition.HasProperties:
                            if dimensions.Name == "Volume":
                                return dimensions.NominalValue[0]
                                continue

            if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                for quantities in properties.RelatingPropertyDefinition.Quantities:
                    if quantities.Name == 'GrossVolume':
                        return round(quantities.VolumeValue, 3)
                        continue

                    if quantities.Name == 'NetVolume':
                        return round(quantities.VolumeValue, 3)
                        continue

                    if quantities.Name == 'Volume':
                        return round(quantities.VolumeValue, 3)
                        continue


                    if quantities.Name == 'Net Volume':
                        return round(quantities.VolumeValue, 3)




def get_perimeter(i):

    for properties in i.IsDefinedBy:
        if properties.is_a('IfcRelDefinesByProperties'):
            if properties.RelatingPropertyDefinition.is_a('IfcElementQuantity'):
                for quantities in properties.RelatingPropertyDefinition.Quantities:
                    if quantities.Name == 'Perimeter':
                        return round(quantities.LengthValue, 0)


def get_phase(i):

    for properties in i.IsDefinedBy:
        if properties.is_a('IfcRelDefinesByProperties'):
            if properties.RelatingPropertyDefinition.is_a('IfcPropertySet'):

                if properties.RelatingPropertyDefinition.Name == "Phasing":
                    for phasing in properties.RelatingPropertyDefinition.HasProperties:
                        return phasing.NominalValue[0]
                        continue

                if properties.RelatingPropertyDefinition.Name == "AC_Pset_RenovationAndPhasing":
                    for phasing in properties.RelatingPropertyDefinition.HasProperties:
                        return phasing.NominalValue[0]
                        continue

                if properties.RelatingPropertyDefinition.Name == "CPset_Phasing":
                    for phasing in properties.RelatingPropertyDefinition.HasProperties:
                        return phasing.NominalValue[0]

def ifcfile(filename):

    print ('IFC is being read')

    ifc_file = ifcopenshell.open(filename)

    project = ifc_file.by_type('IfcProject')

    products = ifc_file.by_type('IfcProduct')

    project_dict = []

    data_dict = collections.defaultdict(list)
    wall_dict = collections.defaultdict(list)
    floor_dict = collections.defaultdict(list)
    covering_dict = collections.defaultdict(list)
    beam_dict = collections.defaultdict(list)
    column_dict = collections.defaultdict(list)


    for j in project:
        project_dict.append(filename)
        project_dict.append(j.OwnerHistory.OwningApplication.ApplicationFullName)
        project_dict.append(j.OwnerHistory.OwningApplication.Version)
        project_dict.append(j.OwnerHistory.OwningUser.ThePerson.FamilyName)
        project_dict.append(j.OwnerHistory.OwningUser.TheOrganization.Name)
        project_dict.append(j.OwnerHistory.OwningUser.Roles)
        project_dict.append(j.Name)
        project_dict.append(j.Description)


    for i in products:

        data_dict[get_globalid(i)] = [  get_ifcproduct(i),
                                        get_ifcproduct_name(i),
                                        get_type_name(i),
                                        get_building_storey(i),
                                        get_classification(i),
                                        get_height(i),
                                        get_length(i),
                                        get_width(i),
                                        get_area(i),
                                        get_volume(i),
                                        get_perimeter(i),
                                        get_phase(i)
                                        ]

        if i.is_a().startswith('IfcWall'):
            wall_dict[get_globalid(i)] = [  get_ifcproduct(i),
                                            get_ifcproduct_name(i),
                                            get_type_name(i),
                                            get_building_storey(i),
                                            get_classification(i),
                                            get_height(i),
                                            get_length(i),
                                            get_width(i),
                                            get_area(i),
                                            get_volume(i),
                                            get_phase(i)
                                            ]
    return wall_dict
