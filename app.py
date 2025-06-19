import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("🌫️ India Air Pollution - Hackathon Ultimate App 🚀")

# Load data
data = pd.read_csv("predictions.csv", parse_dates=['Date'])

# Sidebar filters
st.sidebar.header("Filters")
cities = ['All'] + sorted(data['City'].unique().tolist())
selected_city = st.sidebar.selectbox("Select City", cities)
threshold = st.sidebar.slider("PM2.5 Threshold for Red", 50, 300, 150)

min_date, max_date = data['Date'].min(), data['Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Apply filters
filtered_data = data[
    (data['Date'] >= pd.to_datetime(date_range[0])) &
    (data['Date'] <= pd.to_datetime(date_range[1]))
]
if selected_city != 'All':
    filtered_data = filtered_data[filtered_data['City'] == selected_city]

# Create folium map
m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)

# Animated heatmap data
heatmap_data = []
for date, day_df in filtered_data.groupby('Date'):
    heatmap_data.append(
        [[row['Latitude'], row['Longitude'], row['Predicted_PM2.5']] for index, row in day_df.iterrows()]
    )

HeatMapWithTime(
    heatmap_data,
    index=filtered_data['Date'].dt.strftime('%Y-%m-%d').unique().tolist(),
    radius=15,
    auto_play=True,
    max_opacity=0.9
).add_to(m)

# Circle markers + cloud effect
for i, row in filtered_data.iterrows():
    pm = row['Predicted_PM2.5']
    color = 'green' if pm < 50 else 'orange' if pm < threshold else 'red'
    opacity = 0 if pm < 50 else 0.3 if pm < threshold else 0.6

    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color=color,
        fill=True,
        fill_opacity=0.9,
        popup=f"City: {row['City']}<br>PM2.5: {pm:.1f}<br>Date: {row['Date'].date()}"
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

# Display map
st_folium(m, width=1300, height=700)

# Colorbar legend
st.markdown("""
<div style='display: flex; justify-content: center;'>
    <div style='width: 300px; height: 30px; background: linear-gradient(to right, green , yellow , orange , red); border: 1px solid black;'></div>
</div>
<p style='text-align: center;'>Low PM2.5 ←→ High PM2.5</p>
""", unsafe_allow_html=True)

# Export option
if st.button("📷 Export Map Screenshot"):
    st.warning("You can take screenshot manually or use browser capture tools. Streamlit-folium export still experimental!")