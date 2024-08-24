import comtypes.client


def set_grid_system(sap_model, name, x, y, rz):
    """
    Set or modify a grid system in ETABS.

    Parameters:
    - sap_model: ETABS model object.
    - name: Name of the grid system.
    - x: Global X grid of the origin of the grid system.
    - y: Global Y grid of the origin of the grid system.
    - rz: Rotation of an axis of the new grid system relative to the global grid system (degrees).

    Returns:
    - ret: Return value indicating success (0) or failure (nonzero).
    """
    ret = sap_model.GridSys.SetGridSys(name, x, y, rz)
    return ret


# Test row below
# Set or modify grid system
grid_system_name = "GridSysA"
x_coordinate = 1000
y_coordinate = 1000
rotation_angle = 0

ret = set_grid_system(
    sap_model, grid_system_name, x_coordinate, y_coordinate, rotation_angle
)
