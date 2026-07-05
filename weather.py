#let's build a  weather app 
#
import requests#bcz we are going to use python request library feature 
import os #immporting os librabry will give the feature of getting our api key from .env file
from dotenv import load_dotenv#load_dotenv function is used to import any hidden passwords or 
#API Keys which are saved in .env file
#y just calling this function our key will be loaded from .env file to our environment variable 
#env variables or directly stored by our operating system not by our python script
#it acts like a global setting and are declared in our .env files 
#to save it from being pushed on git we use .gitignore 
#we  add  the files which we want to be ignored by the git while pushing code on git
#git becomes blind of there existing


load_dotenv() #this loads key value in env variable which is visisble to out os.environ.get(pasteapinamehereasit is in .env)

API_KEY=os.environ.get("WEATHER_API_KEY")#os.environ.get() reads itfrom .env file 

# This is the base URL of OpenWeather's current weather endpoint
# An endpoint is a specific URL that does one specific job
# This one job = return current weather for a city
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    #we use try-except to encounter the problems that can occur in future
    #internet problem,web server down etc
    try:
        #every api eeds some arguments in our case the openweather
        #OpenWeather API requires these parameters:
        # q = query (the city name)
        # appid = our API key (how they know who we are)
        # units = metric means celsius, imperial = fahrenheit
        # We use a dictionary because requests.get() 
        # automatically converts it to a proper URL like:
        # ?q=Faisalabad&appid=yourkey & units=metric
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        # Actually make the GET request to the API and it gets the status code which we can use in our if-else to determine
        # params= automatically attaches our dictionary to the URL
        # This is safer than building the URL manually and passing direct arguments in url whichi is not error prone like this 
        response = requests.get(BASE_URL, params=params)#simple get request

        # 200 = success — server found the city and returned data
        if response.status_code == 200:

            # .json() converts the raw JSON response text
            # into a Python dictionary we can navigate normally
            # Just like the dictionaries you learned in Day 4
            data = response.json()

            # The API returns a deeply nested dictionary
            # Let's extract only what we need into a clean dict
            # data["main"]["temp"] = goes into "main" key
            # then gets "temp" from inside it
            # data["weather"] = returns a LIST of conditions
            # [0] = we take the first (and usually only) condition
            # ["description"] = the text like "clear sky"
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"]
            }

        # 404 = city not found on the server
        # This is NOT our code's fault — wrong city name
        elif response.status_code == 404:
            return "City not found! Check spelling."

        # Any other status code = something unexpected happened
        else:
            return f"Unexpected Error : {response.status_code}"#we can use this to printanythin in return
    # This catches network errors — no internet, timeout etc
    # Exception as e = captures the actual error message
    # so we can print exactly what went wrong
    except Exception as e:
        return f"Request failed: {e}"


def display_weather(city):
    # Call get_weather() and store whatever it returns
    # It either returns a dictionary (success)
    # or a string error message (failure)
    weather = get_weather(city)

    # isinstance() checks what TYPE weather is
    # If it's a dict = request succeeded, show the data
    # If it's a string = something went wrong, show the error
    # This is why return is better than print inside functions
    # — we can check and use the returned value here
    if isinstance(weather, dict):#check if response is in dictionary format 
        # f-strings to display our data cleanly
        # weather['temperature'] pulls from our clean dictionary
        # not from the raw messy API response
        print(f"{'='*40}\n")
        print(f"  Weather Report — {weather['city']}, {weather['country']}")
        print(f"{'='*40}")
        print(f"  Temperature   : {weather['temperature']}°C")
        print(f"  Feels Like    : {weather['feels_like']}°C")
        print(f"  Humidity      : {weather['humidity']}%")
        print(f"  Condition     : {weather['description'].title()}")
        print(f"  Wind Speed    : {weather['wind_speed']} m/s")
        print(f"{'='*40}\n")
    else:
        # weather is a string error message — just print it
        print(f"\nError: {weather}\n")


# ============================================
# PROGRAM ENTRY POINT
# ============================================
# This is where the program actually starts running
# We ask the user for a city and pass it to display_weather()
# which calls get_weather() internally
# Clean separation: one function fetches, one function displays
city=input("Enter City Name : ")
display_weather(city)
