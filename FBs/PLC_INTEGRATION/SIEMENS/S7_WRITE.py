from ipaddress import ip_address
import snap7
class S7_WRITE:    
    def __init__(self):
        self.state = None
        self.client = snap7.client.Client()
        
    def schedule(self, event_name, event_value, ip_address, rack, number, port, db_number,start, size,data):

        if event_name == 'INIT':
            self.client.connect(ip_address,rack,number,port)
            status = self.client.get_connected()
            if(status == True):
                print('Connection sucessfully initiated with device at {0}'.format(ip_address))
            else:
                print('Error initiating connection with S7 PLC')
            return [event_value, None, None]

        elif event_name == 'RUN':
            #db_read(db_number: int, start: int, size: int)
            
            b_array =bytearray(data.to_bytes(size, byteorder='big'))
            print(b_array)
            self.client.db_write(db_number,start,b_array)
            return [None, event_value]