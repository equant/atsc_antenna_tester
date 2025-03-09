import streamlit as st
import pandas as pd
import os
import myFcc

# Streamlit UI
st.title("FCC Data Downloader")

st.write("Enter the city and state of interest")

city_input = st.text_input("City", "Tucson")
state_input = st.text_input("State (e.g., AZ)", "AZ")

if st.button("Download OTA Broadcaster Data From FCC"):
    with st.spinner("Downloading data..."):
        df = myFcc.fetch_fcc_data(city_input, state_input)
        filepath = myFcc.save_fcc_data(df, city_input, state_input)
    st.success(f"Data saved to {filepath}")
    st.write("Sample Data:")
    st.dataframe(df.head())

st.write("---")
if st.button("Load Most Recent Local Copy of FCC Data"):
    recent_file = myFcc.get_most_recent_fcc_data(city_input, state_input)
    if recent_file:
        recent_df = pd.read_csv(recent_file)
        st.success(f"Loaded most recent file: {recent_file}")
        st.write("Data from most recent file:")
        st.dataframe(recent_df)
    else:
        st.warning("No data files found for that city and state.")

