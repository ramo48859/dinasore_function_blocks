class F_NOT:

	def __init__(self):
		pass
		
	def schedule(self, event_input_name, event_input_value, IN):

		OUT = None
		EO_EVENT=True
		
		if(event_input_name == 'EI'):
			OUT = not IN

		return [EO_EVENT, OUT]