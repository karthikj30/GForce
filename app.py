import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import numpy as np

st.set_page_config(layout="wide")
st.title("India Air Pollution Prediction Map - Advanced Dashboard")

data = pd.read_csv("predictions.csv", parse_dates=['Date'])

# Sidebar filter
st.sidebar.header("Filter Options")
min_date = data['Date'].min()
max_date = data['Date'].max()
date_range = st.sidebar.date_input("Select date range", [min_date, max_date])
threshold = st.sidebar.slider("PM2.5 Threshold (for color)", 0, 300, 150)

# Filter data based on user input
filtered_data = data[
    (data['Date'] >= pd.to_datetime(date_range[0])) &
    (data['Date'] <= pd.to_datetime(date_range[1]))
]

# Create base map
m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)

# Add heatmap layer
heat_data = [[row['Latitude'], row['Longitude'], row['Predicted_PM2.5']] for index, row in filtered_data.iterrows()]
HeatMap(heat_data, min_opacity=0.4, max_opacity=0.9, radius=15, blur=20).add_to(m)

# Add colored circle markers
for i, row in filtered_data.iterrows():
    color = 'green' if row['Predicted_PM2.5'] < threshold else 'red'
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color=color,
        fill=True,
        fill_opacity=0.8,
        popup=f"PM2.5: {row['Predicted_PM2.5']:.2f}<br>Date: {row['Date'].date()}"
    ).add_to(m)

st_folium(m, width=1300, height=700)

# Add colorbar legend
st.markdown("""
<div style='display: flex; justify-content: center;'>
    <div style='width: 300px; height: 30px; background: linear-gradient(to right, green , yellow , orange , red); border: 1px solid black;'></div>
</div>
<p style='text-align: center;'>Low PM2.5 ←→ High PM2.5</p>
""", unsafe_allow_html=True)