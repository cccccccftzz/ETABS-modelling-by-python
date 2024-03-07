"""
ETABS Connection Script

This script is designed to connect to an active instance of the ETABS (Extended 3D Analysis of Building Systems) software using its COM (Component Object Model) API. 
The script performs the following steps:

1. Connect to ETABS:
   - Create an API helper object.
   - Attach to a running instance of ETABS using the helper object.
   - Obtain the active ETABS object and create a SapModel object.
   - Return the ETABS object and SapModel object.

2. Print Model Name:
   - Takes a SapModel object as a parameter.
   - Uses the GetModelFilename method to retrieve and print the name of the ETABS model file.

3. Disconnect from ETABS:
   - Takes the ETABS object, SapModel object, and an optional 'close' parameter.
   - If 'close' is True, calls ApplicationExit to exit ETABS.
   - Clears the SapModel and ETABS object variables.

Usage:
1. Open an ETABS file from any folder.
2. Run the function connect_to_etabs() to establish a connection.
3. Check if the model name and path are printed to confirm successful connection.
4. Perform other operations as needed.
5. Run disconnect_from_etabs() to disconnect from the ETABS model.

Note: Ensure that comtypes is installed and a running instance of ETABS is available.

Author: Chen Fangting
Date: 07/Mar/2024
"""

import os #os module provides a way to interact with the operating system (e.g., file paths, environment variables).
import sys #sys module provides access to some variables and functions related to the Python runtime environment.
import comtypes.client #comtypes.client module allows interaction with COM (Component Object Model) objects in Windows.

def connect_to_etabs():
    #create a API helper object 
    helper = comtypes.client.CreateObject('ETABSv1.Helper')  #Create a COM object and return an interface pointer to it.
    helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)

    #attach to a running instance of ETABS 
    try:
        #get the active ETABS object
        my_etabs_object = helper.GetObject('CSI.ETABS.API.ETABSObject')
    except (OSError, comtypes.COMError): 
        '''
        If either of these exceptions occurs: 
        1.OSError: This exception is raised when an operating system-related error occurs 
        2. comtypes.COMError: This exception is raised when there is an error related to COM (Component Object Model) objects, 
        which are used for inter-process communication in Windows.
        '''
        print('No running instance of the programme found or failed or failed to attach.')
        sys.exit(-1) #The argument -1 indicates an abnormal exit status.When this line is executed, the Python script terminates immediately.
    
    #create an associated SapModel object
    sap_model = my_etabs_object.SapModel
    return my_etabs_object, sap_model
    

def print_model_name(sap_model_object):
    model_name = sap_model_object.GetModelFilename() #GetModelFilename() method applies to a SapModel instance i.e. sap_model_object here
    print(model_name)


def disconnect_from_etabs(etabs_object, sap_model, close = False):
    if close:
        etabs_object.ApplicationExit(False)
    sap_model = None #Clear the variable
    etabs_object = None #Clear the variable

#Test rows below:
etabs_object, sap_model = connect_to_etabs()
print_model_name(sap_model)
disconnect_from_etabs(etabs_object, sap_model)




