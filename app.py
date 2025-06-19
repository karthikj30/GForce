import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("India Air Pollution Map - PM2.5 Predictions")

# Load prediction data
data = pd.read_csv("predictions.csv")

# Create base map centered over India
m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)

# Add data points to map
for i, row in data.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='red' if row['Predicted_PM2.5'] > 150 else 'green',
        fill=True,
        fill_opacity=0.7,
        popup=f"PM2.5: {row['Predicted_PM2.5']:.2f}"
    ).add_to(m)

st_folium(m, width=1300, height=600)
