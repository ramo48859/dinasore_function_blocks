class COUNTER:    
    def __init__(self):
        self.state = None
        self.count = 0
        self.save = 0
        
    def schedule(self, event_name, event_value, input,reset):

        if event_name == 'INIT':
            self.count=0
            return [event_value, None, self.count]

        elif event_name == 'READ':
            if((input==1) and (self.save==0)):
                self.count=self.count+1
            self.save=input
            if(reset == 1):
                self.count=0
            return [None, event_value, self.count]