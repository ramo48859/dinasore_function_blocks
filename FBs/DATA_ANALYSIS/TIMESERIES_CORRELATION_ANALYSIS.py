import json
import pandas as pd
import numpy as np

""" 
This block takes a two JSON_TIMESERIES and calculates
its correlation.

This block can be modified to use custom columns names.
"""	

class TIMESERIES_CORRELATION_ANALYSIS:

    def schedule(self, event_name, event_value,
                 TIMESERIES_1, TIMESERIES_2):

        if event_name == 'INIT':
            return [event_value, None, None]

        elif event_name == 'RUN':
            if TIMESERIES_1 == None:
                  print("Correlation timeseries_1 is None.")
                  return [None, event_value, None]

            if TIMESERIES_2 == None:
                  print("Correlation timeseries_2 is None.")
                  return [None, event_value, None]

            dataframe1 = pd.read_json(TIMESERIES_1,orient="split")
            dataframe2 = pd.read_json(TIMESERIES_2,orient="split")
            #Make timestamps equal, otherwise correlation does not match rows
            dataframe2.index = dataframe1.index
            #If the result is a long string DINASORE will block
            #TODO verify this problem
            result = dataframe1['value'].corr(dataframe2['value'])
            #print("Correlation result: {}".format(result))
            return [None, event_value, result]