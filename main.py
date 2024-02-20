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

# Lists for data
time_subsets = []
carbon_content_subsets = []
interpolations = []

# Interpolation for each sample
for i in range(num_chunks):
    # Get the subsets we're working with
    time_subset = times[i*sample_size:(i+1)*sample_size]
    carbon_content_subset = carbon_content[i*sample_size:(i+1)*sample_size]

    # Perform interpolation, and add it to our interpolations list
    interpolations.append(CubicSpline(time_subset, carbon_content_subset))

    # Add the subsets of data for easy indexing
    time_subsets.append(time_subset)
    carbon_content_subsets.append(carbon_content_subset)


# Plot the Cubic Spline Interpolation of the [test_index]
TEST_INDEX = 0 #EDIT THIS IF YOU WANT TO CHANGE THE SUBSET

time_subset = time_subsets[TEST_INDEX]
carbon_content_subset = carbon_content_subsets[TEST_INDEX]
interpolation = interpolations[TEST_INDEX]

time_min = time_subset.min()
time_max = time_subset.max()

# X and Y values for the interpolation
cubic_x = pd.date_range(time_min, time_max, 1000)
cubic_y = interpolation(cubic_x)

# Actual plot code
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