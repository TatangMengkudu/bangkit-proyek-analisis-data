import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

dir = 'dashboard'
merge_df = pd.read_csv(os.path.join(dir, "all_data.csv"))

# Sidebar
st.sidebar.title("Bike Rental Dashboard")

# Date Range Selector
st.sidebar.subheader("Date Range Selector")
start_date = pd.to_datetime(st.sidebar.date_input("Start Date", pd.to_datetime(merge_df['dteday'].min())))
end_date = pd.to_datetime(st.sidebar.date_input("End Date", pd.to_datetime(merge_df['dteday'].max())))

# Convert 'dteday' column to datetime
merge_df['dteday'] = pd.to_datetime(merge_df['dteday'])
filtered_df = merge_df[(merge_df['dteday'] >= start_date) & (merge_df['dteday'] <= end_date)]

# Extract 'weekday' after converting 'dteday' to datetime
filtered_df['weekday'] = filtered_df['dteday'].dt.day_name()

# Data preview
if st.sidebar.checkbox("Show Data Preview"):
    st.subheader("Data Preview")
    st.write(filtered_df.sample(5))

# Visualization - Mean Count of Bikes Rented per Season
st.subheader("Mean Count of Bikes Rented per Season")
season_pie = filtered_df.groupby('season_y').mean(numeric_only=True)['cnt_y']
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(season_pie, labels=season_pie.index, autopct='%.2f%%', colors=['#99ff99', '#ffcc99', '#ff9999', '#66b3ff'])
ax.set_title("Mean Count of Bikes Rented per Season")
st.pyplot(fig)

# Visualization - Mean Count of Bikes Rented per Weather Situation
st.subheader("Mean Count of Bikes Rented per Weather Situation")
weather_bar = filtered_df.groupby('weathersit_x').mean(numeric_only=True)['cnt_y']
fig, ax = plt.subplots(figsize=(10, 6))
weather_bar.plot(kind='bar', color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
ax.set_title("Mean Count of Bikes Rented per Weather Situation")
ax.set_xlabel("Weather Situation")
ax.set_ylabel("Mean Count of Bikes Rented")
ax.set_xticklabels(weather_bar.index, rotation=0)
st.pyplot(fig)

st.markdown("""
### Insights and Observations:

1. **Seasonal Distribution:**
   - The pie chart displays the percentage distribution of bike rentals across different seasons.
   - Notable Insight: The majority of bike rentals occur during the fall season, highlighting a potential correlation with favorable weather conditions.

2. **Weather Impact:**
   - The bar chart demonstrates how different weather situations influence the mean count of bikes rented.
   - Notable Insight: Clear weather conditions tend to attract more bike rentals, while heavy rain or thunderstorms result in lower counts.

3. **Date Range Selection:**
   - Utilize the date range selector to focus on specific periods and observe trends or anomalies over time.
    - Notable Insight: Analyzing bike rental patterns during peak seasons or extreme weather conditions can provide valuable insights for business planning and resource allocation.
""")
