from create_object import *
from create_grid_system import *

#Connect to Etabs model
etabs_object, sap_model = connect_to_etabs()
print_model_name(sap_model)
disconnect_from_etabs(etabs_object, sap_model)

#Create the grid line system
storey_heights = [3.88, 3.88, 3.88]  #Only can set the two types of height
x_coordinates = [0] + [8.1 * i for i in range(1, 8)]
y_coordinates = [0] + [4.365, 4.365, 4.365]

grid_points = create_grid_system(sap_model, storey_heights, x_coordinates, y_coordinates)
