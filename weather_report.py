#!/usr/bin/env python
from multiprocessing import Manager
from weather import Weather, Unit
import geocoder
import inkyphat
from PIL import ImageFont


class WeatherReport():

    def __init__(self, city="Philadelphia", manager=None):

        if not manager:
            manager = Manager()
        self.information = manager.dict()

        self.information["weather_base"] = Weather(unit=Unit.FAHRENHEIT)

        if not city:
            geo_loc = geocoder.ip("me")
            self.information["city"] = geo_loc.city
        else:
            self.information["city"] = city
        self.information["location"] = self.information["weather_base"].lookup_by_location(self.information["city"])

        self.information["condition"] = None


    @staticmethod
    def change_location(weather_base_var=None, city_var=None, location_var=None, city="Philadelphia"):
        city_var = city

        location_var = weather_base_var.lookup_by_location(city_var)


    @staticmethod
    def show_weather_report(condition_var=None):

        font = ImageFont.truetype("/usr/local/share/fonts/DejaVuSans.ttf", 14)

        inkyphat.text((110, 10), condition_var.text, inkyphat.BLACK, font)

        inkyphat.show()

    def run(self, condition_var=None, location_var=None):
        condition_var = location_var.condition

        self.show_weather_report(condition_var)
