# import system libraries
import time
import serial
import time
import math
from matplotlib import colors
from keys import ADAFRUIT_IO_USERNAME
from keys import ADAFRUIT_IO_KEY
prev_color = ""
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
ser.flush()

# import Adafruit IO REST client
from Adafruit_IO import Client, Feed, RequestError

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we have a 'color' feed
    color = aio.feeds('lightsetting')
except RequestError: # create an `color` feed
    feed = Feed(name='lightsetting')
    color = aio.create_feed(feed)

while True:
    # grab the feed
    color_val = aio.receive(color.key)
    if color_val != prev_color:
        # check for 'preset' color functions, slow or fast rainbow, or turning the whole panel off
        if color_val.value == "rainbow slow" or color_val.value == "slow rainbow":
            # tell the Pi console whats been checked from Adafruit IO
            print('Recieved slow rainbow')
            # send the correct info to the Arduino
            ser.write(('<3, 40, 255, 255, 255>').encode('utf-8'))
        elif color_val.value == "rainbow fast" or color_val.value == "fast rainbow":
            print('Recieved fast rainbow')
            ser.write(('<3, 10, 255, 255, 255>').encode('utf-8'))
        elif color_val.value == "off":
            print('Recieved off command')
            ser.write(("<2>").encode('utf-8'))
        elif colors.is_color_like(color_val.value):
            # convert the color name to an array of RGBA values
            colorarray = colors.to_rgba_array(color_val.value)[0]
            # separate RGB colors to individual variables for ease of programming and multiply by 255,
            # since initial values are 0-1 and the Arduino needs 0-255 RGB values
            redcolor = math.floor(255*colorarray[0])
            greencolor = math.floor(255*colorarray[1])
            bluecolor = math.floor(255*colorarray[2])
            # tell the Pi console what the color values are
            print('Received Color: ')
            print(color_val.value)
            print(redcolor)
            print(greencolor)
            print(bluecolor)
            # send the color values to the Pi
            ser.write(("<1, "+str(redcolor)+", "+str(greencolor)+", "+str(bluecolor)+", 255>").encode('utf-8'))
            print(("<1, "+str(redcolor)+", "+str(greencolor)+", "+str(bluecolor)+", 255>"))
        else:
            print(color_val.value)
            print('Isn\'t a real color... so...')
        prev_color = color_val
    # let's wait a bit so we don't flood adafruit io's servers...
    time.sleep(1)
