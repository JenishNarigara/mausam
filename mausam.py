import requests
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class town(BaseModel):
    town : str

@app.post("/")
def weather(user : town):
    loc = "https://geocoding-api.open-meteo.com/v1/search"

    data = {
            "name" : user.town,
            "count" : 1,
            "language" : "en"
        }
    
    loc = requests.get(loc , params=data)

    if loc.status_code == 200:
            detail_url = "https://api.open-meteo.com/v1/forecast"
    
            town_loc = loc.json()
            
            location_of_town = town_loc["results"][0]
    
            location = {
               "latitude" : location_of_town['latitude'],
               "longitude" : location_of_town['longitude'],
                "current" : [
                        "temperature_2m",
                        "apparent_temperature",
                        "weather_code",
                        "relative_humidity_2m",
                        "wind_speed_10m",
                        "surface_pressure",
                ],
                "daily": ["temperature_2m_max", "temperature_2m_min"],
                "hourly": ["visibility"],
                "timezone": "auto"
            }
            weather_data = requests.get(url=detail_url , params=location)
            api = weather_data.json()
            api2 = api['current']
            api1 = api['daily']
            api3 = api['hourly']
            print(api)
    
    
            curr = datetime.now().hour

            details = {
                "city" : location_of_town['name'],
                "country" : location_of_town['country'],
                "temprature( ℃ )" : api2['temperature_2m'],
                "feels like( ℃ )" : api2['apparent_temperature'],
                "temp_max( ℃ )" : api1['temperature_2m_max'][0],
                "temp_min( ℃ )" : api1['temperature_2m_min'][0],
                "condition" : api2['weather_code'],
                "humidity( % )" : api2['relative_humidity_2m'],
                "wind speed( km/h )" : api2['wind_speed_10m'],
                "pressure( mbar )" : api2['surface_pressure'],
                "visibility( km )" : ((api3['visibility'][curr])/1000.0)
        }   
            return(details)  
    else:
        return("you have entered wrong town by mistake")
