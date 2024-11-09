import requests

# Define the Overpass API endpoint
overpass_url = "https://overpass-api.de/api/interpreter"

# Define the Overpass query
overpass_query = """
[out:json];
node["amenity"="restaurant"](37.7749,-122.4194,37.7849,-122.4094);
out;
"""
#lat min, long min, lat max, long max.


# Send the request
response = requests.get(overpass_url, params={'data': overpass_query})
data = response.json()

# Print results
for element in data['elements']:
    print(f"Name: {element.get('tags', {}).get('name', 'Unknown')}, Lat: {element['lat']}, Lon: {element['lon']}")