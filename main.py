import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import derive_timeseries, prepair_for_plot

# Read some data
original_series = pd.read_csv("data/2018-11-20_06.01.44.log", sep=';').loc[:, ["timestamp", "Speed"]]
# convert timestamp to seconds
original_series["timestamp"] = (original_series["timestamp"] / 1000).apply(np.round)
# Convert gps m/s to km/h
original_series["y"] = original_series['Speed'] * 3.6

variation_h = derive_timeseries(
    dataframe=original_series,
    x_dimension="timestamp",
    y_dimension="y",
    mean_every_seconds=2,
    y_noice_function=lambda speed: speed + (random.gauss(0, 0.01)),  # ToDo determine real function
    x_noice_function=lambda t: t + (random.gauss(0, 2)),
    p_new_block_per_second=1.86e-4,
    p_data_point_lost=0.02,
    decimals=0,
    on_changes=True)

variation_f = derive_timeseries(
    dataframe=original_series,
    x_dimension="timestamp",
    y_dimension="y",
    mean_every_seconds=5,
    y_noice_function=lambda speed: speed + (random.gauss(0, 0.01)),
    x_noice_function=lambda t: t + (random.gauss(0, 2)),
    p_new_block_per_second=1.86e-4,
    p_data_point_lost=0.02,
    decimals=2,
    on_changes=False)

# ToDo Add Labels

fig, (ax1) = plt.subplots(nrows=1, ncols=1)

original_series = prepair_for_plot(original_series)
variation_h = prepair_for_plot(variation_h)
variation_f = prepair_for_plot(variation_f)

ax1.plot(original_series, lw=0.5, label="original")
ax1.plot(variation_h, lw=0.5, label="variation_h")
ax1.plot(variation_f, lw=0.5, label="variation_f")
ax1.legend()

plt.show()
