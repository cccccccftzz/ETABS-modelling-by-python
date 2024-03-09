from create_object import *
from create_grid_system import *
from draw_slab import *
from material_prop import *
from set_slab_prop import *
from get_storey_data import *
import comtypes.client

#Connect to Etabs model
etabs_object, sap_model = connect_to_etabs()
print_model_name(sap_model)
disconnect_from_etabs(etabs_object, sap_model)

#Generate the grid line by given value
storey_heights = [3.88, 3.88, 3.88]  #Only can set the two types of height
x_coordinates = [0] + [8.1 * i for i in range(1, 8)]
y_coordinates = [0] + [4.365, 8.73, 13.095]

grid_points = create_grid_system(sap_model, storey_heights, x_coordinates, y_coordinates)
print(grid_points)

print(f'{get_story_data(sap_model) = }')
'''get_story_data(sap_model) = [
    ['Story3', 3.88, 11.64, True, None, False, 0.0], 
    ['Story2', 3.88, 7.76, False, 'Story3', False, 0.0], 
    ['Story1', 3.88, 3.88, False, 'Story3', False, 0.0], 
    ['Base', 0.0, 0.0, False, None, False, 0.0]]
'''

#To get all the materials
materials = get_all_materials(sap_model)
print(materials)
'''
{'A992Fy50': {'mat_name': 'A992Fy50', 'mat_type': 'Steel', 'fy': 344.737894475789, 'fu': 448.15926281852575}, 
 '4000Psi': {'mat_name': '4000Psi', 'mat_type': 'Concrete', 'fc': 27.57903155806312}, 
 'A615Gr60': {'mat_name': 'A615Gr60', 'mat_type': 'Rebar'}, 
 'A416Gr270': {'mat_name': 'A416Gr270', 'mat_type': 'Tendon'}}
'''

#Define concrete material C30/37
add_concrete_material(sap_model)



# Set slab properties
slab_prop_name = "MyRC125mmSlab"
ret = set_slab_prop(sap_model, slab_prop_name)

# Add slabs
slab_offset = 0
prop_name = "MyRC125mmSlab"
# balcony_axis = [[1, 3, 5, 7], [1, 3]]  # Offset horizontal indices by -1
# balcony_width = 4
# balcony_depth = 2
# balcony_offset = 4.05

for z, story_height in enumerate(storey_heights):
    z_coordinate = sum(storey_heights[:z + 1]) #{1:3.88, 2:3.88, 3:3.88}
    draw_slab(sap_model, grid_points, 0, len(x_coordinates) - 1, 0, len(y_coordinates) - 1, slab_offset, z_coordinate, prop_name)





# Close ETABS
# sap_application.ApplicationExit(False)