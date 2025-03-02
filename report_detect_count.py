import pandas as pd
import altair as alt

DETECTION_SNR = 2

data_file = "antenna_measurements.csv"
df = pd.read_csv(data_file)
df['date_time'] = pd.to_datetime(df['date_time'])

reading_count_df = df.groupby(['antenna', 'location', 'orientation']).count().snr
detection_count_df = df[df['snr']>DETECTION_SNR].groupby(['antenna', 'location', 'orientation']).count().snr

detections_per_reading = detection_count_df / reading_count_df

print(f"DETECTION_SNR: {DETECTION_SNR}")
print(detections_per_reading.sort_values(ascending=False))

