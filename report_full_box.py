
import pandas as pd
import altair as alt

data_file = "antenna_measurements.csv"
df = pd.read_csv(data_file)
df['date_time'] = pd.to_datetime(df['date_time'])


df['combo'] = df['antenna'] + " | " + df['orientation'] + " | " + df['location']

order_df = df.groupby('combo')['snr'].median().reset_index()
order_df = order_df.sort_values(by='snr', ascending=False)
order_list = order_df['combo'].tolist()

boxplot = alt.Chart(df).mark_boxplot().encode(
    x=alt.X('combo:N', sort=order_list, title='Antenna | Orientation | Location'),
    y=alt.Y('snr:Q', title='SNR (dB)'),
    color=alt.Color('orientation:N', legend=alt.Legend(title='Orientation')),
    tooltip=['antenna', 'orientation', 'location', 'snr']
).properties(
    title='SNR Distribution by Antenna, Orientation, and Location',
    width=800,
    height=500
)

print("Saving boxplot_big.html")
boxplot.save("reports/boxplot_big.html")
