'''
Get all the materials from the created sap_model object
To define the most common used concrete C25/30, C30/37, C32/40, C40/50 from EC2 code for Singapore Industry Design
'''
import re

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

def add_eurocode_conc_materials(sap_model, delete_existing=False):
    """
    This will set all the concrete grades with material properties to Eurocode,
    C25/30, C30/37, C32/40, C40/50. The materials will have the
    designation 'EC-C32/40' etc.

    Parameters
    SapModel : Pointer (refer to function connect_to_etabs)
    delete_existing : Boolean. If True will delete all existing concrete
                      materials

    Returns None
    """
    conc_grades = ["C25/30", "C30/37", "C32/40","C40/50"]

    gravity_weight = 25.0  # kN/m³

    conc_mat_to_del = []
    # Get existing concrete materials to be deleted
    if delete_existing:
        all_materials = get_all_materials(sap_model)
        for mat in all_materials:
            if all_materials[mat]["mat_type"] == "Concrete":
                conc_mat_to_del.append(mat)

    # Delete materials
    for mat in conc_mat_to_del:
        prop_del = sap_model.PropMaterial.Delete(mat)
        if prop_del == 1:
            print("Deleting material {} unsuccessful".format(mat))

    # Add new Eurocode concrete materials
    for grade in conc_grades:
        conc_nm = "EC-" + grade
        numeric_part = re.search(r'\d+', grade).group()  # Extract numeric part using regex
        new_prop = sap_model.PropMaterial.AddMaterial(
            conc_nm, 2, "Europe", "EN 1992-1-1 per 206-1", grade, UserName=conc_nm
        )

        # Check if the material was added successfully
        if new_prop[1] != 0:
            print("Adding material {} unsuccessful. Return code: {}".format(conc_nm, new_prop[1]))
            continue

        isLightweight = False
        fcsFact = 0.0
        SSType = 2
        SSHysType = 4
        strainAtFc = 0.003
        strainAtUlt = 0.0035
        
        return_code = sap_model.PropMaterial.SetOConcrete(
            conc_nm,
            float(numeric_part),  # Convert to float
            isLightweight,
            fcsFact,
            SSType,
            SSHysType,
            strainAtFc,
            strainAtUlt,
        )
        if return_code != 0:
            print("Setting properties for material {} unsuccessful. Return code: {}".format(conc_nm, return_code))
            continue

        conc_E = {
            "C25/30": 31000,
            "C30/37": 33000,
            "C32/40": 33400,
            "C40/50": 35000
        }
        concU = 0.2
        concA = 10 * 10**-6
        return_code = sap_model.PropMaterial.SetMPIsotropic(conc_nm, conc_E[grade], concU, concA)
        if return_code != 0:
            print("Setting properties for material {} unsuccessful. Return code: {}".format(conc_nm, return_code))
            continue        
        
        sap_model.PropMaterial.SetWeightAndMass(conc_nm, 1, 25 * 10**-6)
        if return_code != 0:
            print("Setting properties for material {} unsuccessful. Return code: {}".format(conc_nm, return_code))
            continue 

        # Check if setting concrete properties was successful
        # Rest of the code...
        print("Material {} added successfully".format(conc_nm))

    return None

'''
def add_eurocode_rebar_materials(sap_model):
    return_code = sap_model.PropMaterial.SetORebar('fy500'), 300, 500, 375, 625, 1, 1, 0.01, 0.09, False, 0)
    print("Setting properties for material unsuccessful. Return code: {return_code}")
    continue 
'''

