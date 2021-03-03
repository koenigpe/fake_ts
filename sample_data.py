import copy
import random
import uuid

import numpy as np
import pandas as pd
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

    def get_data_as_collected(self, fdc_mac):
        hmi = self.derive_timeseries(
            y_dimension="Speed",
            mean_every_seconds=2,
            y_noise_function=lambda s: s + (random.gauss(2, 0.01)),
            x_noise_function=lambda t: t + random.gauss(0, 2),
            p_new_block_per_second=2e-4,
            p_data_point_lost=0.02,
            decimals=0,
            on_changes=True,
            drop_start_end_max = 100)

        fdc =self.derive_timeseries(
            y_dimension="Speed",
            mean_every_seconds=5,
            y_noise_function=lambda s: s + (random.gauss(0, 0.01)),
            x_noise_function=lambda t: t + random.gauss(0, 2),
            p_new_block_per_second=2e-4,
            p_data_point_lost=0.02,
            decimals=2,
            on_changes=False,
            drop_start_end_max = 100).data
        fdc["mac"] = fdc_mac
        fdc = SampleData(fdc)

        f_sessions = fdc.data.reset_index().groupby("session").agg({"timestamp": ['min', 'max']})

        h_sessions = hmi.data.reset_index().groupby("session").agg({"timestamp": ['min', 'max']})

        h_sessions.columns = h_sessions.columns.droplevel(0)
        f_sessions.columns = f_sessions.columns.droplevel(0)

        j = h_sessions.reset_index().merge(f_sessions.reset_index(), how="cross", suffixes=('_h', '_f'))
        j["to"] = j[["max_h", "max_f"]].min(axis=1)
        j["from"] = j[["min_h", "min_f"]].max(axis=1)
        j = j[j["to"] - j["from"] > 0].drop(columns=['min_h', 'min_f', 'max_h', 'max_f']).reset_index()

        return (hmi, fdc, j)


    def derive_timeseries(self,
                          y_dimension,
                          mean_every_seconds
                          , y_noise_function
                          , x_noise_function
                          , p_new_block_per_second
                          , p_data_point_lost
                          , decimals
                          , on_changes
                          , drop_start_end_max):
        # Group Data
        self.data.index = np.floor(self.data.index / mean_every_seconds) * mean_every_seconds

        derived_series = self.data.groupby(self.data.index).mean()

        # Apply y_noise_function
        derived_series[y_dimension] = derived_series[y_dimension].apply(y_noise_function)

        # Add sessions
        # ToDo check math
        block_boolean_matrix = (np.random.random((derived_series.shape[0])) > pow(1 - p_new_block_per_second,
                                                                                  mean_every_seconds)).astype(int)
        u = random.randint(100000, 900000000)

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
        derived_series = derived_series.reset_index()

        derived_series["timestamp"] = derived_series["timestamp"].apply(x_noise_function)
        derived_series["timestamp"] = derived_series["timestamp"].astype(float)

        # Drop first / last data from session
        d = int(random.random() * drop_start_end_max)

        sessions = derived_series['session'].unique()

        derived_series = \
            pd.concat([derived_series[derived_series['session'] == b].iloc[d:] for b in sessions])

        derived_series = derived_series.set_index("timestamp")

        return SampleData(derived_series.drop("index", errors='ignore'))

    def plot_blocks(self, ax):
        for n, g in self.data.groupby('session'):
            c = np.random.rand(3, )
            g.loc[:, ["Speed"]].plot(ax=ax, lw=0.5, color=c)

    def plot_series(self, ax):
        c = np.random.rand(3, )
        ax.plot(self.data.loc[:, ["Speed"]], lw=0.5, color=c)
