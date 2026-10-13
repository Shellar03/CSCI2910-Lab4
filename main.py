import requests

def get_locations(city):
    # Finds 5 cities matching entered input and returns
    # latitude and longitude of selected city
    # using Open-Meteo geocoding api.
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 5,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if not data.get("results"):
        return None

    locations = []

    for result in data["results"]:
        locations.append({
            "name": result["name"],
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "country": result.get("country", ""),
            "region": result.get("admin1", "")
        })

    return locations

def get_weather(latitude, longitude):
    #Retrieve current weather and a seven-day forecast.

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "wind_speed_10m",
            "weather_code"
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max"
        ],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timezone": "auto",
        "forecast_days": 7
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()

def main():
    city = input("Enter a city name to see weather: ").strip()

    if not city:
        print("Please enter a city name.")
        return

    try:
        locations = get_locations(city)

        if not locations:
            print("Location not found, try another city.")
            return

        print("\nMatching locations:")

        for i, location in enumerate(locations, start=1):
            region = location["region"]
            country = location["country"]

            print(f"{i}. {location['name']}, "
                  f"{region}, {country}")

        
        while True:
            choice = input(
                f"\nChoose a location (1-{len(locations)}): "
            ).strip()

            try:
                choice = int(choice)
            except ValueError:
                print("Please enter a valid number.")
                continue

            if 1 <= choice <= len(locations):
                break

            print("Please enter a number from the list.")

        # The selection loop ends here.
        location = locations[choice - 1]

        print(f"\nWeather for {location['name']}, "
              f"{location['region']}, {location['country']}")

        weather = get_weather(
            location["latitude"],
            location["longitude"]
        )

        current = weather["current"]
        daily = weather["daily"]

        print("\n--- Current Weather ---")
        print(f"Temperature: {current['temperature_2m']} °F")
        print(f"Feels like: {current['apparent_temperature']} °F")
        print(f"Humidity: {current['relative_humidity_2m']}%")
        print(f"Precipitation: {current['precipitation']} in")
        print(f"Wind speed: {current['wind_speed_10m']} mph")

        print("\n--- Seven-Day Forecast ---")

        for i, date in enumerate(daily["time"]):
            high = daily["temperature_2m_max"][i]
            low = daily["temperature_2m_min"][i]
            rain = daily["precipitation_sum"][i]
            wind = daily["wind_speed_10m_max"][i]

            print(f"\n{date}")
            print(f"  High: {high} °F")
            print(f"  Low: {low} °F")
            print(f"  Precipitation: {rain} in")
            print(f"  Maximum wind: {wind} mph")


    except requests.RequestException as error:
        print(f"Could not retrieve location data: {error}")



if __name__ == "__main__":
    main()
