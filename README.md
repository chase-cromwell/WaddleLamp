# WaddleLamp

Waddle Lamp is a DIY 3D Printed "NanoLeaf" clone.

The lamp is made of 3D Printed triangular panels with adressable RGB LED's inside. The panels have headers soldered onto both the input and output of each strip, so that more panels can be connected. I have 12 panels in use, with 36 LED modules. Each "module" is one corner of a panel, and includes 3 LEDs which are adressable as a group from the WS2811 chip.

The controller is a Raspberry Pi Zero W running a python script that communicates via serial to an Arduino Nano which directly controls the LEDs. The Pi connects to an Adafruit IO feed and decodes the word-color into RGB values using [MatPlotLib.colors](https://matplotlib.org/3.1.1/api/colors_api.html), which gets passed via serial to the Arduino in the format <command, R, G, B, Bri>.
