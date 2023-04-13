class E_R_TRIG:
    
    def __init__(self):
        self.value = None
        pass
    
    def schedule(self, event_input_name, event_input_value, QI):
		
        EO_EVENT = None
		
        if(event_input_name == 'EI' and self.value!= None):
            if(self.value == 0) and (QI == True ):
                EO_EVENT = 1

        self.value = QI
        return [EO_EVENT]