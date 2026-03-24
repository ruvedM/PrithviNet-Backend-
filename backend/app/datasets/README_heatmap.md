# Pollution Heatmap Data Processing

This script processes city pollution data and generates heatmap-ready files for the frontend map.

**How it works:**
- Loads city_day_cleaned.csv and Indian Cities Database.csv
- Cleans and merges pollution and location data
- Aggregates AQI by city
- Outputs:
  - air_poll_data.csv (for frontend)
  - pollution_heatmap.json (for advanced overlays)

**Usage:**

1. Place this script in backend/app/datasets/
2. Run:
   ```bash
   python data_processing.py
   ```
3. The output files will be saved in the same folder.

**Dependencies:**
- pandas
- numpy

Install with:
```bash
pip install pandas numpy
```

**Integration:**
- The frontend MapUi.jsx fetches air_poll_data.csv for heatmap rendering.
- To use pollution_heatmap.json, update MapUi.jsx to fetch and parse the JSON file.

**Note:**
- You can customize the script to use other pollution columns or datasets as needed.
