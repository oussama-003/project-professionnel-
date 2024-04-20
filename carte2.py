import folium
import geopandas as gpd
from shapely.geometry import Polygon, Point

# Sample fish information dictionary (replace with actual data)
fish_info = {
    (0, 0): "Fish species found: Piranha, Catfish",
    (0, 1): "Fish species found: Trout, Salmon",
    # Add more fish information for other grid squares as needed
}

# Load French Guiana boundary data
gdf = gpd.read_file("mapppp.geojson")

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
        # Calculate grid boundaries
        grid_min_lat = min_lat + i * grid_size
        grid_max_lat = min_lat + (i + 1) * grid_size
        grid_min_lon = min_lon + j * grid_size
        grid_max_lon = min_lon + (j + 1) * grid_size

        # Create Point for the center of the grid square
        center_point = Point((grid_min_lon + grid_max_lon) / 2, (grid_min_lat + grid_max_lat) / 2)

        # Check if the center of the grid square is within French Guiana
        if not gdf.geometry.contains(center_point).any():
            continue  # Skip this grid square if it's not within French Guiana
        
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
        
        # Construct fish information message
        fish_info_message = fish_info.get((i, j), "Fish information not available")
        
        # Define colors for grid square
        if (i + j) % 2 == 0:
            fill_color = 'red'  # Even rows + even columns
        else:
            fill_color = 'blue'  # Odd rows + odd columns
        
        # Add GeoJson layer for grid square with tooltip and style
        folium.GeoJson(
            grid_geometry,
            style_function=lambda feature: {
                'color': 'black',
                'fillOpacity': 0,
                'fillColor': fill_color,
            },
            #tooltip=fish_info_message,  # Display fish information on hover
        ).add_to(m)
            
        # Construct the link for the popup marker
        link = '<a href="file:///C:/Users/oussa/Downloads/Nouveau%20html/ex01.html">Click here for more info</a>'
        
        # Add RegularPolygonMarker for grid square with popup
        marker = folium.Marker(
            [(grid_min_lat + grid_max_lat) / 2, (grid_min_lon + grid_max_lon) / 2],  # center of the grid square
            fill_color='red',  # default fill color
            number_of_sides=4,  # square
            radius=10,  # size of the marker
            popup=folium.Popup(fish_info_message + '<br>' + link),  # display fish information and link in popup when clicked
        )
        marker.add_to(m)

# Save the map as an HTML file
m.save("interactive_map_with_colored_grid_and_link.html")
