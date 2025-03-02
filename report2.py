import pandas as pd
import altair as alt


data_file = "antenna_measurements.csv"
df = pd.read_csv(data_file)
df["date_time"] = pd.to_datetime(df["date_time"])

# --- Analysis Using Median SNR ---

# 1. Overall statistics grouped by antenna (median SNR is our key metric)
antenna_stats = df.groupby("antenna").agg(
    count=("snr", "count"),
    median_snr=("snr", "median"),
    avg_power=("power", "mean"),
    avg_noise=("noise", "mean")
).sort_values(by="median_snr", ascending=False)
print("=== Overall Antenna Stats (by median SNR) ===")
print(antenna_stats, "\n")

# 2. Group by location (if you have more than one)
location_stats = df.groupby("location").agg(
    count=("snr", "count"),
    median_snr=("snr", "median"),
    avg_power=("power", "mean"),
    avg_noise=("noise", "mean")
).sort_values(by="median_snr", ascending=False)
print("=== Overall Location Stats (by median SNR) ===")
print(location_stats, "\n")

# 3. Compare antennas at each location
antenna_location_stats = df.groupby(["location", "antenna"]).agg(
    count=("snr", "count"),
    median_snr=("snr", "median"),
    avg_power=("power", "mean"),
    avg_noise=("noise", "mean")
).sort_values(by="median_snr", ascending=False)
print("=== Antenna Stats by Location (by median SNR) ===")
print(antenna_location_stats, "\n")

# 4. Compare the same antenna with different orientations at a location
antenna_orientation_stats = df.groupby(["location", "antenna", "orientation"]).agg(
    count=("snr", "count"),
    median_snr=("snr", "median"),
    avg_power=("power", "mean"),
    avg_noise=("noise", "mean")
).sort_values(by="median_snr", ascending=False)
print("=== Antenna & Orientation Stats by Location (by median SNR) ===")
print(antenna_orientation_stats, "\n")

# --- Finding Stations with the Greatest SNR Variability ---
# Pivot data to have different configurations as columns (using median SNR)
pivot = df.pivot_table(index='call', columns=['antenna', 'orientation'], values='snr', aggfunc='median')
# Compute the range (max - min) of median SNR for each call
pivot['snr_range'] = pivot.max(axis=1) - pivot.min(axis=1)
pivot_sorted = pivot.sort_values(by='snr_range', ascending=False)
print("=== Stations with the greatest SNR variability ===")
print(pivot_sorted['snr_range'].head(), "\n")

# --- Visualization ---

# 1. Scatter plot: SNR vs Frequency by Antenna and Location
scatter_location = alt.Chart(df).mark_point(size=100, opacity=0.7).encode(
    x=alt.X('frequency:Q', title='Frequency (MHz)'),
    y=alt.Y('snr:Q', title='SNR (dB)'),
    color=alt.Color('antenna:N', legend=alt.Legend(title='Antenna')),
    shape=alt.Shape('location:N', legend=alt.Legend(title='location')),
    tooltip=['antenna', 'orientation', 'frequency', 'snr', 'virtual', 'call']
).properties(
    title='SNR vs Frequency by Antenna and Location',
    width=800,
    height=500
).interactive()
scatter_orientation = alt.Chart(df).mark_point(size=100, opacity=0.7).encode(
    x=alt.X('frequency:Q', title='Frequency (MHz)'),
    y=alt.Y('snr:Q', title='SNR (dB)'),
    color=alt.Color('antenna:N', legend=alt.Legend(title='Antenna')),
    shape=alt.Shape('orientation:N', legend=alt.Legend(title='orientation')),
    tooltip=['antenna', 'orientation', 'frequency', 'snr', 'virtual', 'call']
).properties(
    title='SNR vs Frequency by Antenna and Location',
    width=800,
    height=500
).interactive()


# 2. Box plot: Distribution of SNR by Antenna with Orientation as Color
boxplot = alt.Chart(df).mark_boxplot().encode(
    x=alt.X('antenna:N', title='Antenna'),
    y=alt.Y('snr:Q', title='SNR (dB)'),
    color=alt.Color('orientation:N', legend=alt.Legend(title='Orientation')),
    tooltip=['antenna', 'orientation', 'snr']
).properties(
    title='SNR Distribution by Antenna and Orientation',
    width=800,
    height=500
).interactive()

#scatter & boxplot  # This vertically concatenates the charts

print("Saving scatter.html, orienation.html, boxplot.html")
scatter_location.save('reports/scatter.html')
scatter_orientation.save('reports/orienation.html')
boxplot.save('reports/boxplot.html')


#  pivot_reset = pivot.reset_index()
#  # Use a list comprehension to flatten: if a column is a tuple, join its parts with underscores,
#  # and skip empty strings.
#  pivot_reset.columns = [
#      col if isinstance(col, str) else '_'.join([str(c) for c in col if c])
#      for col in pivot_reset.columns.values
#  ]
#  
#  # Now, inspect the columns:
#  print("Flattened columns:", pivot_reset.columns.tolist())
#  # For this example, we expect to see something like:
#  # ['call', 'rabbit_up-w', 'test_up', 'snr_range_up-n'] 
#  # (Your actual column names may differ.)
#  
#  # --- Compute SNR Difference ---
#  # Check that the expected columns exist.
#  if "rabbit_up-w" in pivot_reset.columns and "test_up" in pivot_reset.columns:
#      pivot_reset['diff'] = pivot_reset["rabbit_up-w"] - pivot_reset["test_up"]
#      pivot_reset['abs_diff'] = pivot_reset['diff'].abs()
#  else:
#      raise ValueError("Expected columns 'rabbit_up-w' and 'test_up' not found in pivot data.")
#  
#  # --- Build an Altair Chart ---
#  # We use 'call' as a nominal variable on the x-axis and 'diff' as the quantitative y-axis.
#  chart = alt.Chart(pivot_reset).mark_point(size=100).encode(
#      x=alt.X("call:N", title="Station (Call)", axis=alt.Axis(labelAngle=-45)),
#      y=alt.Y("diff:Q", title="SNR Difference (rabbit - test)"),
#      color=alt.condition("datum.diff > 0", alt.value("green"), alt.value("red")),
#      tooltip=["call", "diff", "abs_diff"]
#  ).properties(
#      title="SNR Difference by Station\n(Green: rabbit > test, Red: test > rabbit)"
#  )
#  
#  chart.save('foo.html')
