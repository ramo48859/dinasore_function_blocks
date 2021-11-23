import json

import pandas as pd



""" 

This block takes a two timeseries from MEASUREMENTS_TO_JSON_TIMESERIES block and calculates

its correlation.

"""	



class TIMESERIES_CORRELATION_ANALYSIS:

     

    def schedule(self, event_name, event_value,

                 TIMESERIES_1, TIMESERIES_2):



        if event_name == 'INIT':

            return [event_value, None, None]



        elif event_name == 'RUN':

            # if TIMESERIES_1 == None:

                  # print("Correlation timeseries_1 is None.")

                  # return [None, event_value, None]

                    

            # if TIMESERIES_2 == None:

                  # print("Correlation timeseries_2 is None.")

                  # return [None, event_value, None]

                    

            dataframe1 = pd.read_json(TIMESERIES_1,orient="split")

            dataframe2 = pd.read_json(TIMESERIES_2,orient="split")

            

            print(dataframe1)



            result = dataframe1['measurement'].corr(dataframe2['measurement'])

            print(result)

            return [None, event_value, result]

