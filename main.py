import random

from utils import get_sample_data

# Input Data
h_data, f_data = get_sample_data(plot = False)

# Summary h data
print(
h_data.reset_index().groupby("session").agg({"timestamp":['min','max'], 'Speed':'mean'})
)

# Summary f data
print(
f_data.reset_index().groupby(["mac", "session"]).agg({"timestamp":['min','max'], 'Speed':'mean'})
)







