#!/usr/bin/env python
import inkyphat
from PIL import Image, ImageFont

def show_image(infile,temp=None, pressure=None, humidity=None):
    font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 16)

    inkyphat.set_image(Image.open(infile))
    inkyphat.text((110,10), "{0:.2f}°F".format(temp), inkyphat.BLACK, font)
    inkyphat.text((110,30), "{0:.2f} hPa".format(pressure),inkyphat.BLACK, font)
    inkyphat.text((110,60), "{0:.3f} %RH".format(humidity), inkyphat.BLACK, font=font)

    inkyphat.show()