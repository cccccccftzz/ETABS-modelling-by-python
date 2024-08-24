"""
Set units for ETABS model in terms of length and force.

Parameters:
- sap_model (object): ETABS model object.
- length (str, optional): Unit for length. Possible values are "m" (meters) or "mm" (millimeters). Default is "mm".
- force (str, optional): Unit for force. Possible values are "N" (Newtons) or "kN" (kiloNewtons). Default is "N".

Returns:
- None: The function does not return any value.

Raises:
- None: No specific exceptions are raised.

Example:
>>> sap_model = initialize_etabs_model()  # Replace with actual initialization function
>>> set_etabs_units(sap_model, length="m", force="kN")

Note:
- This function sets the units for an ETABS model based on the specified length and force units. 
- The length and force units determine the scale at which dimensions and loads are interpreted within the ETABS model.
- It is important to call this function before defining any model geometry or applying loads to ensure consistency in units.

Unit Codes:
- Length Units: "m" (meters) - 10, "mm" (millimeters) - 9
- Force Units: "N" (Newtons) - 10, "kN" (kiloNewtons) - 6
"""


def set_etabs_units(sap_model):
    ret = sap_model.SetPresentUnits(6)

    if ret == 0:
        print(f"The unit has been set.")
    else:
        print(f"Error setting the unit. Return code: {ret}")

    return None
