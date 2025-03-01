import pandas as pd
import folium
from folium.plugins import HeatMap

# Load crime data

outcome_file = "../3228c05a10f136b972bcc8c7a1cf333e9bf76b84/2024-12/2024-12-city-of-london-outcomes.csv"  # Your second CSV (if needed)
crime_file = "../3228c05a10f136b972bcc8c7a1cf333e9bf76b84/2024-12/2024-12-city-of-london-street.csv"  # Change to your actual file

df_crime = pd.read_csv(crime_file)
df_outcome = pd.read_csv(outcome_file)

# Merge both datasets on 'Crime ID' (keeping all crimes even if no outcome exists)
df = df_crime.merge(df_outcome[['Crime ID', 'Outcome type']], on="Crime ID", how="left")

# Define column names for location and details
lat_col, lon_col = "Latitude", "Longitude"
info_cols = ["Crime type", "Location", "Month", "Outcome type"]  # Correct column names

# Drop rows with missing location data
df = df.dropna(subset=[lat_col, lon_col])

# Create a base map centered on the dataset
m = folium.Map(location=[df[lat_col].mean(), df[lon_col].mean()], zoom_start=12)

# Create a heatmap layer
heat_data = df[[lat_col, lon_col]].values.tolist()
HeatMap(heat_data).add_to(m)

# Add Markers with popups
for _, row in df.iterrows():
    popup_info = "<br>".join([f"<b>{col}:</b> {row[col]}" for col in info_cols if pd.notna(row[col])])

    # Ensure there is at least some content in the popup
    popup_info = popup_info if popup_info else "No details available"

    folium.Marker(
        location=[row[lat_col], row[lon_col]],
        popup=folium.Popup(popup_info, max_width=300),
        tooltip="Click for details",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Save and display the map
m.save("crime_map_with_details.html")
print("Map saved as crime_map_with_details.html")
