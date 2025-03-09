import datetime, curses, requests, os
import requests
import numpy as np
import pandas as pd
from io import StringIO
from rtlsdr import RtlSdr

# Initialize RTL-SDR
sdr = RtlSdr()
sdr.sample_rate = 2.4e6  # 2.4 MSPS
sdr.gain = 'auto'
bandwidth_hz = 2400 # 2.4 kHz


def measure_power(frequency, num_measurements=10):
    power_values = []
    for _ in range(num_measurements):
        sdr.center_freq = frequency * 1e6
        samples = sdr.read_samples(256 * 1024)
        fft_vals = np.fft.fftshift(np.fft.fft(samples))
        power_spectrum = 20 * np.log10(np.abs(fft_vals))

        # Find the power at the center frequency
        freqs = np.fft.fftshift(np.fft.fftfreq(len(samples), 1 / sdr.sample_rate))
        mask = (freqs >= -bandwidth_hz / 2) & (freqs <= bandwidth_hz / 2)
        power = np.mean(power_spectrum[mask])
        power_values.append(power)
    print(", ".join([f"{x:.2f}" for x in power_values]))

    return np.mean(power_values)

def fix_virtual_channel(row):
    try:
        return int(row["Virtual Channel"])
    except (ValueError, TypeError):
        #print(f"Can't convert: [{row["Virtual Channel"]}]")
        return row["Channel"]

def main(stdscr):

    import Things
    antennas = Things.Antenna()
    locations = Things.Location()
    orientations = Things.Orientation()

    selected_antenna = antennas.select(stdscr)
    selected_location = locations.select(stdscr)
    selected_orientation = orientations.select(stdscr)


    stdscr.clear()
    stdscr.addstr(2, 2, f"Antenna: {selected_antenna}")
    stdscr.addstr(3, 2, f"Location: {selected_location}")
    stdscr.addstr(4, 2, f"Orientation: {selected_orientation}")
    stdscr.addstr(6, 2, "Press any key to continue.")
    stdscr.refresh()
    stdscr.getch()
    curses.endwin()  # End curses mode

    antenna_name = selected_antenna
    location = selected_location
    orientation = selected_orientation

    data_file = "antenna_measurements.csv"

    # https://transition.fcc.gov/fcc-bin/tvq?call=&filenumber=&state=AZ&city=Tucson&chan=0&cha2=36&serv=&status=&facid=&asrn=&list=4&dist=&dlat2=&mlat2=&slat2=&NS=N&dlon2=&mlon2=&slon2=&EW=W&size=9&NextTab=Results+to+Next+Page%2FTab
    fcc_url = "https://transition.fcc.gov/fcc-bin/tvq?call=&filenumber=&state=AZ&city=Tucson&chan=0&cha2=36&list=4&NS=N&9"

    #fcc_url = ("https://transition.fcc.gov/fcc-bin/tvq?call=&filenumber=&state=AZ&city=Tucson&chan=0&"
           #"cha2=36&serv=&status=&facid=&asrn=&list=4&dist=&dlat2=&mlat2=&slat2=&NS=N&"
           #"dlon2=&mlon2=&slon2=&EW=W&size=9&NextTab=Results+to+Next+Page%2FTab")

    response = requests.get(fcc_url)
    raw_text = response.text

    fcc_df = pd.read_csv(StringIO(raw_text), sep="|", header=None)
    fcc_df = fcc_df.iloc[:, 1:-1]

    col_names = list(fcc_df.columns)
    col_names[0] = "Call"
    col_names[3] = "Channel"
    col_names[37] = "Virtual Channel"
    fcc_df.columns = col_names

    pilot_frequencies = {
             2 :  54.31, 3 :  60.31, 4 :  66.31, 5 :  76.31, 6 :  82.31, 7 : 174.31,
             8 : 180.31, 9 : 186.31, 10 : 192.31, 11 : 198.31, 12 : 204.31, 13 : 210.31,
            14 : 470.31, 15 : 476.31, 16 : 482.31, 17 : 488.31, 18 : 494.31, 19 : 500.31,
            20 : 506.31, 21 : 512.31, 22 : 518.31, 23 : 524.31, 24 : 530.31, 25 : 536.31,
            26 : 542.31, 27 : 548.31, 28 : 554.31, 29 : 560.31, 30 : 566.31, 31 : 572.31,
            32 : 578.31, 33 : 584.31, 34 : 590.31, 35 : 596.31, 36 : 602.31, 37 : 608.31,
            38 : 614.31, 39 : 620.31, 40 : 626.31, 41 : 632.31, 42 : 638.31, 43 : 644.31,
            44 : 650.31, 45 : 656.31, 46 : 662.31, 47 : 668.31, 48 : 674.31, 49 : 680.31,
            50 : 686.31, 51 : 692.31, 52 : 698.31, 53 : 704.31, 54 : 710.31, 55 : 716.31,
            56 : 722.31, 57 : 728.31, 58 : 734.31, 59 : 740.31, 60 : 746.31, 61 : 752.31,
            62 : 758.31, 63 : 764.31, 64 : 770.31, 65 : 776.31, 66 : 782.31, 67 : 788.31,
            68 : 794.31, 69 : 800.31, 70 : 806.31, 71 : 812.31, 72 : 818.31, 73 : 824.31,
            74 : 830.31, 75 : 836.31, 76 : 842.31, 77 : 848.31, 78 : 854.31, 79 : 860.31,
            80 : 866.31, 81 : 872.31, 82 : 878.31, 83 : 884.31,
    }


    channels_of_interest = [18.5, 6.3, 4.2, 9.2, 13.1, 27.1, 46.3]

    fcc_df["Virtual Channel"] = fcc_df.apply(fix_virtual_channel, axis=1)



    # Load existing dataframe or create a new one
    try:
        df = pd.read_csv(data_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["antenna", "location", "orientation", "date_time", "call", "channel", "virtual", "frequency", "power", "noise", "snr"])

    # Measure power and noise for each channel
    for idx, row in fcc_df.iterrows():
        print(f"--------------- [ {idx+1} of {len(fcc_df)}] -------------")
        print(f"{row['Call']}")
        channel = row['Channel']
        vchannel = row['Virtual Channel']
        freq = pilot_frequencies[channel]

        # Measure power at the pilot frequency
        power = measure_power(freq)

        # Measure noise adjacent to the pilot frequency
        noise = measure_power(freq + 0.01)

        # Calculate SNR
        snr = power - noise

        print(f"SNR: {snr}")

        new_row = pd.DataFrame([{
            "antenna": antenna_name,
            "location": location,
            "orientation": selected_orientation,
            "date_time": datetime.datetime.now(),
            "call": row["Call"],
            "channel": channel,
            "virtual": vchannel,
            "frequency": freq,
            "power": power,
            "noise": noise,
            "snr": snr
        }])
        df = pd.concat([df, new_row], ignore_index=True)

    # Print results
    for _, row in df.iterrows():
        print(f"Antenna: {row['antenna']} | Location: {row['location']} | Virt: {row['virtual']} | RF Channel: {row['channel']} | Power: {row['power']:.2f} dB | Noise: {row['noise']:.2f} dB | SNR: {row['snr']:.2f} dB")

    # Save the dataframe back to disk
    df.to_csv(data_file, index=False)

    # Close the RTL-SDR
    sdr.close()

    print("Data saved to", data_file)
    print(df.sort_values(by="snr", ascending=False))

if __name__ == "__main__":
    curses.wrapper(main)
