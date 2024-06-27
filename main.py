import requests
import json

def get_weather_data(lat, lon):
    url = f"https://api.weather.gov/points/{lat},{lon}"
    response = requests.get(url)
    data = response.json()
    """
    The resonse from the API call will be a JSON object. JSON uses key-value pairs to represent data.
    The response contains a key called 'properties' which contains a key called 'forecast'. A nested key:value sequence.
    The property 'forecast' contains the URL to the forecast data.
    """
    forecast_url = data['properties']['forecast']
    forecast_response = requests.get(forecast_url)
    return forecast_response.json()

def save_weather_data_to_json(weather_data, filename):
    with open(filename, 'w') as file:
        json.dump(weather_data, file)

def parse_weather_data(weather_data):
    forecasts = weather_data['properties']['periods']
    forecast_list = [] #Start with an empty list 
    for forecast in forecasts:
        date = forecast['startTime'].split("T")[0]
        time = forecast['startTime'].split("T")[1].split("-")[0]
        temperature = forecast['temperature']
        short_forecast = forecast['shortForecast']
        forecast_list.append([date, time, temperature, short_forecast])
    return forecast_list

def generate_html(forecast_list):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather Forecast</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f0f0f0;
                margin: 0;
            }
            table {
                border-collapse: collapse;
                width: 80%;
                margin: 20px;
                background-color: #ffffff;
            }
            th, td {
                padding: 12px;
                text-align: center;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #4CAF50;
                color: white;
            }
            tr:hover {
                background-color: #f5f5f5;
            }
        </style>
    </head>
    <body>
        <table>
            <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Temperature (F)</th>
                <th>Forecast</th>
            </tr>
    """
    for forecast in forecast_list:
        html_content += f"""
            <tr>
                <td>{forecast[0]}</td>
                <td>{forecast[1]}</td>
                <td>{forecast[2]}</td>
                <td>{forecast[3]}</td>
            </tr>
        """
    html_content += """
        </table>
    </body>
    </html>
    """
    return html_content

def save_html_to_file(html_content, filename):
    with open(filename, "w") as file:
        file.write(html_content)

if __name__ == "__main__":
    while True:
        print("Welcome to the Weather Forecast App! Would you like to:\n 1. Use your own latitude and longitude coordinates>\n 2. Use the coordinates from a given location? \n 3. Use prebuilt latitude and longitude?")
        choice = input("Enter 1, 2 or 3: ")

        if choice == '1':
            lat = input("Enter the latitude: ")
            lon = input("Enter the longitude: ")
            break

        elif choice == '2':
            location = input("Please Enter the location you would like to get the weather forecast for: ")
            location = location.replace(" ", "+")
            loc_response = requests.get(f"http://www.gps-coordinates.net/api/{location}")
            
            try:
                loc_response.raise_for_status()
                location_data = loc_response.json()
                lat = location_data['latitude']
                lon = location_data['longitude']
                break
            except requests.exceptions.RequestException as e:
                print(f"Error: Unable to retrieve location data. {e}")
            except KeyError:
                print("Error: Invalid location data received. Please try again.")
            continue

        elif choice == '3':
            lat = "40.760780"
            lon = "-111.891045"
            break

        else:
            print("Invalid choice. Please try again.")
            continue

    weather_data = get_weather_data(lat, lon)
    save_weather_data_to_json(weather_data, 'weather_data.json')
    parsed_data = parse_weather_data(weather_data)
    html = generate_html(parsed_data)
    save_html_to_file(html, "forecast.html")
    print(parsed_data)