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
                path, name,
                y_axis_label, title,
                first_json_timeseries, second_json_timeseries):

        if event_name == 'INIT':    
            return [event_value, None]

        elif event_name == 'RUN':

            #Convert the json timeseries into a pandas dataframe object
            reference_dfa = pd.read_json(first_json_timeseries, orient="split", precise_float=True)
            process_dfa = pd.read_json(second_json_timeseries, orient="split", precise_float=True)
            process_dfa.index = reference_dfa.index

            plt.plot(reference_dfa['value'], label='Reference Curve', color='green')
            plt.plot(process_dfa['value'], label='Process Curve', color='steelblue')

            plt.legend(title='Group')

            #add axes labels and a title
            plt.ylabel(y_axis_label, fontsize=14)
            plt.xlabel('timestamp', fontsize=14)
            plt.title(title, fontsize=16)
            plt.savefig('{0}\\{1}.png'.format(path,name), dpi="figure")
            plt.show()

            return [None, event_value]