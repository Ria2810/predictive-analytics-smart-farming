import requests
import datetime

api_key = '24bc51dacdc05697ef93fd31dc765f0d'
location = 'New Delhi'
months = ['april', 'may', 'june'] # specify the months of interest here
years = [datetime.date.today().year-1, datetime.date.today().year-2, datetime.date.today().year-3] # specify the years of interest here

# define the function to retrieve weather data
def get_weather_data(location, month, year):
    url = f'http://api.weatherstack.com/current?access_key={api_key}&query={location}&historical_date={year}-{month}-01&hourly=0'
    response = requests.get(url)
    data = response.json()
    print(data)
    return data['historical']['weather'][0]

# initialize lists to store weather data
rainfall = []
humidity = []
temperature = []

# loop through the months and years of interest and retrieve weather data
for month in months:
    for year in years:
        data = get_weather_data(location, month, year)
        rainfall.append(data['total_precip'])
        humidity.append(data['avghumidity'])
        temperature.append(data['avgtemp'])

# calculate the average values for each weather parameter
avg_rainfall = sum(rainfall) / len(rainfall)
avg_humidity = sum(humidity) / len(humidity)
avg_temperature = sum(temperature) / len(temperature)

# print the average values
print(f'Average rainfall: {avg_rainfall} mm')
print(f'Average humidity: {avg_humidity} %')
print(f'Average temperature: {avg_temperature} °C')



# import requests

# # Weatherstack API endpoint and access key
# url = "http://api.weatherstack.com/current"
# access_key = "your_access_key"

# # Location information
# location = "New Delhi, India"

# # API parameters for current weather
# params = {
#     "access_key": access_key,
#     "query": location,
#     "units": "m",  # Use metric units
#     "fields": "temperature,humidity,precip",  # Include temperature, humidity, and precipitation fields
# }

# # Send API request and get JSON response
# response = requests.get(url, params=params).json()

# # Extract current weather data
# current = response.get("current")

# # Calculate average rainfall, humidity, and temperature
# rainfall = current.get("precip")
# humidity = current.get("humidity")
# temperature = current.get("temperature")

# # Print results
# print("Average rainfall: {} mm".format(rainfall))
# print("Average humidity: {}%".format(humidity))
# print("Average temperature: {}°C".format(temperature))
