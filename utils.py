import numpy as np
import pandas as pd



def derive_timeseries(dataframe,
                      x_dimension,
                      y_dimension,
                      mean_every_seconds
                      , y_noise_function
                      , x_noise_function
                      , p_new_block_per_second
                      , p_data_point_lost
                      , decimals
                      , on_changes):
    # Group Data
    grp = (dataframe[x_dimension] / mean_every_seconds).apply(np.floor) * mean_every_seconds
    derived_series = dataframe.groupby(grp).mean()

    # Apply y_noise_function
    derived_series[y_dimension] = derived_series[y_dimension].apply(y_noise_function)

    # Add sessions
    # ToDo check math
    block_boolean_matrix = (np.random.random((derived_series.shape[0])) > pow(1 - p_new_block_per_second,
                                                                              mean_every_seconds)).astype(int)
    session = np.cumsum(block_boolean_matrix)
    derived_series["block"] = session

    # round data
    derived_series[y_dimension] = derived_series[y_dimension].round(decimals)

    # Add OnChange
    derived_series["y_prev"] = derived_series[y_dimension].shift(1)
    if (on_changes):
        derived_series = derived_series[derived_series[y_dimension] != derived_series["y_prev"]]

    # Dropout datapoints
    derived_series = derived_series[np.random.random((derived_series.shape[0])) > p_data_point_lost]

    # Apply x_noise_function
    # ToDo if it actually does something
    derived_series[x_dimension] = derived_series[x_dimension].apply(x_noise_function)
    return derived_series
