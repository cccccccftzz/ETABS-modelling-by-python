"""
The provided material properties module appears to be a Python script for interacting with a structural analysis software, possibly ETABS (Extended Three-dimensional Analysis of Building Systems). 
The module focuses on retrieving and modifying material properties, with a specific emphasis on concrete and steel materials.

Note:
- Please adjust the parameters as needed for your specific project and standards.
- Ensure that the material type, region, and standard align with your SAP model and requirements.

Author: Chen Fangting
Date: 13/Mar/2024
"""
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
    conc_grades = ["C25/30", "C30/37", "C32/40", "C40/50"]

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
        numeric_part = re.search(
            r"\d+", grade
        ).group()  # Extract numeric part using regex
        new_prop = sap_model.PropMaterial.AddMaterial(
            conc_nm, 2, "Europe", "EN 1992-1-1 per 206-1", grade, UserName=conc_nm
        )

        # Check if the material was added successfully
        if new_prop[1] != 0:
            print(
                "Adding material {} unsuccessful. Return code: {}".format(
                    conc_nm, new_prop[1]
                )
            )
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
            print(
                "Setting properties for material {} unsuccessful. Return code: {}".format(
                    conc_nm, return_code
                )
            )
            continue

        conc_E = {"C25/30": 31000, "C30/37": 33000, "C32/40": 33400, "C40/50": 35000}
        concU = 0.2
        concA = 10 * 10**-6
        return_code = sap_model.PropMaterial.SetMPIsotropic(
            conc_nm, conc_E[grade], concU, concA
        )
        if return_code != 0:
            print(
                "Setting properties for material {} unsuccessful. Return code: {}".format(
                    conc_nm, return_code
                )
            )
            continue

        sap_model.PropMaterial.SetWeightAndMass(conc_nm, 1, 25 * 10**-6)
        if return_code != 0:
            print(
                "Setting properties for material {} unsuccessful. Return code: {}".format(
                    conc_nm, return_code
                )
            )
            continue

        # Check if setting concrete properties was successful
        # Rest of the code...
        print("Material {} added successfully".format(conc_nm))

    return None


def add_eurocode_rebar_materials(sap_model, delete_existing=False):
    '''
    Adds Eurocode-compliant rebar material to the specified SAP model.

    Parameters:
    - sap_model: Pointer to the SAP model.
    - delete_existing (optional): If True, deletes existing rebar materials.

    Returns:
    None

    Workflow:
    - Deletes existing rebar materials if delete_existing is True.
    - Adds a new material for the rebar with Eurocode specifications:
        - Material type: 6 (Assuming material type 6 is suitable for rebar).
        - Region: "Europe" (Modify based on the appropriate region).
        - Standard: "User" (Modify based on the appropriate standard).
        - Grade designation: "Grade 500" (Customizable).
    - Sets isotropic mechanical properties for the rebar:
        - Elastic modulus (E): 200,000 MPa (Assuming E = 200 GPa).
        - Thermal coefficient: 0.
    - Sets Eurocode rebar material properties:
        - Yield strength (Fy), Ultimate strength (Fu), Elastic yield strain (Efy), Ultimate strain (Efu),
            Stress-strain type (SSType), Stress-strain hysteresis type (SSHysType),
            Strain at the start of hardening (StrainAtHardening), Strain at ultimate (StrainUltimate),
            Final slope (FinalSlope), UseCaltransSSDefaults, and Temperature (Temp).
    '''

    rebar_nm = "fy500"
    Fy = 500
    Fu = 540
    Efy = 500
    Efu = 540
    SSType = 1
    SSHysType = 1
    StrainAtHardening = 0.01
    StrainUltimate = 0.09
    FinalSlope = 0
    UseCaltransSSDefaults = False
    Temp = 0

    # List of existing rebar materials to be deleted
    rebar_mat_to_del = []

    # Get existing rebar materials to be deleted
    if delete_existing:
        all_materials = get_all_materials(sap_model)
        for mat in all_materials:
            if all_materials[mat]["mat_type"] == "Rebar":
                rebar_mat_to_del.append(mat)

    # Delete existing rebar materials
    for mat in rebar_mat_to_del:
        prop_del = sap_model.PropMaterial.Delete(mat)
        if prop_del == 1:
            print(f"Deleting material {mat} unsuccessful")

    # Add new material for the rebar
    new_prop = sap_model.PropMaterial.AddMaterial(
        rebar_nm,
        6,  # material type 6 is  for rebar
        "Europe",  # Add appropriate region
        "User",  # Add appropriate standard
        f"Grade 500",  # Customize as needed
        UserName=rebar_nm,
    )
    if new_prop[1] != 0:
        print(
            "Adding material {} unsuccessful. Return code: {}".format(
                rebar_nm, new_prop[1]
            )
        )

    # Set isotropic mechanical properties for the rebar
    return_code_isotropic = sap_model.PropMaterial.SetMPUniaxial(
        rebar_nm,
        200000,  # Elastic modulus (E) in MPa (200 GPa = 200,000 MPa)
        0,  # The thermal coefficient. [1/T]
        Temp=0,
    )
    if return_code_isotropic != 0:
        print(
            f"Set isotropic mechanical properties for rebar {rebar_nm} unsuccessful. Return code: {return_code}"
        )

    # Set Eurocode rebar material
    return_code = sap_model.PropMaterial.SetORebar_1(
        rebar_nm,
        Fy,
        Fu,
        Efy,
        Efu,
        SSType,
        SSHysType,
        StrainAtHardening,
        StrainUltimate,
        FinalSlope,
        UseCaltransSSDefaults,
        Temp,
    )

    if return_code != 0:
        print(
            f"Setting properties for material {rebar_nm} unsuccessful. Return code: {return_code}"
        )  # Return code 1 means didnt add the material for the rebar

    else:
        print(f"Material {rebar_nm} added successfully")

    return None
