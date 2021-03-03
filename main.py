import random

from sample_data import SampleData
from utils import get_sample_data, get_logfile_sample
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.0f' % x)

# Input Data
h_data, f_data, matches = get_sample_data(vehicles=10, period_of_time_h=3, plot=True)


# Summary h data
print(
    h_data.reset_index().groupby("session").agg({"timestamp":['min','max'], 'Speed':'mean'})
)

# Summary f data
print(
    f_data.reset_index().groupby(["mac", "session"]).agg({"timestamp":['min','max'], 'Speed':'mean'})
)







