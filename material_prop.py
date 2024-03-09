'''
Get all the materials from the created sap_model object
To define the most common used concrete C30/37 from EC2 code for Singapore Industry Design
'''

def get_all_materials(sap_model):
    """
    Gets the materials in the current model. Will return in units mm, N & MPa.

    If the property type is either 'Concrete' or 'Steel', the function will
    be expanded so that the strength of materials are included.

    Returns
    materials : Type dict
    """
    # Set the Etabs units, all strength of materials will be returned in MPa
    sap_model.SetPresentUnits(9)
    # Etabs material type enumerators
    mat_types = {
        1: "Steel",
        2: "Concrete",
        3: "NoDesign",
        4: "Aluminum",
        5: "ColdFormed",
        6: "Rebar",
        7: "Tendon",
        8: "Masonry",
    }
    mat_name_list = sap_model.PropMaterial.GetNameList()
    materials = {}
    for i in range(mat_name_list[0]):
        mat_name = mat_name_list[1][i]
        mat_props = sap_model.PropMaterial.GetMaterial(mat_name)
        mat_type = mat_types[mat_props[0]]
        if mat_type == "Concrete":
            mat_conc_prop = sap_model.PropMaterial.GetOConcrete_1(mat_name)
            conc_fc = mat_conc_prop[0]
            materials[mat_name] = {
                "mat_name": mat_name,
                "mat_type": mat_type,
                "fc": conc_fc,
            }
        elif mat_type == "Steel":
            mat_steel_prop = sap_model.PropMaterial.GetOSteel_1(mat_name)
            steel_fy = mat_steel_prop[0]
            steel_fu = mat_steel_prop[1]
            materials[mat_name] = {
                "mat_name": mat_name,
                "mat_type": mat_type,
                "fy": steel_fy,
                "fu": steel_fu,
            }
        else:
            materials[mat_name] = {"mat_name": mat_name, "mat_type": mat_type}
    return materials


def add_concrete_material(sap_model): 
    # Material properties
    material_name = "C30/37"
    material_type = 2
    region = "Europe"
    standard = "EN 1992-1-1 per 206-1"
    grade = "C30/37"

    # Add concrete material to the model
    result = sap_model.PropMaterial.AddMaterial(material_name, material_type, region, standard, grade)

    # Check the return code
    ret = result[1] if isinstance(result, list) and len(result) > 1 else result

    if ret == 0:
        print(f"Concrete material '{material_name}' added successfully.")
    else:
        print(f"Error adding concrete material. Return code: {ret}")

def set_concrete_material(sap_model, existing_prop, new_prop):
    existing_prop = "C30/37"
    Fc = 32
    is_lightweight = False
    stress_strain_curve_type = 2
    SSHysType 
