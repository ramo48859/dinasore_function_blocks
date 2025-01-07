from enum import Enum


class States(Enum):
    START = 0
    E1 = 1
    E2 = 2


class E_REND_2:
    def __init__(self):
        self.state = States.START

    def schedule(self, event_input_name, event_input_value):
        match self.state:
            case States.START:
                if event_input_name == "EI1":
                    self.state = States.E1
                    return [None]
                elif event_input_name == "EI2":
                    self.state = States.E2
                    return [None]

            case States.E1:
                if event_input_name == "R":
                    self.state = States.START
                    return [None]
                elif event_input_name == "EI2":
                    self.state = States.START
                    return [event_input_value]

            case States.E2:
                if event_input_name == "R":
                    self.state = States.START
                    return [None]
                elif event_input_name == "EI1":
                    self.state = States.START
                    return [event_input_value]
        return [None]
