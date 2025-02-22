class THRESHOLD:    
    def __init__(self):
        self.state = None

    def schedule(self, event_name, event_value, input, limit):

        if event_name == 'INIT':
            self.count=0
            return [event_value, None, 0]

        elif event_name == 'READ':
            if(input >= limit):
                return [None, event_value, 1]
            else:
                return [None, event_value, 0]