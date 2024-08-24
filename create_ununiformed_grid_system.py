import comtypes.client


def create_custom_grid(sap_model, storey_heights, x_coordinates, y_coordinates):
    num_of_storeys = len(storey_heights)
    num_of_lines_x = len(x_coordinates)
    num_of_lines_y = len(y_coordinates)

    # Initialize ETABS model
    ret = sap_model.InitializeNewModel(6)
    """
    InitializeNewModel(ModelType)
    ModelType: An integer specifying the type of structural model to create.
    6: 3D Frame Model
    """
    if ret == 0:
        print("Function InitializeNewModel was successful")
    else:
        print("Error running function InitializeNewModel")

    # Create grid-only model
    ret = sap_model.File.NewGridOnly(
        num_of_storeys, 0, storey_heights[0], num_of_lines_x, num_of_lines_y, 0, 0
    )
    if (
        ret == 0
    ):  # If ret is 0, it usually means that the method executed successfully without any errors.
        print("Function NewGridOnly was successful")
    else:
        print("Error running function NewGridOnly")

    # Set custom spacings along X and Y directions
    for i in range(num_of_lines_x):
        sap_model.GridSys.SetGridSys("GridX{}".format(i + 1), x_coordinates[i], 0, 0)

    for j in range(num_of_lines_y):
        sap_model.GridSys.SetGridSys("GridY{}".format(j + 1), 0, y_coordinates[j], 0)

    return ret


# Define geometric parameters
storey_heights = [-1.5, 3.88, 3.88, 2.66]
x_coordinates = [0] + [8.1 * i for i in range(1, 8)]
y_coordinates = [0] + [4.365, 8.65, 4.365]

# Create custom grid-only model
create_custom_grid(sap_model, storey_heights, x_coordinates, y_coordinates)
