#!/usr/bin/env python
import inkyphat
from PIL import Image, ImageFont
import math

def magnitude(x):
    return int(math.floor(math.log10(x)))

def calc_delta_exp(in_list):
    delta = max(in_list) - min(in_list)
    if delta > 0:
        mag_delta = magnitude(delta)
        delta_base = round(delta / (10**mag_delta))
        return str(delta_base), str(mag_delta)
    else:
        return "0", "0"


def convert_to_super(base, exponent):
    unicode_script = ""
    number_to_name = {"0": "\N{SUPERSCRIPT ZERO}", 
                      "1": "\N{SUPERSCRIPT ONE}", 
                      "2": "\N{SUPERSCRIPT TWO}", 
                      "3": "\N{SUPERSCRIPT THREE}", 
                      "4": "\N{SUPERSCRIPT FOUR}", 
                      "5": "\N{SUPERSCRIPT FIVE}",
                      "6": "\N{SUPERSCRIPT SIX}",
                      "7": "\N{SUPERSCRIPT SEVEN}",
                      "8": "\N{SUPERSCRIPT EIGHT}",
                      "9": "\N{SUPERSCRIPT NINE}"}
    for char in exponent:
        if char == "-":
            unicode_script += "\N{SUPERSCRIPT MINUS}"
        for number, name in number_to_name.items():
            if char == number:
                unicode_script += name
    return base, unicode_script


def show_image(infile, temp_data=None, pressure_data=None, humidity_data=None):
    font = ImageFont.truetype("/usr/local/share/fonts/DejaVuSans.ttf", 14)

    temp_delta = "Δ{0}{1}".format(*convert_to_super(*calc_delta_exp(temp_data)))
    press_delta = "Δ{0}{1}".format(*convert_to_super(*calc_delta_exp(pressure_data)))
    hum_delta = "Δ{0}{1}".format(*convert_to_super(*calc_delta_exp(humidity_data)))

    inkyphat.set_image(Image.open(infile))
    inkyphat.text((110,10), "{0:.1f}°F \n {1}".format(temp_data[-1], temp_delta), inkyphat.BLACK, font)
    inkyphat.text((110,40), "{0:.0f} hPa \n {1}".format(pressure_data[-1],press_delta), inkyphat.BLACK, font)
    inkyphat.text((110,70), "{0:.0f} %RH \n {1}".format(humidity_data[1], hum_delta), inkyphat.BLACK, font)

    inkyphat.show()