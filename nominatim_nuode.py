import requests

class NominatimAPI:
    def __init__(self, user_agent: str):
        self.base_url = "https://nominatim.openstreetmap.org"
        self.user_agent = user_agent
        self.headers = {
            "User-Agent": self.user_agent
        }

    def geocode(self, address: str):
        """
        Perform forward geocoding to get latitude and longitude from an address.

        :param address: Address to geocode.
        :return: Tuple containing latitude and longitude.
        """
        url = f"{self.base_url}/search"
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()  # Raise an error if the request fails

        data = response.json()
        if data:
            # Extract latitude and longitude from the first result
            lat = data[0].get("lat")
            lon = data[0].get("lon")
            return lat, lon
        else:
            return None, None

if __name__ == "__main__":
    # Replace with your contact email or unique identifier for user-agent
    user_agent = "your_email@example.com"
    nominatim = NominatimAPI(user_agent)

    # Prompt user for input
    place_name = input("Enter the name of the place: ")
    
    # Get the coordinates
    lat, lon = nominatim.geocode(place_name)
    
    if lat and lon:
        print(f"The coordinates for {place_name} are:\nLatitude: {lat}, Longitude: {lon}")
    else:
        print(f"Coordinates for {place_name} could not be found.")