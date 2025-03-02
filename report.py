import datetime, curses, requests, os
import requests
import numpy as np
import pandas as pd
from io import StringIO
from rtlsdr import RtlSdr


data_file = "antenna_measurements.csv"
df = pd.read_csv(data_file)

import pandas as pd

# Step 1. Read in the dataframe.
# If your data is stored in a CSV file (for example, "tv_data.csv"), use:
# df = pd.read_csv("tv_data.csv")
# For demonstration, we'll assume df is already defined.
# (Replace the code below with your actual data loading method if needed.)
data = {
    "antenna": ["test", "test", "test", "test", "test", "rabbit", "rabbit", "rabbit", "rabbit", "rabbit"],
    "location": ["desk"] * 10,
    "orientation": ["up", "up", "up", "up", "up", "up-w", "up-w", "up-w", "up-w", "up-w"],
    "date_time": [
        "2025-02-23 12:31:22.034491", "2025-02-23 12:31:25.986421", "2025-02-23 12:31:29.907165",
        "2025-02-23 12:31:33.805414", "2025-02-23 12:31:37.711958", "2025-02-23 12:47:20.532853",
        "2025-02-23 12:47:24.464058", "2025-02-23 12:47:28.495583", "2025-02-23 12:47:32.457199",
        "2025-02-23 12:47:36.445339"
    ],
    "call": ["KGUN-TV", "KOLD-TV", "KUDF-LP", "KUDF-LD", "KHRR",
             "KPCE-LD", "KUAT-TV", "KOLD-TV", "K35OU-D", "KUVE-CD"],
    "channel": [9, 13, 14, 14, 16, 29, 30, 32, 35, 36],
    "virtual": [9, 13, 14, 14, 40, 29, 6, 13, 35, 38],
    "frequency": [186.31, 210.31, 470.31, 470.31, 482.31, 560.31, 566.31, 578.31, 596.31, 602.31],
    "power": [57.238234, 55.117849, 43.673060, 45.105388, 53.394248, 56.883310, 52.046340, 51.146597, 45.467280, 51.677938],
    "noise": [51.309781, 50.415086, 39.123311, 39.333913, 53.592452, 50.012152, 49.788862, 45.578572, 44.162682, 51.145682],
    "snr": [5.928453, 4.702763, 4.549748, 5.771475, -0.198204, 6.871158, 2.257478, 5.568025, 1.304598, 0.532256]
}
df = pd.DataFrame(data)

# Step 2. Convert date_time to a datetime object.
df["date_time"] = pd.to_datetime(df["date_time"])

# Step 3. Calculate summary statistics.
# (These are example aggregations—you can change the metrics as needed.)

# Compare antennas (overall, regardless of location/orientation)
antenna_stats = df.groupby("antenna").agg(
    count=("snr", "count"),
    avg_snr=("snr", "mean"),
    avg_power=("power", "mean"),
    avg_noise=("noise", "mean")
).sort_values(by="avg_snr", ascending=False)

# Compare locations (overall)
location_stats = df.groupby("location").agg(
    count=("snr", "count"),
    avg_snr=("snr", "mean"),
    avg_power=("power", "mean"),
    avg_noise=("noise", "mean")
).sort_values(by="avg_snr", ascending=False)

# Compare antennas at each location
antenna_location_stats = df.groupby(["location", "antenna"]).agg(
    count=("snr", "count"),
    avg_snr=("snr", "mean"),
    avg_power=("power", "mean"),
    avg_noise=("noise", "mean")
).sort_values(by="avg_snr", ascending=False)

# Compare the same antenna with different orientations at the same location
antenna_orientation_stats = df.groupby(["location", "antenna", "orientation"]).agg(
    count=("snr", "count"),
    avg_snr=("snr", "mean"),
    avg_power=("power", "mean"),
    avg_noise=("noise", "mean")
).sort_values(by="avg_snr", ascending=False)

# Step 4. Print the results.
print("=== Overall Antenna Stats ===")
print(antenna_stats, "\n")

print("=== Overall Location Stats ===")
print(location_stats, "\n")

print("=== Antenna Stats by Location ===")
print(antenna_location_stats, "\n")

print("=== Antenna & Orientation Stats by Location ===")
print(antenna_orientation_stats, "\n")


