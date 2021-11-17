import time
from opcua import Client
from opcua import ua

#===================================================================================
# OPCUA_VARIABLE_LISTEN_STATE_CHANGER Function block
# 
# This function block connects to an OPCUA endpoint url, and, whenever the given variable
# changes, it fires a boolean output.
# 
# @type  endpoint_url: string
# @param endpoint_url: The URL of the OPC UA server to connect.
# 
# @type  node_id: string
# @param node_id: A node id string (e.g. "ns=2;s=Vibration Z)
#
# @type  value: boolean
# @return value: The trigger value
# 
# @organization: DIGI2 Lab, FEUP
# @author: Lu�s Neto
# @contact: lcneto@fe.up.pt
# @license: GPLv3
# @date: 12-11-2021
# @version: V1.0.1
#===================================================================================

class OPCUA_VARIABLE_LISTEN_STATE_CHANGE:
    
    def __init__(self):
        self.endpoint_url = ""
        self.status = ""
        self.client = None
        self.last_value = None
    
    def schedule(self, event_input_name, event_input_value, 
        endpoint_url, node_id):

        if event_input_name == 'INIT':
            if not endpoint_url:
                self.status = "Error, endpoint URL not specified"
                return [event_input_value, None, self.status, None]

            else:
                self.endpoint_url = endpoint_url
                self.client = Client(self.endpoint_url)
                
                try:
                    self.client.connect()
                except Exception as e: 
                    print(e)
                    self.status = "Error connecting OPC UA endpoint"
                    return [event_input_value, None, self.status, None]

            return [event_input_value, None, self.status, None]

        elif event_input_name == 'READ':
            variable = None
            if not node_id:
                self.status = "Error, node_id not specified"
                return [None, event_input_value, self.status, None]
            try:
                variable = self.client.get_node(node_id)
                curr_value = variable.get_value()
                self.status = "Variable retrieved successfully."

                if self.last_value != None:
                    if self.last_value != curr_value:
                        return [None, event_input_value, self.status, True]
                    else:
                        return [None, event_input_value, self.status, False]
                else:

                    self.last_value = curr_value
                    return [None, event_input_value, self.status, False]
            except Exception as e: 
                print(e)
                self.status = "Error retrieving node '{}' from server.".format(node_id)
                return [None, event_input_value, self.status, None]

            self.status = "Writing data '{}'".format(value)

            return [None, event_input_value, self.status, value]
