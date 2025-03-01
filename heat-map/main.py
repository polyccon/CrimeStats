import pandas as pd
import folium
from folium.plugins import HeatMap


outcome_file = "../3228c05a10f136b972bcc8c7a1cf333e9bf76b84/2024-12/2024-12-city-of-london-outcomes.csv"  # Your second CSV (if needed)
crime_file = "../3228c05a10f136b972bcc8c7a1cf333e9bf76b84/2024-12/2024-12-city-of-london-street.csv"  # Change to your actual file
stop_search_file = "../3228c05a10f136b972bcc8c7a1cf333e9bf76b84/2024-12/2024-12-city-of-london-stop-and-search.csv"  # Stop and Search data

df_crime = pd.read_csv(crime_file)
df_outcome = pd.read_csv(outcome_file)
df_search = pd.read_csv(stop_search_file)

# Merge crime and outcome datasets
df = df_crime.merge(df_outcome[['Crime ID', 'Outcome type']], on="Crime ID", how="left")

# Drop missing location data
df = df.dropna(subset=["Latitude", "Longitude"])
df_search = df_search.dropna(subset=["Latitude", "Longitude"])

# Create a base map centered on the dataset
m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=12)

# Add crime heatmap
heat_data = df[["Latitude", "Longitude"]].values.tolist()
HeatMap(heat_data, name="Crime Heatmap").add_to(m)

# Add crime markers with popups
for _, row in df.iterrows():
    popup_info = "<br>".join(
        [f"<b>{col}:</b> {row[col]}" for col in ["Crime type", "Location", "Month", "Outcome type"] if
         pd.notna(row[col])]
    )
    popup_info = popup_info if popup_info else "No details available"

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=folium.Popup(popup_info, max_width=300),
        tooltip="Crime details",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Add stop and search markers (different color)
for _, row in df_search.iterrows():
    popup_info = "<br>".join(
        [f"<b>{col}:</b> {row[col]}" for col in
         ["Type", "Date", "Gender", "Age range", "Self-defined ethnicity", "Object of search", "Outcome"] if
         pd.notna(row[col])]
    )
    popup_info = popup_info if popup_info else "No details available"

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=folium.Popup(popup_info, max_width=300),
        tooltip="Stop & Search details",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# Save and display the map
m.save("crime_and_search_map.html")
print("Map saved as crime_and_search_map.html")
