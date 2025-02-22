class FB_RS:

	def __init__(self):
		self.value = False
		
	def schedule(self, event_input_name, event_input_value, S, R1 ):

		CNF=True

		if(event_input_name == 'REQ'):
			if(S==True):
				self.value = True
			if(R1==True):
				self.value = False

		return [CNF, self.value]