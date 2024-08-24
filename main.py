from create_object import *
from set_units import *
from create_grid_system import *
from draw_slab import *
from material_prop import *
from set_slab_prop import *
from get_storey_data import *
import comtypes.client

# Connect to Etabs model
etabs_object, sap_model = connect_to_etabs()
print_model_name(sap_model)
disconnect_from_etabs(etabs_object, sap_model)

# Set the present units kN for force and m for length
set_etabs_units(sap_model)

# Adding the most common used concrete C25/30, C30/37, C32/40, C40/50 from EC2 code for Singapore Industry Design
add_eurocode_conc_materials(sap_model, delete_existing=True)

# Adding the most common used rebar type fy=500Mpa from EC2 code for Singapore Industry Design
add_eurocode_rebar_materials(sap_model, delete_existing=True)

# Generate the grid line by given value
# storey_heights = [3.88, 3.88, 3.88]  #Only can set the two types of height
# x_coordinates = [0] + [8.1 * i for i in range(1, 8)]
# y_coordinates = [0] + [4.365, 8.73, 13.095]

# grid_points = create_grid_system(sap_model, storey_heights, x_coordinates, y_coordinates)
# print(grid_points)

# print(f'{get_story_data(sap_model) = }')
# '''get_story_data(sap_model) = [
#     ['Story3', 3.88, 11.64, True, None, False, 0.0],
#     ['Story2', 3.88, 7.76, False, 'Story3', False, 0.0],
#     ['Story1', 3.88, 3.88, False, 'Story3', False, 0.0],
#     ['Base', 0.0, 0.0, False, None, False, 0.0]]
# '''

# #Define concrete material C30/37
# add_concrete_material(sap_model)

# # Set slab properties
# slab_prop_name = "MyRC125mmSlab"
# ret = set_slab_prop(sap_model, slab_prop_name)

# # Add slabs
# slab_offset = 0
# prop_name = "MyRC125mmSlab"
# # balcony_axis = [[1, 3, 5, 7], [1, 3]]  # Offset horizontal indices by -1
# # balcony_width = 4
# # balcony_depth = 2
# # balcony_offset = 4.05

# for z, story_height in enumerate(storey_heights):
#     z_coordinate = sum(storey_heights[:z + 1]) #{1:3.88, 2:3.88, 3:3.88}
#     draw_slab(sap_model, grid_points, 0, len(x_coordinates) - 1, 0, len(y_coordinates) - 1, slab_offset, z_coordinate, prop_name)


# Close ETABS
# sap_application.ApplicationExit(False)
