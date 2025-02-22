import time
import queue
import numpy as np
from pyModbusTCP.client import ModbusClient

#===================================================================================
# FACTORY_IO_SORTING Function block
# 
# This function block controls the Factory IO simulation developed for the FactoRIS
# project. 
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
# @organization: DIGI2 Lab, FEUP
# @author: Lu�s Neto
# @contact: lcneto@fe.up.pt
# @license: GPLv3
# @date: 30-11-2021
# @version: V1.0.1
#===================================================================================

"""
The following classes represent objects in the Factory I/O simulation.
Each class has its own Modbus TCP client.
"""
class conveyor:
    def __init__(self, name, modbus_coil, host, port):
        self.name = name
        self.modbus_coil = modbus_coil
        self.client = ModbusClient(host=host, port=port, auto_open=True, auto_close=True)

    def start(self):
        self.client.write_single_coil(self.modbus_coil, True)

    def stop(self):
        self.client.write_single_coil(self.modbus_coil, False)

class sorter:
    def __init__(self, name, open_close_coil, move_belt_coil, host, port):
        self.name = name
        self.open_close_coil = open_close_coil
        self.move_belt_coil = move_belt_coil
        self.client = ModbusClient(host=host, port=port, auto_open=True, auto_close=True)

    def divert(self):
        self.client.write_single_coil(self.open_close_coil, True)
        self.client.write_single_coil(self.move_belt_coil, True)

    def reset(self):
        self.client.write_single_coil(self.open_close_coil, False)
        self.client.write_single_coil(self.move_belt_coil, False)

class boolean_sensor:
    def __init__(self, name, discrete_input, host, port):
        self.name = name
        self.discrete_input = discrete_input
        self.client = ModbusClient(host=host, port=port, auto_open=True, auto_close=True)

    def value(self):
        return self.client.read_discrete_inputs(self.discrete_input)[0]

class register_sensor:
    def __init__(self, name, register_input, host, port):
        self.name = name
        self.register_input = register_input
        self.client = ModbusClient(host=host, port=port, auto_open=True, auto_close=True)

    def value(self):
        return self.client.read_input_registers(self.register_input, 1)[0]

