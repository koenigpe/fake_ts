import copy
import random
import uuid

import numpy as np

np.random.seed(1234)
random.seed(1234)

class SampleData:

    def __init__(self, base_data):
        # ToDo assert if base_bata has required fields (timestamp, speed)
        # ToDo assert if base_bata has required unit (timestamp sec, speed km/h

        self.data = base_data
        self.start = base_data.index.min()
        self.end = base_data.index.max()
        self.duration = self.end - self.start
        # Read some data

        # convert timestamp to seconds

    def get_as_h(self):
        return self.derive_timeseries(
            y_dimension="Speed",
            mean_every_seconds=2,
            y_noise_function=lambda s: s + (random.gauss(2, 0.01)),
            x_noise_function=lambda t: t + random.gauss(0, 2),
            p_new_block_per_second=2e-4,
            p_data_point_lost=0.02,
            decimals=0,
            on_changes=True)

    def get_as_f(self, mac):
        new_series =self.derive_timeseries(
            y_dimension="Speed",
            mean_every_seconds=5,
            y_noise_function=lambda s: s + (random.gauss(0, 0.01)),
            x_noise_function=lambda t: t + random.gauss(0, 2),
            p_new_block_per_second=2e-4,
            p_data_point_lost=0.02,
            decimals=2,
            on_changes=False).data
        new_series["mac"] = mac
        return SampleData(new_series)


    def derive_timeseries(self,
                          y_dimension,
                          mean_every_seconds
                          , y_noise_function
                          , x_noise_function
                          , p_new_block_per_second
                          , p_data_point_lost
                          , decimals
                          , on_changes):
        # Group Data
        self.data.index = np.floor(self.data.index / mean_every_seconds) * mean_every_seconds

        derived_series = self.data.groupby(self.data.index).mean()

        # Apply y_noise_function
        derived_series[y_dimension] = derived_series[y_dimension].apply(y_noise_function)

        # Add sessions
        # ToDo check math
        block_boolean_matrix = (np.random.random((derived_series.shape[0])) > pow(1 - p_new_block_per_second,
                                                                                  mean_every_seconds)).astype(int)
        u = random.randint(1000000, 9000000)

        session = np.cumsum(block_boolean_matrix)+u

        derived_series["session"] = session

        # round data
        derived_series[y_dimension] = derived_series[y_dimension].round(decimals)

        # Add OnChange
        derived_series["y_prev"] = derived_series[y_dimension].shift(1)
        if (on_changes):
            derived_series = derived_series[derived_series[y_dimension] != derived_series["y_prev"]]
        del derived_series["y_prev"]
        # Dropout datapoints
        derived_series = derived_series[np.random.random((derived_series.shape[0])) > p_data_point_lost]

        # Apply x_noise_function
        # ToDo if it actually does something
        derived_series.index = x_noise_function(derived_series.index)

        return SampleData(derived_series)

    def plot_blocks(self, ax):
        for n, g in self.data.groupby('session'):
            c = np.random.rand(3, )
            g.loc[:, ["Speed"]].plot(ax=ax, lw=0.5, color=c)

    def plot_series(self, ax, c):
        ax.plot(self.data.loc[:, ["Speed"]], lw=0.5, color=c)
