import requests
from fastapi import FastAPI
from pydantic import BaseModel

geo = "https://geocoding-api.open-meteo.com/v1/search"
app = FastAPI()

class town(BaseModel):
    town : str

# @app.post('/weather')
def weather(town):
    
    data = {
        "name" : town,
        "count" : 1,
        "language" : "en"
    }

    loc = requests.get(geo , params=data)
    if loc.status_code == 200:
        detail_url = "https://api.open-meteo.com/v1/forecast"

        town_loc = loc.json()
        
        location_of_town = town_loc["results"][0]

        location = {
           "latitude" : location_of_town['latitude'],
           "longitude" : location_of_town['longitude'],
            "current" : [
                    "us_aqi",
                    "uv_index",
                    "relative_humidity_2m"
            ]
        }

        weather_data = requests.get(url=detail_url , params=location)
        print(weather_data.status_code , weather_data.json())

        safe_aqi = {(weather_data.json()["current"]["us_aqi"]<= 100) : "good aqi",
                    (101 <= weather_data.json()["current"]["us_aqi"] <150) : "unhealthy for sensetive groups",
                     151 <= weather_data.json()["current"]["us_aqi"] < 200 : "Unhealthy (Limit outdoor activities)",
                     201 <= weather_data.json()["current"]["us_aqi"] <= 300 :"Very Unhealthy (Avoid outdoor activities)",
                     weather_data.json()["current"]["us_aqi"] > 300 : "hazardous",
                    weather_data.json()["current"]["us_aqi"] == None : "aqi is not available"
                    }

        safe_uv = { weather_data.json()["current"]["uv_index"] <=2.0:"low",
                    2.0 <  weather_data.json()["current"]["uv_index"] <=5.0 :"moderate",
                    5.0 < weather_data.json()["current"]["uv_index"] <= 7.0:"high",
                    7.0 < weather_data.json()["current"]["uv_index"] <= 10:"very high",
                    weather_data.json()["current"]["uv_index"] > 10.0: "extreme",
                    weather_data.json()["current"]["uv_index"] == None : "data is not available"

        }
        

    else :
        return("enter proper town name")

weather("bhavnagar")