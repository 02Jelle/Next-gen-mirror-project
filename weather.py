import requests
api_key = "1b9be699604e82c1cc19a5158e44ccd9"


#Get temperature/humidity/wind_speed with openweathermap API, with api_key and the city
def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        #return the 3 elements we need
        return temperature, humidity, wind_speed
    else:
        print(f"Erreur: {data['message']}")
        return None, None, None


    
def weather_feedback():
    temperature, humidity, wind_speed = get_weather(api_key, "Ixelles")
    if temperature > 22 and humidity < 70 and wind_speed < 5:
        return "hot"
    elif temperature < 10:
        return "cold"
    else:
        return "good"
    
# Compare the results of get_weather() with the different clothes detected on the image and return a feedback based on the result
def weather_clothing_advice(clothing_types):
    temperature, humidity, wind_speed = get_weather(api_key, "Ixelles")
    
    advice = ""
    # Take different weather cases and different options of possible clothing types and give a feedback
    if temperature > 25 and humidity < 70 and wind_speed < 5:
        if any(item in clothing_types for item in [8.0, 5.0, 9.0, 10.0, 11.0]): #"top", "dress", "shorts", "skirt", "headwear"
            advice += "You're dressed well for the heat."
        else:
            advice += "You should wear something lighter for the heat."
    elif temperature < 10:
        if any(item in clothing_types for item in [5.0, 7.0, 4.0, 12.0]): #"dress", "pants", "outer", "scarf/tie"
            advice += "You're dressed enough for the cold."
        else:
            advice += "You should wear something warmer for the cold."
    else:
        advice += "You are well dressed for the current temperature."


    return advice