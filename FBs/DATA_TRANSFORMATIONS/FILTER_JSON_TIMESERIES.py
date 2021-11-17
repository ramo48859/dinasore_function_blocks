import json
import pandas as pd
import numpy as np

class FILTER_JSON_TIMESERIES:

    def __init__(self):
        self.a = None
        
    def schedule(self, event_name, event_value, TIMESERIES_1_IN, TIMESERIES_2_IN):
    
        if event_name == 'INIT':            
            return [event_value, None, None]


        elif event_name == 'RUN':
            
            #print("Meas2Times Run")
            
            #meas_str_list = np.array(MEASUREMENTS.split(";"))
            #meas_flt_list = meas_str_list.astype(float)
            #measurements  = [(self.sensor_id,meas_flt_list[x]) for x in range(len(meas_flt_list))]
            
            #times_str_list = np.array(TIMESTAMPS.split(";"))
            #times_tst_list = times_str_list.astype(pd.Timestamp)            
            
            #timeseries = pd.DataFrame(measurements, columns=["sensor","measurement"], index=times_tst_list)
            #result = timeseries.to_json(orient="split", date_format="iso", date_unit="us")
            
            ts1 = json.loads(TIMESERIES_1_IN)
            ts2 = json.loads(TIMESERIES_2_IN)

            dataframe1 = pd.DataFrame.from_dict(ts1,orient="index")
            dataframe2 = pd.DataFrame.from_dict(ts2,orient="index")

            dataframe1_filtered = dataframe1[dataframe1.measurement != 0]
            dataframe2_filtered = dataframe2[dataframe2.measurement != 0]

            size1 = len(dataframe1_filtered.index)
            size2 = len(dataframe2_filtered.size.index)

            if(size1<size2):
                size = size1
            else:
                size = size2

            timeseries_1_out = dataframe1_filtered.iloc[:size,]
            timeseries_2_out = dataframe2_filtered.iloc[:size,]

    
            return [None, event_value, timeseries_1_out, timeseries_2_out]
