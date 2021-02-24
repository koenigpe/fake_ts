import random

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sample_data import SampleData

# Read the logfile sample
def get_logfile_sample():
    original_series = pd.read_csv("data/2018-11-20_06.01.44.log", sep=';').loc[:, ["timestamp", "Speed"]]
    # bring timestamp to seconds
    original_series["timestamp"] = (original_series["timestamp"] / 1000).apply(np.round)
    # Convert gps m/s to km/h
    original_series["Speed"] = original_series['Speed'] * 3.6
    return original_series.set_index(["timestamp"])

# Create three drivecycle based on sample data
def get_sample_data(plot = False):
    s = SampleData(get_logfile_sample())
    drivecycle1 = s.derive_timeseries(
        y_dimension="Speed",
        mean_every_seconds=2,
        y_noise_function=lambda speed: speed / 2 + (random.gauss(0, 0.01)),
        x_noise_function=lambda t: t,
        p_new_block_per_second=0,
        p_data_point_lost=0,
        decimals=2,
        on_changes=False)

    drivecycle1_h = drivecycle1.get_as_h()
    drivecycle1_f = drivecycle1.get_as_f("drivecycle1mac")

    drivecycle2 = s.derive_timeseries(
        y_dimension="Speed",
        mean_every_seconds=2,
        y_noise_function=lambda speed: speed + (random.gauss(0, 0.01)),
        x_noise_function=lambda t: t+(60*55),
        p_new_block_per_second=0,
        p_data_point_lost=0,
        decimals=2,
        on_changes=False)

    drivecycle2_h = drivecycle2.get_as_h()
    drivecycle2_f = drivecycle2.get_as_f("drivecycle2mac")

    drivecycle3 = s.derive_timeseries(
        y_dimension="Speed",
        mean_every_seconds=2,
        y_noise_function=lambda speed: speed / 1.5 + (random.gauss(0, 0.01)),
        x_noise_function=lambda t: t+(60*60 * 1.2),
        p_new_block_per_second=0,
        p_data_point_lost=0,
        decimals=2,
        on_changes=False)

    drivecycle3_h = drivecycle3.get_as_h()
    drivecycle3_f = drivecycle3.get_as_f("drivecycle3mac")

    if (plot):

        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(10, 10))

        ax1.set_title("Crivecycle")
        drivecycle1.plot_series(ax1, "red")
        drivecycle2.plot_series(ax1, "blue")
        drivecycle3.plot_series(ax1, "green")

        ax2.set_title("H Sessions")
        drivecycle1_h.plot_blocks(ax2)
        drivecycle2_h.plot_blocks(ax2)
        drivecycle3_h.plot_blocks(ax2)

        ax3.set_title("F Sessions")
        drivecycle1_f.plot_blocks(ax3)
        drivecycle2_f.plot_blocks(ax3)
        drivecycle3_f.plot_blocks(ax3)

        plt.show()

    return (
        pd.concat([drivecycle3_h.data, drivecycle2_h.data, drivecycle1_h.data]),
        pd.concat([drivecycle3_f.data, drivecycle2_f.data, drivecycle1_f.data])
    )




