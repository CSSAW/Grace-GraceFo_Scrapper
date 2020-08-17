import pandas as pd
import streamlit as st

st.title("Grace/Grace-Fo Data Visualization")
all_data = pd.read_csv("*/Grace-GraceFo_Scrapper/all_data.csv")

# Parse the coordinate from (lat, lon) to separate lat, lon columns
lon = []
lat = []
for coord in all_data["Coordinate"]:
  longitude = coord.split(",")[1][:-1]
  latitude = coord.split(",")[0][1:]
  lon.append(longitude)
  lat.append(latitude)

all_data.drop(columns="Coordinate", inplace=True)
all_data.insert(0, "longitude", lon)
all_data.insert(1, "latitude", lat)


# create a select bar
date = []
for row in all_data:
  if row != "longitude" and row != "latitude":
    date.append(row)

year_month = st.selectbox("Select date", date, "20020417")

year_data = pd.DataFrame()
# present data in range
year_data.insert(0, "longitude", lon)
year_data.insert(1, "latitude", lat)
year_data.insert(2, "lwe_data", all_data[year_month])

if st.checkbox("View mapped 3D data"):
  st.map(year_data)
elif st.checkbox("View raw data"):
  st.write(year_data)


