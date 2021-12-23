import time
from pyModbusTCP.client import ModbusClient

#===================================================================================
# FACTORY_IO_PICK_AND_PLACE_ROBOT Function block
# 
# This function block controls the PICK_AND_PLACE_ROBOT, part of the simulation 
# developed for the FactoRIS project. 
# URL: https://github.com/DIGI2-FEUP/TF4iM/blob/main/factory_io/FactoRIS%20-%20Zero%20Defects.factoryio
#
# Dependencies required:
# pip3 install pyModbusTCP
# 
# @type  host: string
# @param host: The URL of TCP Modbus server to connect.
# 
# @type  port: integer
# @param port: TCP Modbus port (default 502)
# 
# @type  discard: boolean
# @param discard: If true, robot will dicard a part
# 
# @organization: DIGI2 Lab, FEUP
# @author: Luís Neto
# @contact: lcneto@fe.up.pt
# @license: GPLv3
# @date: 30-11-2021
# @version: V1.0.1
#===================================================================================

"""
The following classes represent objects in the Factory I/O simulation.
Each class has its own Modbus TCP client.
"""
class two_axis_pick_and_place:
    def __init__(self, name, x_coil, z_coil, grab_coil,
    mov_x_input, mov_z_input, obj_detected_input):
        self.name = name
        self.x_coil = x_coil
        self.z_coil = z_coil
        self.grab_coil = grab_coil
        self.mov_x_input = mov_x_input
        self.mov_z_input = mov_z_input
        self.obj_detected_input = obj_detected_input
        self.client = ModbusClient(host="127.0.0.1", port=502)

    def discard(self):
        self.client.open()

        self.client.write_single_coil(self.z_coil, True)
        moving_z = True
        while(moving_z):
            moving_z = self.client.read_discrete_inputs(self.mov_z_input, 1)[0]
            time.sleep(1)
        self.client.write_single_coil(self.grab_coil, True)
        time.sleep(1)
        self.client.write_single_coil(self.z_coil, False)
        time.sleep(1)
        moving_z = True
        while(moving_z):
            moving_z = self.client.read_discrete_inputs(self.mov_z_input, 1)[0]
            time.sleep(1)
        time.sleep(1)
        self.client.write_single_coil(self.x_coil, True)
        moving_x =  True
        while(moving_x):
             moving_x = self.client.read_discrete_inputs(self.mov_x_input, 1)[0]
             time.sleep(1)
        self.client.write_single_coil(self.grab_coil, False)
        time.sleep(1)
        object = True
        while(object):
             object = self.client.read_discrete_inputs(self.obj_detected_input, 1)[0]
             time.sleep(1)
        self.client.write_single_coil(self.x_coil, False)
        moving_x = True
        while(moving_x):
             moving_x = self.client.read_discrete_inputs(self.mov_x_input, 1)[0]
             time.sleep(1)
        self.client.close()
        return True

    def reset(self):
         self.client.write_single_coil(self.z_coil, False)
         self.client.write_single_coil(self.x_coil, False)
         self.client.write_single_coil(self.grab_coil, False)

"""
This is the Function Block class.
"""
class FACTORY_IO_PICK_AND_PLACE_ROBOT:
    
    def __init__(self):
        self.robot = None
        self.finished = True

    def schedule(self, event_name, event_value,
        host, port, discard):
        if event_name == 'INIT':
            self.host = host
            self.port = port
            # Instantiate all simulation objects
            # Coil and register IDs are hard coded for now.
            # To see each coil and register ID, open the Factory I/O simulation
            # go to File->Drivers and select Modbus TCP/IP Server to see the mapping.
            self.robot = two_axis_pick_and_place("robot", 8, 9, 10, 1, 0, 2)
            # Reset all objects to avoid problems with Factory I/O running previously
            self.robot.reset()
            return [event_value, None, self.finished]

        elif event_name == 'RUN':
            # The following code is the Finite State Machine that controls the robot.
            # This block works like a service, it will be called whenever the RUN event
            # is triggered. If discard is True, the  robot will discard the part.
            if discard == True and self.finished:
                self.finished = False
                print("Robot waiting: ", self.finished)
            elif discard == True and self.finished == False:
                self.finished = self.robot.discard()
                print("Wait for robot: ", self.finished)
            elif discard == False and self.finished == False:
                pass
                print("Wait for robot: ", self.finished)
            else:
                self.finished = True
                print("Robot done: ", self.finished)
            return [None, event_value, self.finished]