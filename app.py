import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("🌫️ India Air Pollution Cloud Map - Hackathon Special")

data = pd.read_csv("predictions.csv", parse_dates=['Date'])

# Sidebar filters
st.sidebar.header("Filter")
min_date, max_date = data['Date'].min(), data['Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

threshold = st.sidebar.slider("PM2.5 Threshold for Red", 50, 300, 150)

filtered_data = data[
    (data['Date'] >= pd.to_datetime(date_range[0])) & 
    (data['Date'] <= pd.to_datetime(date_range[1]))
]

# Base Map
m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)

# Add heatmap layer
heat_data = [[row['Latitude'], row['Longitude'], row['Predicted_PM2.5']] for index, row in filtered_data.iterrows()]
HeatMap(heat_data, min_opacity=0.4, max_opacity=0.9, radius=15, blur=20).add_to(m)

# Add markers + cloudy effect simulation
for i, row in filtered_data.iterrows():
    pm = row['Predicted_PM2.5']
    color = 'green' if pm < 50 else 'orange' if pm < threshold else 'red'
    opacity = 0 if pm < 50 else 0.3 if pm < threshold else 0.6

    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.9,
        popup=f"PM2.5: {pm:.1f}<br>Date: {row['Date'].date()}"
    ).add_to(m)

    if opacity > 0:
        folium.Circle(
            location=[row['Latitude'], row['Longitude']],
            radius=10000,
            color=None,
            fill=True,
            fill_color='white',
            fill_opacity=opacity
        ).add_to(m)

st_folium(m, width=1300, height=700)

# Colorbar legend
st.markdown("""
<div style='display: flex; justify-content: center;'>
    <div style='width: 300px; height: 30px; background: linear-gradient(to right, green , yellow , orange , red); border: 1px solid black;'></div>
</div>
<p style='text-align: center;'>Low PM2.5 ←→ High PM2.5</p>
""", unsafe_allow_html=True)