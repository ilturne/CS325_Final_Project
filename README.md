
# Weather Forecast App

Welcome to the Weather Forecast App! This application allows users to get weather forecasts using latitude and longitude coordinates. The forecasts are retrieved from the NOAA Weather API and are displayed in an HTML format.

## Table of Contents

- [Overview](#overview)
- [How to Use the Program](#how-to-use-the-program)
  - [Running the Program](#running-the-program)
  - [Understanding API Calls](#understanding-api-calls)
  - [Generating an HTML File](#generating-an-html-file)
- [Program Explanation](#program-explanation)
  - [get_weather_data Function](#get_weather_data-function)
  - [save_weather_data_to_json Function](#save_weather_data_to_json-function)
  - [parse_weather_data Function](#parse_weather_data-function)
  - [generate_html Function](#generate_html-function)
  - [save_html_to_file Function](#save_html_to_file-function)
- [Conclusion](#conclusion)

## Overview

This project aims to demonstrate how to:
1. Download data from the internet.
2. Parse a JSON file for specific information.
3. Inject content into a webpage.

## How to Use the Program

### Running the Program

1. Clone the repository from GitHub.
2. Install the required Python libraries:
   ```bash
   pip install requests
   ```
3. Run the program:
   ```bash
   python main.py
   ```
4. Follow the on-screen instructions to select the input method for latitude and longitude.

### Understanding API Calls

API calls are a way for applications to interact with external services. In this program, we use the NOAA Weather API to get weather forecasts. Here's a brief explanation of how API calls work:

1. **Making a Request**: We use the `requests` library to make an HTTP GET request to the NOAA Weather API using latitude and longitude coordinates.
   ```python
   url = f"https://api.weather.gov/points/{lat},{lon}"
   response = requests.get(url)
   ```
2. **Parsing the Response**: The response from the API is in JSON format. JSON (JavaScript Object Notation) is a lightweight data-interchange format that is easy for humans to read and write. JSON data is structured as key-value pairs, where each key is a string and each value can be a string, number, array, or another JSON object. Here's an example of JSON data:
   
   ```json
   {
       "key1": "value1",
       "key2": {
           "subkey1": "subvalue1"
       },
       "key3": [1, 2, 3]
   }
   ```

   In this program, the JSON response from the API is converted into a Python dictionary using the `response.json()` method:
   ```python
   data = response.json()
   ```

### Generating an HTML File

The program generates an HTML file to display the weather forecast in a table format. Here's how it works:

1. **Parsing Weather Data**: The JSON response from the API is parsed to extract relevant forecast information.
2. **Generating HTML Content**: The extracted data is formatted into an HTML table.
3. **Saving HTML to File**: The HTML content is saved to a file, which can be opened in any web browser.

## Program Explanation

### get_weather_data Function

This function retrieves weather data from the NOAA Weather API using the provided latitude and longitude coordinates.

```python
def get_weather_data(lat, lon):
    url = f"https://api.weather.gov/points/{lat},{lon}"
    response = requests.get(url)
    data = response.json()
    forecast_url = data['properties']['forecast']
    forecast_response = requests.get(forecast_url)
    return forecast_response.json()
```

### save_weather_data_to_json Function

This function saves the retrieved weather data to a JSON file.

```python
def save_weather_data_to_json(weather_data, filename):
    with open(filename, 'w') as file:
        json.dump(weather_data, file)
```

### parse_weather_data Function

This function parses the weather data to extract the date, time, temperature, and short forecast.

```python
def parse_weather_data(weather_data):
    forecasts = weather_data['properties']['periods']
    forecast_list = []
    for forecast in forecasts:
        date = forecast['startTime'].split("T")[0]
        time = forecast['startTime'].split("T")[1].split("-")[0]
        temperature = forecast['temperature']
        short_forecast = forecast['shortForecast']
        forecast_list.append([date, time, temperature, short_forecast])
    return forecast_list
```

### generate_html Function

This function generates HTML content to display the forecast data in a table.

```python
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
```

### save_html_to_file Function

This function saves the generated HTML content to a file.

```python
def save_html_to_file(html_content, filename):
    with open(filename, "w") as file:
        file.write(html_content)
```

## Conclusion

This Weather Forecast App demonstrates how to use API calls to retrieve data, parse JSON responses, and dynamically generate HTML content. By following the instructions and understanding the provided code, you can create a functional weather forecast web page.