"""
This is the Function Block class.
"""
class FACTORY_IO_SORTING:
    
    def __init__(self):
        # Vision sensor variable
        self.vision_value = 0
        self.last_vision_value = 0
        self.discard = False
        self.state = 1
        self.diverter = None
        self.fsm_states = {}
        self.item_color_queue = queue.Queue()
        self.first_group = None
        self.second_group = None
        self.third_group = None

    def simulation_running(self):
        client = ModbusClient(self.host, self.port, auto_open=True, auto_close=True)
        return client.read_discrete_inputs(5)[0]


    def state_1(self, event_value, discard_finished):
        # While the vision sensor does not detect a part, roll the entry conveyor
        self.entry_conveyor.start()
        self.vision_value = self.vision_sensor.value()
        while(self.vision_value == 0):
            self.vision_value = self.vision_sensor.value()
            #print("Vision sensor value: ", self.vision_value)
        self.item_color_queue.put(self.vision_value)
        # Update state
        self.state = 2
        return [None, event_value, False]

    def state_2(self, event_value, discard_finished):
        # While the robot sensor does not detect a part, roll the entry conveyor
        self.entry_conveyor.start()
        object_present = False
        while(object_present == False):
            object_present = self.object_sensor.value()
            #print("Object sensor value: ", object_present)
        #self.entry_conveyor.stop()
        # Update state
        self.state = 3
        return [None, event_value, False]

    def state_3(self, event_value, discard_finished):
        self.entry_conveyor.start()
        self.vision_value = self.item_color_queue.get()
        # Parts to discard
        if (self.vision_value not in self.first_group and 
            self.vision_value not in self.second_group and 
            self.vision_value not in self.third_group):
            self.entry_conveyor.stop()
            #print("Robot discard material.")
            self.discard = True
            self.vision_value = 0
            # Update state
            self.state = 4
            return [None, event_value, True]
        # Parts to sort
        else:
            self.exit_conveyor.start()
            self.diverter = None
            # Blue part to be sorted
            if self.vision_value in self.first_group:
                self.diverter = self.blue_sorter
            # Green part to be sorted
            elif self.vision_value in self.second_group:
                self.diverter = self.green_sorter
            # Grey part to be sorted
            elif self.vision_value in self.third_group:
                self.diverter = self.grey_sorter
            self.vision_value = 0
            # Update state
            self.state = 6
            return [None, event_value, False]

    def state_4(self, event_value, discard_finished):
        # DINASORE does not allow to implement synchronism between SENSOR and SERVICE FB's
        # This initial code checks the discard flag to know if it needs to synchronize 
        # with the FACTORY_IO_PICK_AND_PLACE_ROBOT FB.
        # If it does, it must set the flag to False and return again to indicate the 
        # FACTORY_IO_PICK_AND_PLACE_ROBOT must synchronize.
        if self.discard == True:
            self.discard = False
        self.state = 5
        return [None, event_value, True]

    def state_5(self, event_value, discard_finished):
        #print("Discard is: ", discard_finished)
        self.vision_value = self.vision_sensor.value()
        if(self.vision_value > 0):
            self.item_color_queue.put(self.vision_value)
        # While the robot is not finished, loop
        while not discard_finished:
            time.sleep(0.2)
            #print("Waiting for robot.")
            return [None, event_value, False]
        # Robot finished and new item in robot place
        if(self.vision_value > 0):
            # Update state
            self.state = 2
            return [None, event_value, False]
        else:
            # Update state
            self.state = 1
            return [None, event_value, False]

    def state_6(self, event_value, discard_finished):
        # Activate correct sorter/diverter
        self.diverter.divert()
        # Inverse logic sensor, while True part is not in the exit ramp
        exit_object = True
        # Variable to keep track of items that cross the vision sensor while in this state
        self.last_vision_value = 0
        while exit_object == True:
            exit_object = self.exit_sensor.value()
            self.last_vision_value = self.vision_sensor.value()
            if(self.last_vision_value > 0):
                # Update state
                self.state = 7
                return [None, event_value, False]
            #print("Exit sensor value: ", exit_object)
        self.entry_conveyor.stop()
        # Update state
        self.state = 9
        return [None, event_value, False]

    def state_7(self, event_value, discard_finished):
        # Inverse logic sensor, while True part is not in the exit ramp
        exit_object = True
        object_present = True
        while exit_object == True:
            exit_object = self.exit_sensor.value()
            object_present = self.object_sensor.value()
            if(object_present == False):
                if(self.last_vision_value > 0):
                    # Object past vision sensor while in last state, make this current color to evaluate
                    self.vision_value = self.last_vision_value
                    # Reset last item
                    self.last_vision_value = 0
                    # Queue the item color
                    self.item_color_queue.put(self.vision_value)
                # Update state
                self.state = 8
                return [None, event_value, False]
            #print("Exit sensor value: ", exit_object)
        self.entry_conveyor.stop()
        # Update state
        self.state = 9
        return [None, event_value, False]

    def state_8(self, event_value, discard_finished):
        # Make sure part is in the exit conveyor before stopping it
        exit_object = True
        object_present = False
        while exit_object == True and object_present == False:
            object_present = self.object_sensor.value()
            exit_object = self.exit_sensor.value()
            self.last_vision_value = self.vision_sensor.value()
        # Check if some item crossed thw color sensor meanwhile
        if(self.last_vision_value > 0 and self.last_vision_value != self.vision_value):
            # Object past vision sensor while in last state, make this current color to evaluate
            self.vision_value = self.last_vision_value
            # Reset last item
            self.last_vision_value = 0
            # Queue the item color
            self.item_color_queue.put(self.vision_value)
        # Stop entry conveyor
        self.entry_conveyor.stop()
        # Make sure part is in the exit ramp
        while exit_object == True:
            exit_object = self.exit_sensor.value()
        # Update state
        self.state = 9
        return [None, event_value, False]

    def state_9(self, event_value, discard_finished):
        # Make sure part left the conveyor to close the sorter
        exit_object = False
        while exit_object == False:
            exit_object = self.exit_sensor.value()
            #print("Exit sensor value: ", exit_object)
        # Stop exist conveyor and reset sorter
        self.exit_conveyor.stop()
        self.diverter.reset()
        self.vision_value = 0
        # Item left in correct ramp and new item in robot place
        if(self.object_sensor.value() == True):
            # Update state
            self.state = 3
            return [None, event_value, False]
        # Item left in correct ramp and new item already past vision sensor
        elif(self.object_sensor.value() == False and self.last_vision_value > 0):
            # Object past vision sensor while in last state, make this current color to evaluate
            self.vision_value = self.last_vision_value
            self.entry_conveyor.start()
            # Update state
            self.state = 2
            return [None, event_value, False]
        # Item left in correct ramp and new item before robot
        else:
            # Update state
            self.state = 1
            return [None, event_value, False]
        
    def schedule(self, event_name, event_value,
        host, port, 
        first_group, second_group, third_group,
        discard_finished):
        if event_name == 'INIT':
            # Store modbus host and port
            self.host = host
            self.port = port

            # Convert group of items into list of items
            self.first_group = np.fromstring(first_group, dtype=int, sep=',')
            self.second_group = np.fromstring(second_group, dtype=int, sep=',')
            self.third_group = np.fromstring(third_group, dtype=int, sep=',')

            # Instantiate all simulation objects
            # Coil and register IDs are hard coded for now.
            # To see each coil and register ID, open the Factory I/O simulation
            # go to File->Drivers and select Modbus TCP/IP Server to see the mapping.
            self.entry_conveyor = conveyor("entry", 0, self.host, self.port)
            self.exit_conveyor = conveyor("exit", 1, self.host, self.port)
            self.vision_sensor = register_sensor("vision", 0, self.host, self.port)
            self.object_sensor = boolean_sensor("object", 3, self.host, self.port)
            self.exit_sensor = boolean_sensor("exit_sensor", 4, self.host, self.port)
            self.blue_sorter = sorter("blue part sorter", 2, 3, self.host, self.port)
            self.green_sorter = sorter("green part sorter", 4, 5, self.host, self.port)
            self.grey_sorter = sorter("grey part sorter", 6, 7, self.host, self.port)

            self.fsm_states = {1 : self.state_1,
                                2 : self.state_2,
                                3 : self.state_3,
                                4 : self.state_4,
                                5 : self.state_5,
                                6 : self.state_6,
                                7 : self.state_7,
                                8 : self.state_8,
                                9 : self.state_9}

            # Reset all objects to avoid problems with Factory I/O running previously
            self.entry_conveyor.stop()
            self.exit_conveyor.stop()
            self.blue_sorter.reset()
            self.green_sorter.reset()
            self.grey_sorter.reset()
            self.vision_value = 0
            return [event_value, None, False]

        elif event_name == 'READ':
            # The following code is a loop executing the Finite State Machine (FSM) that controls the simulation.
            # DINASORE will call this code repeatedly.
            # The only part missing is the pick and place robot control, that is implemented in another function block.
            # States 4 and 5 control the robot interaction.

            # Variable to store the return parameters
            return_value = [None, event_value, False]
            if(self.simulation_running):
                # Execute current state actions
                return_value = self.fsm_states[self.state](event_value, discard_finished)
                print("Current state: ", self.state)
                #print("Current return value: ", return_value)
            else:
                time.sleep(0.2)
            return return_value