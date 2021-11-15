import time
from opcua import Client
from opcua import ua

#===================================================================================
# OPCUA_VARIABLE_WRITER Function block
# 
# This function block connects to an OPCUA endpoint url, and, whenever is triggered,
# writes the specified variable value.
# 
# @type  endpoint_url: string
# @param endpoint_url: The URL of the OPC UA server to connect.
# 
# @type  node_id: string
# @param node_id: A node id string (e.g. "ns=2;s=Vibration Z)
#
# @type  value: string
# @param value: The value to be written, serialized as string
# 
# @organization: DIGI2 Lab, FEUP
# @author: Lu�s Neto
# @contact: lcneto@fe.up.pt
# @license: GPLv3
# @date: 12-11-2021
# @version: V1.0.1
#===================================================================================

class OPCUA_VARIABLE_WRITER:
    
    def __init__(self):
        self.endpoint_url = ""
        self.status = ""
        self.client = None
        self.data = ""
        self.node = None
    
    def schedule(self, event_input_name, event_input_value, 
        endpoint_url, node_id, value):

        if event_input_name == 'INIT':
            if not endpoint_url:
                self.status = "Error, endpoint URL not specified"
                return [event_input_value, None, self.status, None]
            if not node_id:
                self.status = "Error, node_id not specified"
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
                try:
                    self.node = self.client.get_node(node_id)
                    self.status = "Ready to write data."
                except Exception as e: 
                    print(e)
                    self.status = "Error retrieving node '{}' from server.".format(node_id)
                    return [event_input_value, None, self.status, None]
            return [event_input_value, None, self.status, None]

        elif event_input_name == 'RUN':

            self.status = "Writing data '{}'".format(value)

            #Currently the blockis only writing booleans
            #TODO: Verify the self.node data type and cast value accordingly
            
            data_value = ua.DataValue(ua.Variant(bool(value), ua.VariantType.Boolean))
            self.node.set_value(data_value)

            return [None, event_input_value, self.status, value]
