import folium
import geopandas as gpd
from shapely.geometry import Polygon

# Sample fish information dictionary (replace with actual data)
fish_info = {
    (0, 0): ["Piranha", "Catfish"],
    (0, 1): ["Trout", "Salmon"],
    (4, 3): ["Piranha", "Catfish"],
    # Add more fish information for other grid squares as needed
}

# Define the fish species you want to display the squares for
target_fish = "Piranha"  # Change this to the fish species you're interested in

# Load French Guiana boundary data
gdf = gpd.read_file("mapp.geojson")

# Get the bounding box of French Guiana
bounds = gdf.total_bounds
min_lon, min_lat, max_lon, max_lat = bounds

# Define grid parameters
grid_size = 0.4  # Size of each grid square in degrees

# Calculate the number of rows and columns
num_rows = int((max_lat - min_lat) / grid_size)
num_cols = int((max_lon - min_lon) / grid_size)

# Create a Folium map centered on French Guiana
m = folium.Map(location=[(min_lat + max_lat) / 2, (min_lon + max_lon) / 2], zoom_start=8)

# Iterate over each grid square to add to the map
for i in range(num_rows):
    for j in range(num_cols):
        # Check if the target fish species exists in this grid square
        if target_fish in fish_info.get((i, j), []):
            # Calculate grid boundaries
            grid_min_lat = min_lat + i * grid_size
            grid_max_lat = min_lat + (i + 1) * grid_size
            grid_min_lon = min_lon + j * grid_size
            grid_max_lon = min_lon + (j + 1) * grid_size
            
            # Create Polygon for grid square
            polygon = Polygon([(grid_min_lon, grid_min_lat), 
                               (grid_max_lon, grid_min_lat), 
                               (grid_max_lon, grid_max_lat), 
                               (grid_min_lon, grid_max_lat),
                               (grid_min_lon, grid_min_lat)])
            
            # Define grid square geometry
            grid_geometry = {
                "type": "Polygon",
                "coordinates": [[(grid_min_lon, grid_min_lat), 
                                 (grid_max_lon, grid_min_lat), 
                                 (grid_max_lon, grid_max_lat), 
                                 (grid_min_lon, grid_max_lat),
                                 (grid_min_lon, grid_min_lat)]]
            }
            
            # Add GeoJson layer for grid square with style
            folium.GeoJson(
                grid_geometry,
                style_function=lambda feature: {
                    'color': 'white',
                    'fillOpacity': 0.1,
                    'fillColor': 'blue',  # Change the color as needed
                },
            ).add_to(m)

# Save the map as an HTML file
m.save("map_with_squares_for_" + target_fish + ".html")
