import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import derive_timeseries
import matplotlib.cm as cm
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
    y_noise_function=lambda speed: speed + (random.gauss(0, 0.01)),  # ToDo determine real function
    x_noise_function=lambda t: t + (random.gauss(0, 2)),
    p_new_block_per_second=1.86e-4,
    p_data_point_lost=0.02,
    decimals=0,
    on_changes=True)

variation_f = derive_timeseries(
    dataframe=original_series,
    x_dimension="timestamp",
    y_dimension="y",
    mean_every_seconds=5,
    y_noise_function=lambda speed: speed + (random.gauss(0, 0.01)),
    x_noise_function=lambda t: t + (random.gauss(0, 2)),
    p_new_block_per_second=1.86e-4,
    p_data_point_lost=0.02,
    decimals=2,
    on_changes=False)



fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(10,10))

original_series = original_series.set_index("timestamp").sort_index()
variation_h = variation_h.set_index("timestamp").sort_index()
variation_f = variation_f.set_index("timestamp").sort_index()


ax1.set_title("Entire Series")
ax1.plot(original_series.loc[:, [ "y"]], lw=0.5, label="original")
ax1.plot(variation_h.loc[:, [ "y"]], lw=0.5, label="variation_h")
ax1.plot(variation_f.loc[:, [ "y"]], lw=0.5, label="variation_f")
ax1.legend()

ax2.set_title("First minute in detail")
detail_limit = original_series.index.min() + 60
ax2.plot(original_series.loc[:, [ "y"]][original_series.index < detail_limit], lw=0.5, label="original")
ax2.plot(variation_f.loc[:, [ "y"]][variation_f.index < detail_limit], lw=0.5, label="variation_f")
ax2.plot(variation_h.loc[:, [ "y"]][variation_h.index < detail_limit], lw=0.5, label="variation_h")
ax2.legend()

ax3.set_title("Blocks of variation_f")



for n, g in variation_f.groupby('block'):
    c = np.random.rand(3,)
    g.loc[:, [ "y"]].plot(ax=ax3, lw=0.5, color=c)

#ax2.legend()

plt.show()
