#!/usr/bin/env python
from weather import Weather, Unit
import geocoder
import inkyphat
from PIL import ImageFont


class WeatherReport():

    def __init__(self, city="Philadelphia"):

        self.weather_base = Weather(unit=Unit.FAHRENHEIT)

        if not city:
            geo_loc = geocoder.ip("me")
            self.city = geo_loc.city
        else:
            self.city = city
        self.location = self.weather_base.lookup_by_location(self.city)

        self.condition = None

    def change_location(self, city="Philadelphia"):
        self.city = city
        self.location = self.weather_base.lookup_by_location(self.city)

    def show_weather_report(self):

        font = ImageFont.truetype("/usr/local/share/fonts/DejaVuSans.ttf", 14)

        inkyphat.text((110, 10), self.condition.text, inkyphat.BLACK, font)

        inkyphat.show()


    def run(self):

        self.condition = self.location.condition

        self.show_weather_report()
