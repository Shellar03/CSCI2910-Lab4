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
        location = get_city_coords(city)

        if location is None:
            print("Location not found, try another city.")
            return

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
