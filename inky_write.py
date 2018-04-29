import inkyphat
from PIL import Image

def show_image(infile):
    inkyphat.paste(im=Image.open(infile))
    inkyphat.show()