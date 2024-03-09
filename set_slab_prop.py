import comtypes.client

def set_slab_prop(sap_model, prop_name):
    """
    Set slab property in ETABS.

    Parameters:
    - sap_model: ETABS model object.
    - prop_name: Name of the slab property.

    Returns:
    - ret: Return value indicating success (0) or failure (nonzero).
    """
    SlabType = 0  # eSlabType: Normal slab
    ShellType = 1  # eShellType.ShellThin->1,ShellThin->2, Membrane->3
    MatProp = "C30/37"  # You may need to adjust the material property name based on your ETABS model
    Thickness = 0.125  # Thickness in meters (125mm converted to meters)
    Color = -1  # Optional color, set to -1 for default
    Notes = ""  # Optional notes, leave empty for default
    GUID = ""  # Optional GUID, leave empty for default

    ret = sap_model.PropArea.SetSlab(prop_name, SlabType, ShellType, MatProp, Thickness, Color, Notes, GUID)
    return ret

