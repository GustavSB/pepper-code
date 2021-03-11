# -*- coding: utf-8 -*-

from time_utilities import *

from weather import WeatherService, OpenWeatherMap

class WeatherAnswers(object):
    def __init__(self, language):
        self.default_language = language
        self.weather = OpenWeatherMap()
        self.time_util = TimeUtilities()

        self.words = {"thunderstorm":"Lyn og Torden",
                 "drizzle":"Yr",
                 "rain":"Regn",\
                "snow":"Snø",\
                "atmosphere":"Atmosfære",\
                "clear":"Klar himmel",\
                "clouds":"Overskyet",\
                "extreme":"Ekstrem vær",
                 "monday":"mandag",
                 "tuesday": "tirsdag",
                 "wednesday": "onsdag",
                 "thursday": "torsdag",
                 "friday": "fredag",
                 "saturday": "lørdag",
                 "sunday": "søndag"}




    def set_default_language(self, language):
        self.default_language = language


    def get_current_weather_sentence(self, language, location):
        status, temperature = self.__get_weather()

        print(temperature)
        temperature = int(round(float(temperature)))

        if language == "English":
            weather_sentence = "\\rspd=80\\ The weather in " + str(location) + " is " + status.lower() + \
                   ". The temperature is " + str(temperature) + " degrees. "
        else:
            weather_sentence = "I " + str(location) + " i dag blir det " + self.translate(status) + \
                               ". Det er omtrent " + str(temperature) + " grader ute. "

        return weather_sentence

    def get_forecast_weather_sentence(self, language, location, date=None):
        status, minTemp, maxTemp, date = self.__get_forecast(language, location, date)


        minTemp = int(round(float(minTemp)))
        maxTemp = int(round(float(maxTemp)))

        if language == "English":
            forecast = "\\rspd=80\\ The forecast for " + str(location) + " " + \
                       TimeUtilities.get_day_string(date).lower() + \
                       " is " + status.lower() + ". The temperature will be between " + \
                       str(minTemp) + " and " + str(maxTemp) + " degrees. "
        else:
            forecast = "Værmeldingen for " + str(location) + " på " + self.translate(TimeUtilities.get_day_string(date)) \
                       + " er " + self.translate(status) + "... Temperaturen vil bli mellom " + str(minTemp) \
                       + " og " + str(maxTemp) + " grader."

        return forecast


    def translate(self, word, from_lang="ENG", to_lang="NOR"):
        word = word.lower()

        return self.words.get(word)


    def __get_forecast(self, language, location, date=None):
        if date==None:
            date = self.time_util.get_tomorrow()
        weather_forecast_raw = self.weather.get_raw_forecast(location, date=date)

        return weather_forecast_raw[0], weather_forecast_raw[1], weather_forecast_raw[2], date


    def __get_weather(self):
        weather_raw = self.weather.get_raw_weather("Tennfjord")
        return weather_raw[0], weather_raw[1]