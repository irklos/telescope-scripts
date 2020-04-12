#!/usr/bin/env python
import time
import os
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
import RPi.GPIO as GPIO
import time
from socket import *
from config import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(RAN, GPIO.OUT)
GPIO.setup(RAP, GPIO.OUT)
GPIO.setup(DECP, GPIO.OUT)
GPIO.setup(DECN, GPIO.OUT)


RST = 0
file = open("/var/log/mount.log","a+") 

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image1 = Image.new('1', (width, height))
draw = ImageDraw.Draw(image1)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding
x = 0
#font = ImageFont.load_default()
font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf',24)


draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Write two lines of text.
disp.clear()
disp.display()
draw.text((x+10, top+5),       "MOTOR" ,  font=font, fill=255)
draw.text((x+10, top+30),       "TEST" ,  font=font, fill=255)

    # Display image.
disp.image(image1)
disp.display()
time.sleep(5)



if disp.height == 64:
    image = Image.open('/usr/share/indi/scripts/right.png').convert('1')
else:
    image = Image.open('/usr/share/indi/scripts/right.png').convert('1')

disp.image(image)
disp.display()
GPIO.output(RAN, GPIO.HIGH)
time.sleep(10)
GPIO.output(RAN, GPIO.LOW)


disp.clear()
disp.display()


draw.text((x+10, top+5),       "MOTOR" ,  font=font, fill=255)
draw.text((x+10, top+30),       "TEST" ,  font=font, fill=255)

    # Display image.
disp.image(image1)
disp.display()


time.sleep(2)

if disp.height == 64:
    image = Image.open('/usr/share/indi/scripts/left.png').convert('1')
else:
    image = Image.open('/usr/share/indi/scripts/left.png').convert('1')


disp.image(image)
disp.display()
GPIO.output(RAP, GPIO.HIGH)
time.sleep(10)
GPIO.output(RAP, GPIO.LOW)
disp.clear()
disp.display()


draw.text((x+10, top+5),       "MOTOR" ,  font=font, fill=255)
draw.text((x+10, top+30),       "TEST" ,  font=font, fill=255)

# Display image.
disp.image(image1)
disp.display()


time.sleep(2)

if disp.height == 64:
    image = Image.open('/usr/share/indi/scripts/up.png').convert('1')
else:
    image = Image.open('/usr/share/indi/scripts/up.png').convert('1')

disp.image(image)
disp.display()
GPIO.output(DECP, GPIO.HIGH)
time.sleep(10)
GPIO.output(DECP, GPIO.LOW)
disp.clear()
disp.display()



draw.text((x+10, top+5),       "MOTOR" ,  font=font, fill=255)
draw.text((x+10, top+30),       "TEST" ,  font=font, fill=255)

# Display image.
disp.image(image1)
disp.display()


time.sleep(2)

if disp.height == 64:
    image = Image.open('/usr/share/indi/scripts/down.png').convert('1')
else:
    image = Image.open('/usr/share/indi/scripts/down.png').convert('1')

disp.image(image)
disp.display()
GPIO.output(DECN, GPIO.HIGH)
time.sleep(10)
GPIO.output(DECN, GPIO.LOW)
disp.clear()
disp.display()
file.write("Motor test end\n")
file.close()
