
from ipaddress import ip_address
import snap7
class S7_READ_CONTINUOUS_BYTE:    
    def __init__(self):
        self.state = None
        self.client = snap7.client.Client()
        self.bits = [0,0,0,0,0,0,0,0]
        self.old_value = 0
        self.first_time = True
        
        self.bit_changed = [True, True, True, True, True, True, True, True ]

    def schedule(self, event_name, event_value, ip_address, rack, number, port, db_number,start, bit):
        
        if event_name == 'INIT':
            try:
                self.client.connect(ip_address,rack,number,port)
                status = self.client.get_connected()
            except:
                status = False
            if(status == True):
                print('Connection sucessfully initiated with device at {0}'.format(ip_address))
            else:
                print('Error initiating connection with S7 PLC')
            return [event_value, None, None, None, None, None, None, None, None ,None, 0,self.bits[0], self.bits[1], self.bits[2], self.bits[3], self.bits[4], self.bits[5], self.bits[6], self.bits[7]]

        elif event_name == 'READ':
            try:            
                data = self.client.db_read(db_number,start,1)
            except:
                data = self.old_value
            int_val = int.from_bytes(data, "big")
            #calculate edge transitions
            changes = int_val ^ self.old_value
            
            #Calculate bit changes
            i=0
            if(not self.first_time):
                for i in range(0,8):
                    if(changes & (1<<i)):
                        self.bit_changed[i] = True
                    else:
                        self.bit_changed[i] = False
                    self.bits[i] = (int_val & (1<<i))>> i
            else: 
                for i in range(0,8,1):
                    self.bits[i] = (int_val & (1<<i))>> i
                self.first_time = False
            #prepare outputs
            return_value = [None, event_value]
            for i in range(0,8):
                return_value.append(1 if self.bit_changed[i]==True else None)
            return_value.append(int_val)
            for i in range(0,8):
                return_value.append(self.bits[i])
            
            self.old_value = int_val

            return return_value
    

    def __del__(self):
        self.client.__del__()