class E_F_TRIG:
    
    def __init__(self):
        print('Initiated E_F_TRIG')
        self.value = None
        pass
    
    def schedule(self, event_input_name, event_input_value, QI):
		
        EO_EVENT = None
		
        if(event_input_name == 'EI' and self.value!= None):
            if(self.value == 1) and (QI == False ):
                EO_EVENT = 1
        #print('Was ' + self.value + 'is ' + QI)

        self.value = QI
        return [EO_EVENT]