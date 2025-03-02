import pandas as pd
import altair as alt

data_file = "antenna_measurements.csv"
df = pd.read_csv(data_file)
df['date_time'] = pd.to_datetime(df['date_time'])

# Bin timestamps into 15-minute windows.
df['scan_time'] = df['date_time'].dt.floor('15min')

# Group by antenna and scan_time, and compute the median SNR and count (for reference)
grouped = df.groupby(['antenna', 'scan_time']).agg(
    median_snr=('snr', 'median'),
    count=('snr', 'count')
).reset_index()

# single Altair chart with a line for each antenna.
chart = alt.Chart(grouped).mark_line(point=True).encode(
    x=alt.X('scan_time:T', title='Scan Time (15-min bins)'),
    y=alt.Y('median_snr:Q', title='Median SNR (dB)'),
    color=alt.Color('antenna:N', title='Antenna'),
    tooltip=['antenna', 'scan_time:T', 'median_snr', 'count']
).properties(
    title='Scan-to-Scan Variability in SNR by Antenna',
        width=800,
            height=500

)

chart.save("reports/time_report.html")

# Facet the chart by antenna, creating a separate panel for each.
facet_chart = alt.Chart(grouped).mark_line(point=True).encode(
    x=alt.X('scan_time:T', title='Scan Time (15-min bins)'),
    y=alt.Y('median_snr:Q', title='Median SNR (dB)'),
    tooltip=['antenna', 'scan_time:T', 'median_snr', 'count']
).facet(
    column=alt.Column('antenna:N', title='Antenna')
).properties(
    title='Scan-to-Scan Variability in SNR for Each Antenna',
        #width=800,
)

print("Saving time_report_facet.html")
facet_chart.save("reports/time_report_facet.html")


# Simer series plots

chart = alt.Chart(df).mark_point().encode(
    x=alt.X('date_time:T', title='Scan Time (15-min bins)'),
    y=alt.Y('snr:Q', title='SNR (dB)'),
    color=alt.Color('antenna:N', title='Antenna'),
    tooltip=['antenna', 'date_time:T', 'snr']
).properties(
    title='Scatter Plot of SNR Readings Over Time by Antenna',
    width=800,
    height=500
)

print("Saving time_report_full.html")
chart.save("reports/time_report_full.html")

chart = alt.Chart(df).mark_point().encode(
    x=alt.X('date_time:T', title='Time'),
    y=alt.Y('snr:Q', title='SNR (dB)'),
    tooltip=['antenna', 'date_time:T', 'snr']
).facet(
    column=alt.Column('antenna:N', title='Antenna')
).properties(
    title='Scatter Plot of SNR Readings Over Time for Each Antenna',
    #width=800,
    #height=500
)
print("Saving time_report_full_facet.html")
chart.save("reports/time_report_full_facet.html")
