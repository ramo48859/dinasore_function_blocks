"""
This block will plot two JSON timeseries.

Input format from MEASUREMENTS_TO_JSON_TIMESERIES fblock:

"{"columns": ["sensor","measurement"],"index": ["2017-01-01T12:00:00.000000Z","2017-01-01T12:00:00.300000Z","2017-01-01T12:00:00.600000Z","2017-01-01T12:00:00.900000Z","2017-01-01T12:00:01.200000Z","2017-01-01T12:00:01.500000Z","2017-01-01T12:00:01.800000Z","2017-01-01T12:00:02.100000Z","2017-01-01T12:00:02.400000Z","2017-01-01T12:00:02.700000Z"],"data":[[3,0.0],[3,0.0],[3,0.0],[3,0.0],[3,0.0],[3,0.0],[3,0.0],[3,0.0],[3,0.0],[3,0.0]]}"
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PLOT_JSON_TIMESERIES:

    def __init__(self):
        self.state = None
        
    def schedule(self, event_name, event_value,
                 first_json_timeseries, second_json_timeseries):

        if event_name == 'INIT':    
            return [event_value, None]

        elif event_name == 'RUN':
            #Convert the json timeseries into a pandas dataframe object
            reference_dfa = pd.read_json(first_json_timeseries, orient="split", precise_float=True)
            process_dfa = pd.read_json(first_json_timeseries, orient="split", precise_float=True)

            frames = [reference_dfa, process_dfa, df3]
            result = pd.concat(frames, keys=["reference", "process"])
            
            measurements.plot(subplots=True, legend=False)
            pyplot.show()

            return [None, event_value]