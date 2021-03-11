# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import pyowm # https://github.com/csparpa/pyowm
from time_utilities import TimeUtilities

# Weather services super class.
class WeatherService(object):
    """
    Weather services super class / interface
    """
    def __init__(self, default_city="Tennfjord"):
        self.default_city = default_city

    # Gets the weather
    def get_weather(self):
        pass


class OpenWeatherMap(WeatherService):
    def __init__(self, API_key="8d9a0e619982f573996fe93dc022a7aa"):
        """
        init
        :param API_key: 
        """
        super(OpenWeatherMap, self).__init__()
        self.owm = pyowm.OWM(API_key=API_key)

    def get_weather(self, location=None, date=None):
        """
        gets weather if only location and forecast if date parameter filled
        :param location: location to search for
        :param date: date to look for
        :return: a string describing the weather or forecast
        """
        if location is None:
            location = self.default_city
        if date is None:
            return self.get_current_weather(location)
        else:
            return self.get_forecast(location, date)

    def get_current_weather(self, location):
        """
        gets the current weather
        :param location: location to search for
        :return: a string describing the weather
        """
        try:
            observation = self.owm.weather_at_place(location)
            weather = observation.get_weather()
            status = weather.get_status()
            temperature = weather.get_temperature(unit="celsius")
            s = ""
            return "The weather in " + str(location) + " is " + status.lower() + \
                   ". The temperature is " + str(temperature["temp"]) + " degrees. "
        except pyowm.exceptions.not_found_error.NotFoundError:
            return "Sorry I could not find the weather in " + str(location) + ". "

    def get_raw_weather(self, location):
        """
            gets the current weather
            :param location: location to search for
            :return: a string describing the weather
            """
        try:
            observation = self.owm.weather_at_place(location)
            weather = observation.get_weather()
            status = weather.get_status()
            temperature = weather.get_temperature(unit="celsius")
            s = ""
            return status.lower(),str(temperature["temp"]), status
        except pyowm.exceptions.not_found_error.NotFoundError:
            return "Sorry I could not find the weather in " + str(location) + ". "


    def get_raw_forecast(self, location, date):
        """
            gets the forecast
            :param location: location to search for
            :return: a string describing the forecast
            """
        try:
            forecast = self.owm.daily_forecast(location)
            weather = forecast.get_weather_at(date)
            status = weather.get_status()
            temperature = weather.get_temperature(unit="celsius")
            return status.lower(), str(temperature["min"]),str(temperature["max"]), status
        except pyowm.exceptions.not_found_error.NotFoundError:
            return "Sorry I could not find the forecast for " + str(location) + ". "




    def get_forecast(self, location, date):
        """
        gets the forecast
        :param location: location to search for
        :return: a string describing the forecast
        """
        try:
            forecast = self.owm.daily_forecast(location)
            weather = forecast.get_weather_at(date)
            status = weather.get_status()
            temperature = weather.get_temperature(unit="celsius")
            return "The forecast for " + str(location) + " " + \
                   TimeUtilities.get_day_string(date).lower() + \
                   " is " + status.lower() + ". The temperature will be between " + \
                   str(temperature["min"]) + " and " + str(temperature["max"]) + " degrees. "
        except pyowm.exceptions.not_found_error.NotFoundError:
            return "Sorry I could not find the forecast for " + str(location) + ". "