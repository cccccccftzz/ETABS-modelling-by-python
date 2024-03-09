"""
ETABS draw slab by coordinates
"""

def draw_slab(sap_model, point_list, start_x_index, end_x_index, start_y_index, end_y_index, offset, z_coordinate, prop_name):
    # Extract corner points of the slab
    x1, y1 = point_list[start_x_index][start_y_index]
    x2, y2 = point_list[end_x_index][start_y_index]
    x3, y3 = point_list[end_x_index][end_y_index]
    x4, y4 = point_list[start_x_index][end_y_index]
    
    # Apply the offset
    x1 -= offset
    y1 -= offset
    x2 += offset
    y2 -= offset
    x3 += offset
    y3 += offset
    x4 -= offset
    y4 += offset

    # Create coordinates arrays
    x_coordinates = [x1, x2, x3, x4]
    y_coordinates = [y1, y2, y3, y4]
    z_coordinates = [z_coordinate] * 4

    # Define the slab name
    slab_name = ""

    # Add the slab to the ETABS model
    num_points = len(x_coordinates)
    _, _, _, slab_name, ret = sap_model.AreaObj.AddByCoord(num_points, x_coordinates, y_coordinates, z_coordinates, slab_name, prop_name)
    if ret == 0:
        print(f"Function AddByCoord was successful for slab {slab_name} with property {prop_name}")
    else:
        print(f"Error running function AddByCoord for slab {slab_name}")

    return slab_name


'''
    int AddByCoord(
	int NumberPoints,
	ref double[] X,
	ref double[] Y,
	ref double[] Z,
	ref string Name,
	string PropName = "Default",
	string UserName = "",
	string CSys = "Global"
)
    '''
    