import requests

def get_city_coords(city):
    #Find city latitude and longitude using Open-Meteo geocoding api.
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if not data.get("results"):
        return None

    location = data["results"][0]

    return {
        "name": location["name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "country": location.get("country", ""),
        "region": location.get("admin1", "")
    }

def main():
    city = input("Enter a city name to see weather: ").strip()

    if not city:
        print("Please enter a city name.")
        return

    try:
        location = get_city_coords(city)

        if location is None:
            print("Location not found, try another city.")
            return

        print(f"\nLocation found: {location['name']}")
        print(f"Region: {location['region']}")
        print(f"Country: {location['country']}")
        print(f"Latitude: {location['latitude']}")
        print(f"Longitude: {location['longitude']}")

    except requests.RequestException as error:
        print(f"Could not retrieve location data: {error}")


if __name__ == "__main__":
    main()
