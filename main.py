import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import datetime as dt
import math
import matplotlib.dates as mdates

# Dataframe
filename = "Data.csv"

# Reading in data, sorting
df = pd.read_csv(filename, parse_dates=True, dayfirst=True)
df["Time(dd/mm/yyyy)"] = pd.to_datetime(df["Time(dd/mm/yyyy)"], format="mixed").dt.floor("T")
df = df.sort_values(by="Time(dd/mm/yyyy)", ascending=True)

# Columns we care about
times = df["Time(dd/mm/yyyy)"]
carbon_content = df["Carbon dioxide(ppm)"]

# Making interpolations
"code referenced from here: https://stackoverflow.com/questions/17315737/split-a-large-pandas-dataframe"
sample_size = 100
num_chunks = math.ceil(len(times)/sample_size)

time_subsets = []
carbon_content_subsets = []
interpolations = []

for i in range(num_chunks):
    time_subset = times[i*sample_size:(i+1)*sample_size]
    carbon_content_subset = carbon_content[i*sample_size:(i+1)*sample_size]
    interpolations.append(CubicSpline(time_subset, carbon_content_subset))

    time_subsets.append(time_subset)
    carbon_content_subsets.append(carbon_content_subset)


# Plot the Cubic Spline Interpolation of the first subset
    
test_index = 0
time_subset = time_subsets[test_index]
# Clean this subset so that it can be displayed nicely

carbon_content_subset = carbon_content_subsets[test_index]
interpolation = interpolations[test_index]

time_min = time_subset.min()
time_max = time_subset.max()

cubic_x = pd.date_range(time_min, time_max, 1000)
cubic_y = interpolation(cubic_x)

plt.figure()
plt.plot(cubic_x.to_pydatetime(), cubic_y, color="green", label="Interpolation")
plt.scatter(time_subset, carbon_content_subset, color="Blue", label="Gathered data")
plt.xlabel(f"Time: from {time_min} to {time_max}")
plt.ylabel("Carbon content")
plt.title("Time vs Carbon content")
plt.legend()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
plt.xticks(rotation=45)

plt.show()