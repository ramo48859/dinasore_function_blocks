import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from multiprocessing import Process, Value, Manager
from ctypes import c_char_p
from tkinter import *

# This FB plots the values of 4 time series in streaming
# Install tkinter pip install tk
# https://stackoverflow.com/questions/34764535/why-cant-matplotlib-plot-in-a-different-thread

#Create a window
window=Tk("Streamming Plot FB")

class StreamingPlotter:

    def __init__(self, sampling_window, serie1_units, serie2_units, serie3_units, serie4_units):

        self.sampling_window = sampling_window
        self.serie1_units = serie1_units
        self.serie2_units = serie2_units 
        self.serie3_units = serie3_units 
        self.serie4_units = serie4_units

        empty_series = [0]*sampling_window
        self.series = [empty_series, empty_series, empty_series, empty_series]
        plt.style.use('ggplot')
        self.fig = matplotlib.figure.Figure()
        self.axs1 = self.fig.add_subplot(2,2,1)
        self.axs2 = self.fig.add_subplot(2,2,2)
        self.axs3 = self.fig.add_subplot(2,2,3)
        self.axs4 = self.fig.add_subplot(2,2,4)

    def animate_temp(self, sample1, sample2, sample3, sample4):

        # Append most recent value
        self.series[0].append(sample1.value)   
        # Keep only the last 'sampling_window' items
        self.series[0] = self.series[0][-self.sampling_window:]
        # Draw x and y for serie 1
        self.axs1.clear()
        self.axs1.plot(self.series[0])
        self.axs1.set_xlabel("Serie 1")
        self.axs1.set_ylabel(self.serie1_units)

        self.series[1].append(sample2.value)
        self.series[1] = self.series[1][-self.sampling_window:]
        self.axs2.clear()
        self.axs2.plot(self.series[1])
        self.axs2.set_xlabel("Serie 2")
        self.axs2.set_ylabel(self.serie2_units)

        self.series[2].append(sample3.value)
        self.series[2] = self.series[2][-self.sampling_window:]
        self.axs3.clear()
        line = self.axs3.plot(self.series[2])
        self.axs3.set_xlabel("Serie 3")
        self.axs3.set_ylabel(self.serie3_units)
        #self.axs3.draw_artist(line)

        self.series[3].append(sample4.value)
        self.series[3] = self.series[3][-self.sampling_window:]
        self.axs4.clear()
        self.axs4.plot(self.series[3])
        self.axs4.set_xlabel("Serie 4")
        self.axs4.set_ylabel(self.serie4_units)

        self.canvas.draw()
        # Call itseld
        window.after(500,self.animate_temp, sample1, sample2, sample3, sample4)        

    def start(self, sample1, sample2, sample3, sample4):
        # Store the shared variables
        self.sample1 = sample1
        self.sample2 = sample2
        self.sample3 = sample3
        self.sample4 = sample4
        self.canvas = FigureCanvasTkAgg(self.fig, master=window)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.draw()
        self.animate_temp(self.sample1, self.sample2, self.sample3, self.sample4)
        window.mainloop()

def start_plot_process(sampling_window, 
    units1, units2, units3, units4, 
    sample1, sample2, sample3, sample4):
    # Plot object
    splotter = StreamingPlotter(sampling_window.value, units1.value, units2.value, units3.value, units4.value)
    splotter.start(sample1, sample2, sample3, sample4)

class SREAMING_PLOT_4_TIMESERIES:

    def schedule(self, event_name, event_value, samp_window,
                serie1_units, serie2_units, serie3_units, serie4_units,
                reading1, reading2, reading3, reading4):

        if event_name == 'INIT':
            # Variables to share with the plot process
            self.sampling_window = Value('i', 10)
            manager = Manager()
            self.units1 = manager.Value(c_char_p, serie1_units)
            self.units2 = manager.Value(c_char_p, serie2_units)
            self.units3 = manager.Value(c_char_p, serie3_units)
            self.units4 = manager.Value(c_char_p, serie4_units)
            self.sample1 = Value('d', 0.0)
            self.sample2 = Value('d', 0.0)
            self.sample3 = Value('d', 0.0)
            self.sample4 = Value('d', 0.0)

            self.sampling_window.value = samp_window

            plot_process = Process(target=start_plot_process, 
                args=(self.sampling_window, 
                self.units1, self.units2, self.units3, self.units4,
                self.sample1, self.sample2, self.sample3, self.sample4,))
            plot_process.start()
            return [event_value, None]

        elif event_name == 'RUN':
            self.sample1.value = reading1
            self.sample2.value = reading2
            self.sample3.value = reading3
            self.sample4.value = reading4
            return [None, event_value]