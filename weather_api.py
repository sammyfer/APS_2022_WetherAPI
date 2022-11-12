from fastapi import FastAPI
import requests
import json


app = FastAPI(title="Weather API")
data = {
    "brazil": {
        "sao paulo": {
            "sao paulo": {
                "agua branca": {
                    "lat": -23.514959152027526,
                    "lon": -46.691385890335894
                },
                "vila prudente": {
                    "lat": -23.57894748483907,
                    "lon": -46.5797319207272
                }
            }
        },
        "rio de janeiro": {
            "rio de janeiro": {
                "copacabana": {
                    "lat": -22.969421213908124,
                    "lon": -43.186792436811515
                },
                "tijuca": {
                    "lat": -22.932522216442976,
                    "lon": -43.24119212050752
                }
            }
        }
    }
}


@app.get("/countries")
def countries():
    return list(data.keys())

@app.get("/states")
def states(country = None):
    if country == None:
        return "No country selected"
    else:
        return list(data.get(country.lower()).keys()) \
            if country.lower() in data.keys() \
            else "Country not found"

@app.get("/cities")
def cities(country = None, state = None):
    if country == None or state == None:
        return "Country or state not selected"
    else:
        return list(data.get(country.lower()).get(state.lower()).keys()) \
            if country.lower() in data.keys() and \
                state.lower() in data.get(country.lower()).keys() \
            else "Country/state not found"

@app.get("/regions")
def regions(country = None, state = None, city = None):
    if country == None or state == None or city == None:
        return "No country, state or city selected"
    else:
        return list(data.get(country.lower()).get(state.lower()).get(city.lower()).keys()) \
            if country.lower() in data.keys() and \
                state.lower() in data.get(country.lower()).keys() and \
                    city.lower() in data.get(country.lower()).get(city.lower()).keys() \
            else "Country/state/city not found"

@app.get("/weather")
def weather(country = None, state = None, city = None, regiao = None):
    if country == None or state == None or city == None or regiao == None:
        return "No country, state, city or region selected"
    else:
        coord=data.get(country.lower()).get(state.lower()).get(city.lower()).get(regiao.lower()) \
            if country.lower() in data.keys() and \
                state.lower() in data.get(country.lower()).keys() and \
                    city.lower() in data.get(country.lower()).get(state.lower()).keys() and \
                        regiao.lower() in data.get(country.lower()).get(state.lower()).get(city.lower()) \
            else None
        if coord != None:
            apiKey="39c5c786582008201a2591277862ab3f"
            lat=coord.get("lat")
            lon=coord.get("lon")
            response=requests.get("https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}".format(
                lat, lon, apiKey))
            result=json.loads(response.content.decode())
            return {
                "weather":result.get("weather")[0].get("main"),
                "weather_condition":result.get("weather")[0].get("description"),
                "temperature":result.get("main").get("temp"),
                "feels_like":result.get("main").get("feels_like"),
                "temp_min":result.get("main").get("temp_min"),
                "temp_max":result.get("main").get("temp_max")
            }
        else:
            return "Country/state/city not found"
