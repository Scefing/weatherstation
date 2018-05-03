#!/usr/bin/env python
import inkyphat
from PIL import Image, ImageFont
from stat_calc import regression_info, calc_delta_exp

def convert_to_delta(data):

    base, exponent = calc_delta_exp(data, as_string=True)

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

def create_informatics(data):
    if len(data) > 1:
        regress_info = regression_info(data)
        r_data = regress_info["r-value"]
        p_data = regress_info["p-value"]

        informatic = "Δ{0}{1} - {2}{3}".format(*convert_to_delta(data), r_data["relationship_symbol"], p_data["evidence_symbol"])
    else:
        informatic = "Δ{0}{1}".format(*convert_to_delta(data))

    return informatic



def show_image(infile, temp_data=None, pressure_data=None, humidity_data=None):
    font = ImageFont.truetype("/usr/local/share/fonts/DejaVuSans.ttf", 14)

    temp_info = create_informatics(temp_data)
    press_info = create_informatics(pressure_data)
    humidity_info = create_informatics(humidity_data)

    inkyphat.set_image(Image.open(infile))
    inkyphat.text((110,10), "{0:.1f}°F \n {1}".format(temp_data[-1], temp_info), inkyphat.BLACK, font)
    inkyphat.text((110,40), "{0:.0f} hPa \n {1}".format(pressure_data[-1],press_info), inkyphat.BLACK, font)
    inkyphat.text((110,70), "{0:.0f} %RH \n {1}".format(humidity_data[-1], humidity_info), inkyphat.BLACK, font)

    inkyphat.show()