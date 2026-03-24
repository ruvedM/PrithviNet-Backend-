import pandas as pd
import numpy as np
import os
import csv
import json

# Paths to datasets
DATA_DIR = os.path.dirname(__file__)
CITY_DAY = os.path.join(DATA_DIR, 'city_day_cleaned.csv')
CITIES_DB = os.path.join(DATA_DIR, 'Indian Cities Database.csv')

# Load city pollution data
city_df = pd.read_csv(CITY_DAY)

# Load city coordinates
cities_db = pd.read_csv(CITIES_DB)


# --- Enhanced Heatmap Processing ---
pollutants = ['AQI', 'PM2_5', 'PM10']
output_files = {}

for pollutant in pollutants:
    # Clean and filter
    city_poll_df = city_df.dropna(subset=['City', pollutant])
    city_poll_df = city_poll_df.merge(cities_db[['City', 'Lat', 'Long']], on='City', how='left')
    city_poll_df = city_poll_df.dropna(subset=['Lat', 'Long'])

    # Aggregate by city/date for dynamic filtering
    agg_df = city_poll_df.groupby(['City', 'Lat', 'Long', 'Date'])[pollutant].mean().reset_index()

    # Prepare heatmap data
    heatmap_data = agg_df[['Lat', 'Long', pollutant]].values.tolist()

    def normalize(val):
        if pollutant == 'AQI':
            if val >= 400:
                return 1.0
            elif val >= 300:
                return 0.85
            elif val >= 200:
                return 0.65
            elif val >= 100:
                return 0.45
            else:
                return 0.25
        elif pollutant == 'PM2_5':
            if val >= 250:
                return 1.0
            elif val >= 150:
                return 0.85
            elif val >= 100:
                return 0.65
            elif val >= 50:
                return 0.45
            else:
                return 0.25
        elif pollutant == 'PM10':
            if val >= 400:
                return 1.0
            elif val >= 300:
                return 0.85
            elif val >= 200:
                return 0.65
            elif val >= 100:
                return 0.45
            else:
                return 0.25
        else:
            return 0.5

    heatmap_data = [[lat, lon, normalize(val)] for lat, lon, val in heatmap_data]

    # Save as CSV for frontend
    csv_path = os.path.join(DATA_DIR, f'air_poll_data_{pollutant.lower()}.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['city', 'latitude', 'longitude', 'date', pollutant.lower()])
        for row in agg_df.itertuples():
            writer.writerow([row.City, row.Lat, row.Long, row.Date, getattr(row, pollutant)])
    output_files[pollutant] = csv_path

    # Save heatmap data as JSON
    json_path = os.path.join(DATA_DIR, f'pollution_heatmap_{pollutant.lower()}.json')
    with open(json_path, 'w') as f:
        json.dump(heatmap_data, f)

print(f"Saved heatmap files: {output_files}")