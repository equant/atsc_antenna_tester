import os, glob
import datetime
import requests
from io import StringIO
import pandas as pd

def fetch_fcc_data(city, state):
    """
    Fetch FCC data for the given city and state.
    """
    base_url = "https://transition.fcc.gov/fcc-bin/tvq"
    # query parameters; maybe one day want these?
    params = {
        "call": "",
        "filenumber": "",
        "state": state.upper(),
        "city": city,
        "chan": "0",
        "cha2": "36",
        "serv": "",
        "status": "",
        "facid": "",
        "asrn": "",
        "list": "4",
        "dist": "",
        "dlat2": "",
        "mlat2": "",
        "slat2": "",
        "NS": "N",
        "dlon2": "",
        "mlon2": "",
        "slon2": "",
        "EW": "W",
        "size": "9",
        "NextTab": "Results to Next Page/Tab"
    }
    response = requests.get(base_url, params=params)
    raw_text = response.text

    df = pd.read_csv(StringIO(raw_text), sep="|", header=None)
    # Remove the first and last empty columns (due to leading and trailing pipes).
    df = df.iloc[:, 1:-1]

    # Assign column names to key fields we know
    col_names = list(df.columns)
    col_names[0] = "Call"
    col_names[3] = "Channel"
    col_names[37] = "Virtual Channel"
    df.columns = col_names

    return df

def save_fcc_data(df, city, state, directory="../data/fcc"):
    """
    Save the FCC DataFrame to a CSV file in the given directory.
    The filename includes the state, city, and a timestamp.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H")
    # Replace spaces with underscores for a safe filename.
    filename = f"fcc_data_{state.upper()}_{city.replace(' ', '_')}_{timestamp}.csv"
    filepath = os.path.join(directory, filename)
    df.to_csv(filepath, index=False)
    return filepath

def get_most_recent_fcc_data(city, state, directory="../data/fcc"):
    """
    Find the most recent CSV file for the given city and state.
    """
    pattern = os.path.join(directory, f"fcc_data_{state.upper()}_{city.replace(' ', '_')}_*.csv")
    files = glob.glob(pattern)
    if not files:
        return None
    # Use file modification time to get the most recent file.
    most_recent = max(files, key=os.path.getmtime)
    return most_recent
