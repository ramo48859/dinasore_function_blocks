import json
import pandas as pd
import numpy as np

class FILTER_JSON_TIMESERIES:

    def schedule(self, event_name, event_value, TIMESERIES_1_IN, TIMESERIES_2_IN):
        if event_name == 'INIT':            
            return [event_value, None, None, None]

        elif event_name == 'RUN':
            
            #print("Meas2Times Run")
            #meas_str_list = np.array(MEASUREMENTS.split(";"))
            #meas_flt_list = meas_str_list.astype(float)
            #measurements  = [(self.sensor_id,meas_flt_list[x]) for x in range(len(meas_flt_list))]
            #times_str_list = np.array(TIMESTAMPS.split(";"))
            #times_tst_list = times_str_list.astype(pd.Timestamp)            
            #timeseries = pd.DataFrame(measurements, columns=["sensor","measurement"], index=times_tst_list)
            #result = timeseries.to_json(orient="split", date_format="iso", date_unit="us")
            #print("here")
            #ts1 = json.loads(TIMESERIES_1_IN)
            #ts2 = json.loads(TIMESERIES_2_IN)
            #print(ts1)
            
            dataframe1 = pd.read_json(TIMESERIES_1_IN,orient="split")
            dataframe2 = pd.read_json(TIMESERIES_2_IN,orient="split")

            dataframe1_filtered = dataframe1[dataframe1.value != 0]
            dataframe2_filtered = dataframe2[dataframe2.value != 0]

            size1 = len(dataframe1_filtered.index)
            size2 = len(dataframe2_filtered.index)

            size = None
            if(size1<size2):
                size = size1
            else:
                size = size2

            timeseries_1_out = dataframe1_filtered.tail(size)
            timeseries_2_out = dataframe2_filtered.tail(size)

            timeseries_1_out = timeseries_1_out.to_json(orient="split", date_format="iso", date_unit="us")
            timeseries_2_out = timeseries_2_out.to_json(orient="split", date_format="iso", date_unit="us")

            return [None, event_value, timeseries_1_out, timeseries_2_out]