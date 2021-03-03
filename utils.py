import random
import uuid

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sample_data import SampleData

# Read the logfile sample
def get_logfile_sample():
    original_series = pd.read_csv("data/2018-11-20_06.01.44.log", sep=';').loc[:, ["timestamp", "Speed"]]
    # bring timestamp to seconds
    #original_series["timestamp"] = (original_series["timestamp"] / 1000).apply(np.round)
    # Convert gps m/s to km/h
    original_series["Speed"] = original_series['Speed'] * 3.6
    return original_series.set_index(["timestamp"])


# Create three drivecycle based on sample data

#todo add time window

def derive_new_series(original, time_window_h):
    time_window_msec = time_window_h * 60 * 60 * 1000
    speed_offset = random.random()*1.5
    time_shift = random.randint(0, time_window_msec)

    return original.derive_timeseries(
        y_dimension="Speed",
        mean_every_seconds=1,
        y_noise_function=lambda speed: speed * speed_offset + (random.gauss(0, 0.01)),
        x_noise_function=lambda t: t + time_shift,
        p_new_block_per_second=0,
        p_data_point_lost=0,
        decimals=2,
        on_changes=False,
        drop_start_end_max = 10)

def get_sample_data(vehicles=6, period_of_time_h=2, plot = False):


    s = SampleData(get_logfile_sample())

    drivecycle = [derive_new_series(s, period_of_time_h) for x in range(vehicles) ]


    tuple = [x.get_data_as_collected( str(uuid.uuid4())) for x in drivecycle ]

    h_data = pd.concat([tuple[x][0].data for x in range(len(tuple))])
    f_data = pd.concat([tuple[x][1].data for x in range(len(tuple))])
    matches = pd.concat([tuple[x][2] for x in range(len(tuple))])






    if (plot):

        fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))

        ax1.set_title("Crivecycle")
        [dc.plot_series(ax1) for dc in drivecycle]

        plt.show()

    return h_data, f_data, matches


